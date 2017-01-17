__author__ = 'civa'

import importlib
import inspect
'''
http://stackoverflow.com/a/30941292/522319
'''
class Loader(object):
    def __init__(self):
        self.modules = []

    def load(self, module_name):
        try:
            mod = importlib.import_module(module_name)
            self.modules.append(mod)
        except ImportError as e:
            print e.message

    def load_multiple(self, module_names):
        imported = map(self.load, module_names)

        for mod in imported:
            self.modules.append(mod)

    def clear(self):
        del self.modules[:]

    def enum_all(self):
        for mod in self.modules:
            self.get_contents(mod)

    def get_contents(self, module):
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                print 'Class %s' % name
            elif inspect.isfunction(obj):
                print 'Function %s' % name
            elif inspect.ismethod(obj):
                print 'Method %s' % name
