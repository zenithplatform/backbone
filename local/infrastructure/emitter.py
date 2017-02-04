__author__ = 'civa'

import json, time
from local.infrastructure.pipes import Pipe

IN = 'emitter_in_channel'
OUT = 'emitter_out_channel'

class Emitter(Pipe):
    def on_receive(self, message, context):
        self.send(OUT, message)
