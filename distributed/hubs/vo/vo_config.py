__author__ = 'civa'

import os
import json
from shared.singleton import Singleton
from shared.utils import DictQuery

@Singleton
class VoConfig(dict):
    def __init__(self, *args, **kwds):
        self.name = None

    def load(self, filename, verbose=1, *args, **kwds):
        self.filename = filename
        self.verbose = verbose

        dict.__init__(self, *args, **kwds)

        if os.path.isfile(self.filename):
            self._read()
        else:
            if self.verbose:
                print "File '%s' doesn't exist." % (
                    self.filename
                )

    def _read(self):
        if self.verbose:
            print "Reading configuration from %r ..." % self.filename

        f = file(self.filename, "r")
        data = json.load(f)
        f.close()

        dict.update(self, data)

    def save(self):
        if self.verbose:
            print "Saving configuration to %r ..." % self.filename,

        f = file(self.filename, "w")
        json.dump(self, f, sort_keys=True, indent=4)
        f.close()
        if self.verbose:
            print "Configuration saved."

    def find(self, key):
        return DictQuery(self).get(key)
