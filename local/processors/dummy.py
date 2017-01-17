__author__ = 'civa'

from processors.base import BaseProcessor

class DummyProcessor(BaseProcessor):
    def __init__(self, **kwargs):
        super(DummyProcessor, self).__init__(**kwargs)

    def process(self, *args, **kwargs):
        #do some work and push results to the agent
        input_data = []
        message = {'json_data': { 'processor' : 'Dummy', 'result' : 'result' }, 'req_id':'989yyt67'}
        input_data.append(message)
        super(DummyProcessor, self).process(*input_data)