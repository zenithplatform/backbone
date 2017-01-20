__author__ = 'civa'

import zmq, threading, logging, sys, time

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

    def create_channel_ex(self, name, **kwargs):
        address = "tcp://{0}:{1}"
        ch_kind = kwargs['kind']
        ch_port = kwargs['port']
        ch_type = kwargs['type']

        channel = self.context.socket(self.get_channel_kind(ch_kind))
        val = getattr(chtype, ch_type)

        if val == chtype.inbound:
            channel.bind(address.format("*", ch_port))
        else:
            channel.connect(address.format("localhost", ch_port))

        self.channels[name] = ChannelWrapper(name, channel, kwargs)

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

    def setup(self):
        if self.config:
            channels_config = self.config.find('configuration/pipeline/{}/channels'.format(self.pipe_name))

            for name, metadata in channels_config.iteritems():
                self.create_channel_ex(name, **metadata)

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

        while True:
            if self.verbose:
                self.log.info("[{}] waiting for message".format(self.pipe_name))

            self.poller_result = dict(self.poller.poll())

            for channel_wrapper in self.polling_channels:
                if self.poller_result.get(channel_wrapper.channel) == zmq.POLLIN:
                    message = channel_wrapper.channel.recv_json()
                    self.on_receive(message, PipeContext(channel_wrapper))
                    break

            time.sleep(0.1)

    def _start_receiving(self):
        if self.verbose:
            self.log.info("[{}] started".format(self.pipe_name))

        while True:
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

        message = channel.recv_json()
        self.on_receive(message, PipeContext(wrapper))

    def run(self):
        if self.polling:
            self._start_polling()
        else:
            self._start_receiving()

    def on_receive(self, message, context):
        pass

    def before_send(self):
        if self.verbose:
            self.log.info("[{}] sending".format(self.pipe_name))
        pass

    def send(self, to, *args, **kwargs):
        self.before_send()
        args = list(args)
        payload = args[0]
        self.get_channel(to).send(payload)
        self.after_send()
        pass

    def after_send(self):
        if self.verbose:
            self.log.info("[{}] sent".format(self.pipe_name))
        pass

    def close(self):
        pass