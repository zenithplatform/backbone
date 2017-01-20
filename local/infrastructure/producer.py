__author__ = 'civa'

import json
from .pipes import Pipe
from ..processors.dummy import DummyProcessor

IN = 'producer_in_channel'
OUT = 'producer_out_channel'

class Producer(Pipe):
    def on_receive(self, message, context):
        dummy = DummyProcessor()
        result = dummy.process('test')
        self.send(OUT, json.dumps(result))
