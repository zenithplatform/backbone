__author__ = 'civa'

from infrastructure.producer import Producer

class BaseProcessor(object):
    def __init__(self):
        self.producer = Producer()

    def process(self, *args, **kwargs):
        args = list(args)
        obj = args[0]
        self.producer.execute(obj)