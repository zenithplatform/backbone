__author__ = 'civa'

import json, time
from .pipes import Pipe

IN = 'dispatcher_in_channel'
OUT = 'dispatcher_out_channel'

class Dispatcher(Pipe):
    def before_receive(self, message):
        self.log.info("[{0}] preprocessing message {1}".format(self.pipe_name, message))
        return message

    def on_receive(self, message, context):
        self.send(OUT, json.dumps(message))
