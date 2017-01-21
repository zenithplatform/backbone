__author__ = 'civa'

import os, path
import imp
import importlib
import inspect
'''
http://stackoverflow.com/a/30941292/522319
'''

class ModuleLoader(object):
    def __init__(self, directory=''):
        self.dir = directory

    def find(self, module, cls=''):
        package = None
        klass = None

        try:
            fp, pathname, description = imp.find_module(module, [self.dir])
        except ImportError:
            print "unable to locate module {0} at {1}".format(module, self.dir)
            return (None, None)

        try:
            package = imp.load_module(module, fp, pathname, description)
        except Exception, e:
            print e

        if cls:
            try:
                klass = getattr(package, cls)
            except Exception, e:
                print e

        return package, klass

    def load(self, module):
        full = os.path.join(self.dir, module + '.py')
        return imp.load_source(module, full)

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
