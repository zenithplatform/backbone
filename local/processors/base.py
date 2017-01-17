__author__ = 'civa'

from infrastructure.producer import Producer

class BaseProcessor(object):
    def __init__(self, **kwargs):
        if 'config' in kwargs:
            config = kwargs['config']
            self.producer = Producer('producer', config=config)

    def process(self, *args, **kwargs):
        args = list(args)
        obj = args[0]
        self.producer.send(obj)