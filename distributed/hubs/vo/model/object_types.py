__author__ = 'civa'

import os
from shared.loaders import JsonDataLoader

class ObjectTypes(object):
    otypes = []

    def __init__(self, types):
        for elem in types:
            otype = ObjectType(elem['identifier'], elem['short_name'], elem['short_code'], elem['description'])
            otype.parent = None

            if 'subtypes' in elem:
                self.load_subtypes(otype, elem['subtypes'])

            self.otypes.append(otype)

    def load_subtypes(self, otype, subtypes):
        for subtype in subtypes:
            if isinstance(subtype, dict):
                child = ObjectType(subtype['identifier'], subtype['short_name'], subtype['short_code'], subtype['description'])
                child.parent = otype
                otype.subtypes.append(child)

                if 'subtypes' in subtype:
                    self.load_subtypes(child, subtype['subtypes'])

    def find(self, name, formatted=False):
        found = None

        if not self.otypes:
            return None

        for ot in self.otypes:
            found = self.get(ot, name)

            if found:
                break

        while found.parent != None:
            found = found.parent

        if formatted:
            return "{0} ({1})".format(found.short_name, found.description)
        else:
            return found.short_name

    def get(self, parent, name):
        if parent.short_name == name:
            return parent

        for otype in parent.subtypes:
            elem = self.get(otype, name)

            if elem is not None:
                return elem

class ObjectType(object):
    def __init__(self, identifier, short_name, short_code, description):
        self.identifier = identifier
        self.short_name = short_name
        self.short_code = short_code
        self.description = description
        self.parent = ''
        self.subtypes = []

    def __repr__(self):
        return "%s %s" % (self.identifier, self.short_name)

    def add(self, subtype):
        self.subtypes.append(subtype)

class ObjectTypesLoader(JsonDataLoader):
    def __init__(self):
        root = os.path.abspath(os.path.join(__file__ ,"../../data"))
        filename = os.path.join(root, 'object_types.json')
        super(ObjectTypesLoader, self).__init__(filename, cls=ObjectTypes)