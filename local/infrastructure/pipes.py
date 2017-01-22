__author__ = 'civa'

import zmq, threading, logging, sys, time, copy

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
            modified_message = self.hook(pipe, message)

            new_args = list(args)
            new_args[1] = modified_message

            func(*new_args, **kwargs)

        newf.__doc__ = func.__doc__

        return newf

class ChannelWrapper(object):
    def __init__(self, channel_name, channel, metadata):
        self.channel_name = channel_name
        self.channel = channel
        self.metadata = metadata

        self.port = self.metadata['port']
        self.type = self.metadata['type']
        self.kind = self.metadata['kind']
        self.polling = self.metadata['polling']

    def __repr__(self):
        return "Channel : {0}, {1}, {2}, {3}, {4}}".format(self.channel_name,
                                                           self.metadata['port'],
                                                           self.metadata['type'],
                                                           self.metadata['kind'],
                                                           self.metadata['polling'])

class PipeContext(object):
    def __init__(self, channel):
        self.channel = channel

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
    def __init__(self, name, config=None):
        self.active = True
        self.context = zmq.Context()

        self.pipe_name = name
        self.config = config
        self.channels = {}

        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)
        self.verbose = True

        self.mode = self.config.find('configuration/pipeline/{}/mode'.format(self.pipe_name))
        self.polling = (getattr(looping_mode, self.mode) == looping_mode.multiplex)

        threading.Thread.__init__(self)
        self.daemon = True
        self.setup()

    def create_channel(self, name, **kwargs):
        address = "tcp://{0}:{1}"

        if len(kwargs) == 0:
            raise PipeError("Can not create channel {}. Check if configuration is valid.".format(name))

        channel_metadata = copy.deepcopy(kwargs)

        ch_kind = kwargs.pop('kind', '')
        ch_port = kwargs.pop('port', 0)
        ch_type = kwargs.pop('type', '')

        try:
            channel = self.context.socket(self.get_channel_kind(ch_kind))
            val = getattr(chtype, ch_type)

            if val == chtype.inbound:
                channel.bind(address.format("*", ch_port))
            else:
                channel.connect(address.format("localhost", ch_port))

            self.channels[name] = ChannelWrapper(name, channel, channel_metadata)
        except zmq.ZMQError as e:
            raise PipeError("Can not create channel {}.".format(name), errors=e)

    def get_channel_kind(self, kind):
        val = getattr(chkind, kind)

        if val == chkind.pull:
            return zmq.PULL
        elif val == chkind.push:
            return zmq.PUSH
        elif val == chkind.publish:
            return zmq.PUB
        elif val == chkind.subscribe:
            return zmq.SUB

    def get_channel(self, name):
        if name in self.channels:
            wrapper = self.channels[name]
            return wrapper.channel
        else:
            raise PipeError("Channel {} does not exist.".format(name))

    def setup(self):
        if self.config:
            channels_config = self.config.find('configuration/pipeline/{}/channels'.format(self.pipe_name))

            if not channels_config:
                raise PipeError("Configuration not found for {}".format(self.pipe_name))

            for name, metadata in channels_config.iteritems():
                self.create_channel(name, **metadata)

    def _start_polling(self):
        if self.verbose:
            self.log.info("[{}] started (multiplex)".format(self.pipe_name))
        self.poller = zmq.Poller()
        self.poller_result = None
        self.polling_channels = []

        for name, wrapper in self.channels.iteritems():
            if wrapper.polling:
                self.poller.register(wrapper.channel, zmq.POLLIN)
                self.polling_channels.append(wrapper)

        while self.active:
            if self.verbose:
                self.log.info("[{}] waiting for message".format(self.pipe_name))

            self.poller_result = dict(self.poller.poll())

            for channel_wrapper in self.polling_channels:
                if self.poller_result.get(channel_wrapper.channel) == zmq.POLLIN:
                    try:
                        message = channel_wrapper.channel.recv_json()
                        self.on_receive(message, PipeContext(channel_wrapper))
                    except zmq.ZMQError as e:
                        raise PipeError("Can not receive data on channel {}.".format(channel_wrapper.channel_name), errors=e)
                    finally:
                        break

            time.sleep(0.1)

        #self._close(self.polling_channels)

    def _start_receiving(self):
        if self.verbose:
            self.log.info("[{}] started".format(self.pipe_name))

        while self.active:
            if self.verbose:
                self.log.info("[{}] waiting for message".format(self.pipe_name))

            wrapper_channel = None
            for name, wrapper in self.channels.iteritems():
                if wrapper.kind == 'pull' or wrapper.kind == 'sub':
                    wrapper_channel = wrapper
                    break

            self._receive_message(wrapper_channel)
            time.sleep(0.1)

    def _receive_message(self, wrapper):
        name = wrapper.channel_name
        channel = wrapper.channel

        try:
            message = channel.recv_json()
            self.on_receive(message, PipeContext(wrapper))
        except zmq.ZMQError as e:
            raise PipeError("Can not receive data on channel {}.".format(name), errors=e)

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
        if self.polling:
            self._start_polling()
        else:
            self._start_receiving()

    def before_send(self):
        if self.verbose:
            self.log.info("[{}] sending".format(self.pipe_name))
        pass

    def send(self, to, *args, **kwargs):
        self.before_send()
        args = list(args)
        payload = args[0]

        try:
            self.get_channel(to).send(payload)
        except zmq.ZMQError as e:
            raise PipeError("Can not send data to channel {}.".format(to), errors=e)

        self.after_send()
        pass

    def after_send(self):
        if self.verbose:
            self.log.info("[{}] sent".format(self.pipe_name))
        pass

    def on_error(self):
        pass

    def close(self):
        if self.verbose:
            self.log.info("[{}] is closing".format(self.pipe_name))
        self._terminate_pipe()