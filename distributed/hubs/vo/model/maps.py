__author__ = 'civa'

import os
from shared.loaders import JsonDataLoader

class FieldMapCollection(object):
    def __init__(self, providers):
        self.all_maps = []

        for provider, val in providers.iteritems():
            map = FieldMap(provider, val)

            self.all_maps.append(map)

    def get(self, provider, type, field=''):
        _map = None
        _fields = {}

        for map in self.all_maps:
            if map.provider == provider:
                _map = map
                break

        _fields = _map.fields

        if type not in _fields:
            return None

        if not field:
            return _fields[type]
        else:
            subfields = _fields[type]

            if field in subfields:
                return _fields[type].get(field)
            else:
                return None

    def __repr__(self):
        return '%s' % (self.all_maps)

class FieldMap(object):
    def __init__(self, provider, types):
        self.provider = provider
        self.fields = {}

        for typename, _fields in types.iteritems():
            self.fields[typename] = _fields

    def __repr__(self):
        return '%s %s' % (self.provider, self.fields)

class FieldMapLoader(JsonDataLoader):
    def __init__(self):
        root = os.path.abspath(os.path.join(__file__ ,"../../data"))
        filename = os.path.join(root, 'field_maps.json')
        super(FieldMapLoader, self).__init__(filename, cls=FieldMapCollection, auto=False)
