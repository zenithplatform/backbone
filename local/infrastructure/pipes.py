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

class Pipe(object):
    def __init__(self, name, config=None):
        self.pipe_name = name
        self.config = config
        self.channels = {}
        self.context = zmq.Context()
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

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

    def before_open(self):
        pass

    def open(self, *args, **kwargs):
        pass

    def before_close(self):
        pass

    def close(self):
        pass

    def send(self, *args, **kwargs):
        pass

    def setup(self):
        if self.config:
            channels_config = self.config.find('configuration/pipeline/{}/channels'.format(self.pipe_name))

            for name, metadata in channels_config.iteritems():
                self.create_channel_ex(name, **metadata)

class LoopingPipe(Pipe, threading.Thread):
    def __init__(self, name, mode='single', config=None):
        super(LoopingPipe, self).__init__(name, config)
        self.polling = (getattr(looping_mode, mode) == looping_mode.multiplex)
        threading.Thread.__init__(self)
        self.daemon = True

    def poll(self):
        self.before_open()

        self.poller = zmq.Poller()
        self.poller_result = None
        self.polling_channels = []

        for name, wrapper in self.channels.iteritems():
            if wrapper.polling:
                self.poller.register(wrapper.channel, zmq.POLLIN)
                self.polling_channels.append(wrapper)

        while True:
            self.poller_result = dict(self.poller.poll())

            for channel_wrapper in self.polling_channels:
                if self.poller_result.get(channel_wrapper.channel) == zmq.POLLIN:
                    self.on_receive(channel_wrapper)
                    break

            time.sleep(0.1)

    def on_receive(self, channel_wrapper):
        pass

    def run(self):
        if self.polling:
            self.poll()
        else:
            self.open()