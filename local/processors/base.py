__author__ = 'civa'

class BaseProcessor(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def process(self, json):
        pass