__author__ = 'civa'

import zmq, random, time, threading, logging, sys

class Initiator(threading.Thread):
    def __init__(self):
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.log = logging.getLogger(__name__)
        self.context = zmq.Context()

        #channels
        self.receiver_channel = None
        self.callback_channel = None

        self.setup()

        threading.Thread.__init__(self)
        self.daemon = True

    def setup(self):
        self.receiver_channel = self.context.socket(zmq.PUSH)
        self.receiver_channel.connect("tcp://localhost:18801")

        self.callback_channel = self.context.socket(zmq.SUB)
        self.callback_channel.connect("tcp://localhost:18800")
        self.callback_channel.setsockopt(zmq.SUBSCRIBE, '')

    def send(self):
        random.seed()
        workload = random.randint(1, 100)
        self.receiver_channel.send(str(workload))
        self.log.info('[INITIATOR] Sending {0}'.format(workload))

    def run(self):
        while True:
            time.sleep(1)
            self.send()
            self.log.info('[INITIATOR] Waiting for callback')
            callback_message = self.callback_channel.recv_json()
            self.log.info('[CALLBACK] Received callback {0}'.format(callback_message))