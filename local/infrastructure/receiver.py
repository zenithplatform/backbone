__author__ = 'civa'

import time, json
from infrastructure.pipes import Pipe

IN = 'receiver_in_channel'
OUT = 'receiver_out_channel'

class Receiver(Pipe):
    def receive(self):
        message = self.get_channel(IN).recv_json()
        self.send(OUT, json.dumps(message))