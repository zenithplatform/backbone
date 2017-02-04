__author__ = 'civa'

import zmq, threading, logging, logging.config, sys, time, copy, json
from messages import PipeMessage, PipeMessageEncoder

class PipeError(Exception):
    def __init__(self, message, errors=None):
        super(PipeError, self).__init__(message)
        self.errors = errors

class messagehook(object):
    def __init__ (self, hook):
        self.hook = hook

    def __call__(self, func):
        def newf(*args, **kwargs):

            pipe = args[0]
            message = args[1]
            context = args[2]

            if pipe.verbose:
                pipe.log.info('[{0}] is preprocessing message {1}'.format(pipe.pipe_name, message))

            hooked_msg, hooked_ctx = self.hook(pipe, message, context)

            new_args = list(args)
            new_args[1] = hooked_msg
            new_args[2] = hooked_ctx

            func(*new_args, **kwargs)

        newf.__doc__ = func.__doc__

        return newf

class PipeChannel(object):
    def __init__(self, name, channel, metadata):
        self.name = name
        self.real_channel = channel
        self.metadata = metadata

        self.port = self.metadata['port']
        self.type = self.metadata['type']
        self.kind = self.metadata['kind']
        self.multiplex = self.metadata['multiplex']
        self.exit = self.metadata['exit']
        self.entry = self.metadata['entry']
        self.belongs_to = self.metadata['belongs_to']

    def __repr__(self):
        format_str = 'Channel : Name -> {0}, Port -> {1}, Type -> {2}, Kind -> {3}, Is Multiplex -> {4}, Is Entry -> {5}, Is Exit -> {6}, Belongs To -> {7}'
        return format_str.format(self.name,
                                 self.port,
                                 self.type,
                                 self.kind,
                                 self.multiplex,
                                 self.entry,
                                 self.exit,
                                 self.belongs_to)

class ChannelSetup(object):
    @classmethod
    def fromconfig(cls, config):
        if config:
            context = zmq.Context()
            pipeline = config.find('configuration/pipeline')
            channels = []

            for pipe_name, vals in pipeline.iteritems():
                channels_config = config.find('configuration/pipeline/{}/channels'.format(pipe_name))

                if not channels_config:
                    raise PipeError("Configuration not found for {}".format(pipe_name))

                for name, metadata in channels_config.iteritems():
                    metadata['belongs_to'] = pipe_name
                    channels.append(cls._new_channel("{0}_{1}_channel".format(pipe_name, name), context, **metadata))

            return context, channels

    @classmethod
    def _new_channel(cls, name, context, **kwargs):
        address = 'tcp://{0}:{1}'

        if len(kwargs) == 0:
            raise PipeError('Can not create channel {}. Check if configuration is valid.'.format(name))

        channel_metadata = copy.deepcopy(kwargs)

        ch_kind = kwargs.pop('kind', '')
        ch_port = kwargs.pop('port', 0)
        ch_type = kwargs.pop('type', '')

        try:
            channel = context.socket(cls.get_kind(ch_kind))
            val = getattr(chtype, ch_type)

            if val == chtype.inbound:
                channel.bind(address.format('*', ch_port))
            else:
                channel.connect(address.format('localhost', ch_port))

            return PipeChannel(name, channel, channel_metadata)
        except zmq.ZMQError as e:
            raise PipeError('Can not create channel {}.'.format(name), errors=e)

    @classmethod
    def get_kind(cls, kind):
        val = getattr(chkind, kind)

        if val == chkind.pull:
            return zmq.PULL
        elif val == chkind.push:
            return zmq.PUSH
        elif val == chkind.publish:
            return zmq.PUB
        elif val == chkind.subscribe:
            return zmq.SUB

class PipeContext(object):
    def __init__(self, channel, pipeline, should_exit=False):
        self.channel = channel
        self.pipeline = pipeline
        self.should_exit = should_exit

class looping_mode:
    single, multiplex = range(2)

class chtype:
    inbound, outbound = range(2)

class chkind:
    push, pull, publish, subscribe = range(4)

class PipeInput():
    def __init__(self):
        pass

class PipeOutput():
    def __init__(self):
        pass

class Pipe(threading.Thread):
    def __init__(self, pipeline, name, context, channels, config):
        self.active = True
        self.config = config
        self.pipeline = pipeline
        self.pipe_name = name
        self.context = context
        self.channels = channels
        self.multiplex = (getattr(looping_mode, self.config.find('configuration/pipeline/{}/mode'.format(name))) == looping_mode.multiplex)
        self._setup_logging()
        self.log = logging.getLogger(__name__)
        self.verbose = True
        threading.Thread.__init__(self)
        self.daemon = True

    def get_channel(self, name):
        if name in self.channels:
            wrapper = self.channels[name]
            return wrapper.real_channel
        else:
            raise PipeError('Channel {} does not exist.'.format(name))

    def _setup_logging(self, default_level=logging.INFO):
        section = self.config.find('configuration/logging')

        if section:
            logging.config.dictConfig(section)
        else:
            logging.basicConfig(level=default_level)

    def _start_polling(self):
        if self.verbose:
            self.log.info('[{}] started (multiplex)'.format(self.pipe_name))
            self.log.info('[{}] waiting for message'.format(self.pipe_name))

        self.multiplexer = zmq.Poller()
        self.multiplexer_result = None
        self.multiplex_channels = []

        for name, channel in self.channels.iteritems():
            if channel.multiplex:
                self.multiplexer.register(channel.real_channel, zmq.POLLIN)
                self.multiplex_channels.append(channel)

        while self.active:
            self.multiplexer_result = dict(self.multiplexer.poll())

            for channel in self.multiplex_channels:
                if self.multiplexer_result.get(channel.real_channel) == zmq.POLLIN:
                    try:
                        message = channel.real_channel.recv_json(zmq.NOBLOCK)
                    except zmq.ZMQError, e:
                        if e.errno == zmq.EAGAIN:
                            time.sleep(0.1)
                            continue
                        else:
                            raise PipeError('Can not receive data on channel {}.'.format(channel.name), errors=e)
                    else:
                        context = PipeContext(channel, self.pipeline)
                        self.on_receive(message, context)

            time.sleep(0.1)

    def _start_receiving(self):
        if self.verbose:
            self.log.info('[{}] started'.format(self.pipe_name))
            self.log.info('[{}] waiting for message'.format(self.pipe_name))

        while self.active:
            current_channel = None
            for name, channel in self.channels.iteritems():
                if channel.kind == 'pull' or channel.kind == 'sub':
                    current_channel = channel
                    break

            self._receive_message(current_channel)
            time.sleep(0.1)

    def _receive_message(self, current_channel):
        name = current_channel.name
        channel = current_channel.real_channel

        try:
            raw_message = channel.recv_json(zmq.NOBLOCK)
        except zmq.ZMQError, e:
            if e.errno == zmq.EAGAIN:
                time.sleep(0.1)
                pass
            else:
                raise PipeError('Can not receive data on channel {}.'.format(name), errors=e)
        else:
            context = PipeContext(current_channel, self.pipeline)
            self.on_receive(raw_message, context)

    def _close(self, specific_channels=None):
        if not specific_channels:
            for channel in self.channels:
                channel.close()
        else:
            for channel in specific_channels:
                channel.close()

        self.context.term()

    def _terminate_pipe(self):
        self.active = False

    def on_receive(self, message, context):
        pass

    def run(self):
        if self.multiplex:
            self._start_polling()
        else:
            self._start_receiving()

    def before_send(self, message):
        if self.verbose:
            self.log.info('[{0}] sending {1} ...'.format(self.pipe_name, message))

    def send(self, to, message):
        self.before_send(message)

        try:
            payload = json.dumps(message, cls=PipeMessageEncoder)
            self.get_channel(to).send(payload)
        except zmq.ZMQError as e:
            raise PipeError('Can not send data to channel {}.'.format(to), errors=e)

        self.after_send()

    def after_send(self):
        if self.verbose:
            self.log.info('[{}] Message sent'.format(self.pipe_name))

    def on_error(self):
        pass

    def close(self):
        if self.verbose:
            self.log.info('[{}] is closing'.format(self.pipe_name))
        self._terminate_pipe()

    def exit(self, message):
        if self.verbose:
            self.log.info('[{0}] is exiting pipeline with message {1}'.format(self.pipe_name, message))

        if self.pipeline:
            payload = json.dumps(message, cls=PipeMessageEncoder)
            self.pipeline.exit(payload)