__author__ = 'civa'

class BaseProcessor(object):
    def __init__(self, **kwargs):
        pass

    def process(self, *args, **kwargs):
        args = list(args)
        return args[0]