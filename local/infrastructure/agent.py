__author__ = 'civa'

import json
from .pipes import Pipe

IN_REQUEST = 'agent_request_channel'
OUT_PRODUCE = 'agent_produce_channel'
IN_CALLBACK = 'agent_callback_channel'
OUT_DISPATCH = 'agent_dispatch_channel'

class Agent(Pipe):
    def before_receive(self, message):
        self.log.info("[{0}] preprocessing message {1}".format(self.pipe_name, message))
        return message

    def on_receive(self, message, context):
        name = context.channel.channel_name

        if name == IN_REQUEST:
            self.send(OUT_PRODUCE, json.dumps(message))
        elif name == IN_CALLBACK:
            data = message['json_data']
            self.send(OUT_DISPATCH, json.dumps(message))