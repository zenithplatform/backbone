__author__ = 'civa'

import json
from .pipes import Pipe
from ..dynamic.loader import Loader
from ..processors.dummy import DummyProcessor

IN = 'producer_in_channel'
OUT = 'producer_out_channel'

class Producer(Pipe):
    def before_receive(self, message):
        self.log.info("[{0}] preprocessing message {1}".format(self.pipe_name, message))
        return message

    def on_receive(self, message, context):
        #result = None
        # p = __import__('D:\Programming\Astronomy\Dev\ZenithPlatformSandbox\processors\fits.py')
        # m = getattr(p, 'fits')
        # c = getattr(m, 'FITSprocessor')
        # instance = c()
        # return instance
        # ldr = Loader()
        # ldr.load('processors.fits')
        dummy = DummyProcessor()
        result = dummy.process('test')
        self.send(OUT, json.dumps(result))
