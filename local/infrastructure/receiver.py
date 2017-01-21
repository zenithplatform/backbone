__author__ = 'civa'

import time, json
from .pipes import Pipe

IN = 'receiver_in_channel'
OUT = 'receiver_out_channel'

class Receiver(Pipe):
    def before_receive(self, message):
        self.log.info("[{0}] preprocessing message {1}".format(self.pipe_name, message))
        return message

    def on_receive(self, message, context):
        self.send(OUT, json.dumps(message))