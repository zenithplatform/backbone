__author__ = 'civa'

import os
import json

class JsonDataLoader(object):
    loaded = False
    auto = False
    cls = None
    filename = ''

    def __init__(self, filename, cls, auto=True):
        self.filename = filename
        self.auto = auto
        self.cls = cls

    def load(self):
        if self.loaded:
            return

        try:
            # root = os.path.abspath(os.path.join(__file__ ,"../../data"))
            # filename = os.path.join(root, 'object_types.json')
            f = file(self.filename, "r")
            str_data = f.read()
            f.close()

            data = json.loads(str_data)
            self.loaded = True

            if self.auto:
                return self.cls(**data)
            else:
                return self.cls(data)
        except:
            self.loaded = False
            raise
