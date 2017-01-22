__author__ = 'civa'

import time, json
from .pipes import Pipe, MessageHook

IN = 'receiver_in_channel'
OUT = 'receiver_out_channel'

def msg_hook(pipe, message):
    pipe.log.info("[{0}] preprocessing message {1}".format(pipe.pipe_name, message))
    return message

class Receiver(Pipe):
    @MessageHook(hook=msg_hook)
    def on_receive(self, message, context):
        self.send(OUT, json.dumps(message))