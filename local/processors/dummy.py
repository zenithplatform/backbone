__author__ = 'civa'

from base import BaseProcessor

class DummyProcessor(BaseProcessor):
    def __init__(self, **kwargs):
        super(DummyProcessor, self).__init__(**kwargs)

    def process(self, *args, **kwargs):
        return {'processor': 'Dummy', 'result': 'result'}