__author__ = 'civa'

import time, json
from .pipes import Pipe

IN = 'receiver_in_channel'
OUT = 'receiver_out_channel'

class Receiver(Pipe):
    def on_receive(self, message, context):
        self.send(OUT, json.dumps(message))