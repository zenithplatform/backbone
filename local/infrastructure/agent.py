__author__ = 'civa'

import zmq, time, json
from infrastructure.dispatcher import Dispatcher
from infrastructure.pipes import LoopingPipe, chtype, chkind
from processors.dummy import DummyProcessor

class Agent(LoopingPipe):
    def setup(self):
        self.create_channel('p_request_channel', 18802, chtype.inbound, chkind.pull)
        self.create_channel('p_callback_channel', 18803, chtype.inbound, chkind.pull)

        self.poller = zmq.Poller()
        self.poller.register(self.get_channel('p_request_channel'), zmq.POLLIN)
        self.poller.register(self.get_channel('p_callback_channel'), zmq.POLLIN)

    def run_processor(self):
        dummy = DummyProcessor()
        dummy.process('test')

    def execute(self):
        self.dispatcher = Dispatcher()
        self.log.info("[AGENT] Started")

        while True:
            channels = dict(self.poller.poll())

            if channels.get(self.get_channel('p_request_channel')) == zmq.POLLIN:
                p_rq_message = self.get_channel('p_request_channel').recv_json()
                self.run_processor()

            # If the message came over the control channel, shut down the worker.
            if channels.get(self.get_channel('p_callback_channel')) == zmq.POLLIN:
                p_rs_message = self.get_channel('p_callback_channel').recv_json()
                self.log.info("[AGENT] : Processor %s finished: %s" % (p_rs_message['processor'], p_rs_message['result']))
                self.log.info("[AGENT] : Calling dispatcher")

                #send result to another process
                self.dispatcher.execute(json.dumps(p_rs_message))

            time.sleep(0.1)