__author__ = 'civa'

import json
from local.infrastructure.pipes import Pipe
from local.infrastructure.messages import PipeMessage
from local.dynamic.loader import Loader
from local.processors.dummy import DummyProcessor

IN = 'executor_in_channel'
OUT = 'executor_out_channel'

class Executor(Pipe):
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

        msg_obj = PipeMessage(message)
        msg_obj.write_body(**result)
        self.send(OUT, msg_obj.reprJSON())
