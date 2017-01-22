__author__ = 'civa'

import json, time
from local.infrastructure.pipes import Pipe, messagehook

IN = 'dispatcher_in_channel'
OUT = 'dispatcher_out_channel'

class Dispatcher(Pipe):
    def preprocess(self, message):
        self.log.info("[{0}] preprocessing message {1}".format(self.pipe_name, message))
        return message

    @messagehook(hook=preprocess)
    def on_receive(self, message, context):
        self.send(OUT, json.dumps(message))
