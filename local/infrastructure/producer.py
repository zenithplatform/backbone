__author__ = 'civa'

import json
from infrastructure.pipes import Pipe
from processors.dummy import DummyProcessor

IN = 'producer_in_channel'
OUT = 'producer_out_channel'

class Producer(Pipe):
    def receive(self):
        message = self.get_channel(IN).recv_json()
        dummy = DummyProcessor()
        result = dummy.process('test')
        self.send(OUT, json.dumps(result))
