__author__ = 'civa'

import json
from infrastructure.dispatcher import Dispatcher
from infrastructure.pipes import LoopingPipe
from processors.dummy import DummyProcessor

class Agent(LoopingPipe):
    def run_processor(self):
        metadata = {'config': self.config}
        dummy = DummyProcessor(**metadata)
        dummy.process('test')

    def before_open(self):
        self.dispatcher = Dispatcher('dispatcher', self.config)
        self.log.info("[AGENT] Started")

    def on_receive(self, channel_wrapper):
        name = channel_wrapper.channel_name
        channel = channel_wrapper.channel

        if name == 'p_request_channel':
            p_rq_message = channel.recv_json()
            self.run_processor()
        elif name == 'p_callback_channel':
            p_rs_message = channel.recv_json()
            data = p_rs_message['json_data']
            self.log.info("[AGENT] : Processor %s finished: %s" % (data['processor'], data['result']))
            self.log.info("[AGENT] : Calling dispatcher")

            #send result to another process
            self.dispatcher.send(json.dumps(p_rs_message))