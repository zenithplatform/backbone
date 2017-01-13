__author__ = 'civa'

class SearchTarget:
    Object, Catalog = range(2)

class Target:
    Object, Catalog = range(2)

    @classmethod
    def tostring(cls, val):
        for k,v in vars(cls).iteritems():
            if v==val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str, None)