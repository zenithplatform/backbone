__author__ = 'civa'

import json
from infrastructure.pipes import Pipe

IN_REQUEST = 'agent_request_channel'
OUT_PRODUCE = 'agent_produce_channel'
IN_CALLBACK = 'agent_callback_channel'
OUT_DISPATCH = 'agent_dispatch_channel'

class Agent(Pipe):
    def distribute(self, channel_wrapper):
        name = channel_wrapper.channel_name
        channel = channel_wrapper.channel

        if name == IN_REQUEST:
            p_rq_message = channel.recv_json()
            self.send(OUT_PRODUCE, json.dumps(p_rq_message))
        elif name == IN_CALLBACK:
            p_rs_message = channel.recv_json()
            data = p_rs_message['json_data']
            self.send(OUT_DISPATCH, json.dumps(p_rs_message))