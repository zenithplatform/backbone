__author__ = 'civa'

class Singleton(object):
    def __init__(self, klass):
        self.klass = klass   # class which is being decorated
        self.instance = None  # instance of that class
    def __call__(self, *args, **kwargs):
        if self.instance is None:
            # new instance is created and stored for future use
            self.instance = self.klass(*args, **kwargs)
        return self.instance
