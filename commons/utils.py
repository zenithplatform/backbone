__author__ = 'civa'

import re

class DictQuery(dict):

    def get(self, path, where = '', single=False, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    if where:
                        if '*' in where:
                            val = [v for v in val if v and (re.search(where.replace('*', '.'), v.get(key, default)) is not None)]
                        else:
                            val = [v for v in val if v and v.get(key, default) == where]

                        if single and val:
                            val = val[0]
                    else:
                        val = [v.get(key, default) if v else None for v in val]
                else:
                    if '*' in key:
                        for k, v in val.iteritems():
                            x = re.search(key.replace('*', '.'), k)

                            if x:
                                val = v
                                break
                    else:
                        val = val.get(key, default)

                    if where and val == where:
                        break
            else:
                if '*' in key:
                    for k, v in self.iteritems():
                        x = re.search(key.replace('*', '.'), k)

                        if x:
                            val = v
                            break
                else:
                    val = dict.get(self, key, default)

            if not val:
                break;

        return val

    '''
    Find key with selected value recursively
    DictQuery(some_dict).find('id', 5)
    '''
    def find(self, key, value):
        if key in self and self[key] == value:
            return self
        else:
            return self._find(self, key, value)

    def _find(self, data, key, value):
        if key in data and data[key] == value: return data

        for k, v in data.iteritems():
            if isinstance(v, dict):
                return self._find(v, key, value)
            elif isinstance(v, list):
                for item in v:
                    ret_val = self._find(item, key, value)

                    if ret_val is not None:
                        return ret_val