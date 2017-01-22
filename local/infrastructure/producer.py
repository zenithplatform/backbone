__author__ = 'civa'

import json
from .pipes import Pipe, MessageHook
from ..dynamic.loader import Loader
from ..processors.dummy import DummyProcessor

IN = 'producer_in_channel'
OUT = 'producer_out_channel'

def msg_hook(pipe, message):
    pipe.log.info("[{0}] preprocessing message {1}".format(pipe.pipe_name, message))
    return message

class Producer(Pipe):
    @MessageHook(hook=msg_hook)
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
