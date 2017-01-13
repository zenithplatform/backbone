__author__ = 'civa'

from processors.base import BaseProcessor

class DummyProcessor(BaseProcessor):
    def process(self, *args, **kwargs):
        #do some work and push results to the agent
        input_data = []
        message = { 'processor' : 'Dummy', 'result' : 'result' }
        input_data.append(message)
        super(DummyProcessor, self).process(*input_data)