__author__ = 'civa'

import json, time
from .pipes import Pipe

IN = 'dispatcher_in_channel'
OUT = 'dispatcher_out_channel'

class Dispatcher(Pipe):
    def on_receive(self, message, context):
        #message = self.get_channel(IN).recv_json()
        self.send(OUT, json.dumps(message))

    # def receive(self):
    #     message = self.get_channel(IN).recv_json()
    #     self.send(OUT, json.dumps(message))

