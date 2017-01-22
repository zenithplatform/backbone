__author__ = 'civa'

import json
from .pipes import Pipe, MessageHook

IN_REQUEST = 'agent_request_channel'
OUT_PRODUCE = 'agent_produce_channel'
IN_CALLBACK = 'agent_callback_channel'
OUT_DISPATCH = 'agent_dispatch_channel'

def msg_hook(pipe, message):
    pipe.log.info("[{0}] preprocessing message {1}".format(pipe.pipe_name, message))
    return message

class Agent(Pipe):
    @MessageHook(hook=msg_hook)
    def on_receive(self, message, context):
        name = context.channel.channel_name

        if name == IN_REQUEST:
            self.send(OUT_PRODUCE, json.dumps(message))
        elif name == IN_CALLBACK:
            data = message['json_data']
            self.send(OUT_DISPATCH, json.dumps(message))