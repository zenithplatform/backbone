__author__ = 'civa'

import os, fnmatch

class JsonConfig():
    max_iter_levels = 0

    def get_absolute_path(self):
        path = self.traverse('*.cfg', os.path.dirname( __file__ ))
        return path

    def find(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    def traverse(self, pattern, path):
        self.max_iter_levels += 1

        try:
            result = ''
            for root, dirs, files in os.walk(path):
                for name in files:
                    if fnmatch.fnmatch(name, pattern):
                        result = os.path.join(root, name)
                        return result
                #if os.path.dirname(path) == 'ZenithHub':


                #path = os.path.abspath(os.path.join(path, os.pardir))
                #path = os.path.join(os.path.dirname(path), '..')
                #path = os.path.dirname(path)

                #if path.endswith('ZenithHub'):
                #    return None

                if self.max_iter_levels == 100:
                    return None

            return self.traverse(pattern, os.path.dirname(path))
        except:
            raise


