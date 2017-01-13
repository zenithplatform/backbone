__author__ = 'civa'

import zmq, threading, logging, sys, time

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
    def __init__(self):
        self.channels = {}
        self.context = zmq.Context()

        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)

        self.setup()

    def create_channel(self, name, port, type=chtype.inbound, kind=chkind.pull):
        address = "tcp://{0}:{1}"
        channel = self.context.socket(self.get_channel_kind(kind))

        if type == chtype.inbound:
            channel.bind(address.format("*", port))
        else:
            channel.connect(address.format("localhost", port))

        self.channels[name] = channel

    def get_channel_kind(self, kind):
        if kind == chkind.pull:
            return zmq.PULL
        elif kind == chkind.push:
            return zmq.PUSH
        elif kind == chkind.publish:
            return zmq.PUB
        elif kind == chkind.subscribe:
            return zmq.SUB

    def get_channel(self, name):
        if name in self.channels:
            return self.channels[name]

    def execute(self, *args, **kwargs):
        pass

    def setup(self):
        pass

class LoopingPipe(Pipe, threading.Thread):
    def __init__(self):
        super(LoopingPipe, self).__init__()
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        self.execute()