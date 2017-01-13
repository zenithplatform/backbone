__author__ = 'civa'

from jsonweb.encode import to_object, dumper, to_list

def catalog_item_encoder(catalog):
    return {"id":           catalog.ID,
            "name":         catalog.name,
            "description":  catalog.description,
            "status":       catalog.status,
            "mission":      catalog.mission,
            "is_obsolete":  catalog.is_obsolete,
            "density":      catalog.density,
            "popularity":   catalog.popularity,
            "wavelengths":  catalog.wavelengths,
            "astronomy":    catalog.astronomy,
            "links":        catalog.links}

def catalog_collection_encoder(catalog_collection):
    return {"catalogs":  catalog_collection.catalogs}

@to_object(suppress=["__type__"],handler=catalog_item_encoder)
class Catalog(object):

    def __init__(self):
        self.ID = ''
        self.name = ''
        self.description = ''
        self.status = ''
        self.is_obsolete = False
        self.density = 0.0
        self.popularity = 0.0
        self.media = '' #infos
        self.target = '' #infos
        self.mission = ''
        self.wavelengths = []
        self.astronomy = []
        self.links = []

    def create(self, cat):
        self.ID = cat.ID
        self.description = cat.description
        self.name = cat.name

        for info in cat.infos:
            if info.ID == 'status':
                self.status = info.value

                if self.status == 'obsolete':
                    self.is_obsolete = True
                else:
                    self.is_obsolete = False
            elif info.name == '-kw.Astronomy':
                self.astronomy.append(info.value.replace("_", " "))
            elif info.name == '-kw.Mission':
                self.mission = info.value
            elif info.name == 'media':
                self.media = info.value
            elif info.name == '-density':
                self.density = info.value
            elif info.ID == 'ipopu':
                self.popularity = info.value
            elif info.name == '-kw.Wavelength':
                self.wavelengths.append(info.value.replace("optical", "Optical"))
            else:
                continue

        for link in cat.links:
            self.links.append("http://vizier.u-strasbg.fr/viz-bin/{0}".format(link.action))

@to_object(suppress=["__type__"],handler=catalog_collection_encoder)
class CatalogCollection(object):
    catalogs = []

    def __init__(self, result):
        for result_entry in result:
            catalog = Catalog()
            catalog.create(result[result_entry])
            self.catalogs.append(catalog)

    def __iter__(self):
        for cat in self.catalogs:
            yield cat

def known_catalog_encoder(catalog):
    return {"short_code":  catalog.short_code,
            "name":  catalog.name,
            "description":  catalog.description}

def known_catalogs_encoder(catalogs):
    return {"known_catalogs":  catalogs.catalog_list}

@to_object(suppress=["__type__"],handler=known_catalog_encoder)
class KnownCatalog(object):

    def __init__(self, short_code, name, description):
        self.short_code = short_code
        self.name = name
        self.description = description

@to_object(suppress=["__type__"],handler=known_catalogs_encoder)
class KnownCatalogCollection(object):

    def __init__(self):
        self.catalog_list = []

    def add(self, known_catalog):
        self.catalog_list.append(known_catalog)

    def __iter__(self):
        for cat in self.catalog_list:
            yield cat







