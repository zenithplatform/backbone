import logging
from jsonweb import dumper
from astroquery.simbad import Simbad

from ..model.celestial_object import *
from commons.serialization import CelestialObjectEncoder
from commons.enums import Target
from ..providers.exceptions import ProviderException
from ..vo_config import VoConfig


class SimbadProvider():
    logger = None
    config = None

    def __init__(self):
        self.config = VoConfig()
        self.logger = logging.getLogger("vo")

    def configure(self):
        pass

    def search(self, params):
        kind = params.target

        if kind == Target.tostring(0):
            return self.search_objects(params)
            #return '{"result":"Object"}'
        else:
            #return self.search_catalog(params)
            return '{"result":"Catalog"}'

    def search_objects(self, params):
        Simbad.reset_votable_fields()

        fields = self.config.find("configuration/providers/Simbad/search_fields")
        Simbad.add_votable_fields(*fields)

        cel_objects = []
        wildcard = not params.exact

        try:
            if params.exact:
                result = Simbad.query_object(params.term, wildcard=wildcard)
            else:
                Simbad.ROW_LIMIT = 20
                if params.coordinates:
                    if params.epoch and params.equinox:
                        result = Simbad.query_region(params.coordinates,
                                                     radius=params.radius,
                                                     epoch=params.epoch,
                                                     equinox=params.equinox)
                    else:
                        result = Simbad.query_region(params.coordinates, radius=params.radius)
                else:
                    result = Simbad.query_region(params.term, radius=params.radius)

            if result:
                for entry in result:
                    identifiers = Simbad.query_objectids(entry["MAIN_ID"])
                    celestial_obj = CelestialObject(entry, identifiers)
                    cel_objects.append(celestial_obj)
            else:
                self.logger.info("Nothing found for '{0}'".format(params))

            obj_collection = CelestialObjectCollection(cel_objects)

            json_result = dumper(obj_collection, cls=CelestialObjectEncoder)
            self.logger.info("Result from Simbad for '{0}' \n {1}".format(params, json_result))
            return json_result
        except:
            self.logger.error("Error in SimbadProvider", exc_info=True)
            raise ProviderException("error", "something")

    def search_catalog(self, term):
        return ''