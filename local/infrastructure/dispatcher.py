__author__ = 'civa'

import json, time
from .pipes import Pipe, MessageHook

IN = 'dispatcher_in_channel'
OUT = 'dispatcher_out_channel'

def msg_hook(pipe, message):
    pipe.log.info("[{0}] preprocessing message {1}".format(pipe.pipe_name, message))
    return message

class Dispatcher(Pipe):
    @MessageHook(hook=msg_hook)
    def on_receive(self, message, context):
        self.send(OUT, json.dumps(message))
