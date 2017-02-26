__author__ = 'civa'

import logging
from jsonweb import dumper
from astroquery.simbad import Simbad

from ..model.celestial_object import *
from commons.serialization import CelestialObjectEncoder
from commons.enums import Target
from ..providers.exceptions import ProviderException
from ..providers.raw_result import RawResult, FuncResult, RawCoordinates
from ..model.result.base import ProviderResult
from commons.serialization import ProviderResultEncoder


class Resolver(object):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("vo")

    def configure(self):
        pass

    def resolve(self, params):
        kind = params.target
        valid = True

        if kind != Target.tostring(0):
            valid = False

        if valid:
            Simbad.reset_votable_fields()

            fields = self.config.find("configuration/providers/resolver/search_fields")
            Simbad.add_votable_fields(*fields)
            Simbad.remove_votable_fields('coordinates')

            cel_objects = []
            wildcard = not params.exact

            try:
                if params.exact:
                    table = Simbad.query_object(params.term, wildcard=wildcard)
                else:
                    Simbad.ROW_LIMIT = 20
                    if params.coordinates:
                        if params.epoch and params.equinox:
                            table = Simbad.query_region(params.coordinates,
                                                         radius=params.radius,
                                                         epoch=params.epoch,
                                                         equinox=params.equinox)
                        else:
                            table = Simbad.query_region(params.coordinates, radius=params.radius)
                    else:
                        table = Simbad.query_region(params.term, radius=params.radius)

                result = RawResult()
                result.load(table)
                result.foreach(self.get_all_coordinates)
                result.foreach(self.get_identifiers)
                result.foreach(self.get_result)

                # if result:
                #     for entry in result:
                #         identifiers = Simbad.query_objectids(entry["MAIN_ID"])
                #         celestial_obj = CelestialObject(entry, identifiers)
                #         cel_objects.append(celestial_obj)
                # else:
                #     self.logger.info("Nothing found for '{0}'".format(params))
                #
                # obj_collection = CelestialObjectCollection(cel_objects)
                #
                # json_result = dumper(obj_collection, cls=CelestialObjectEncoder)
                # self.logger.info("Result from Simbad for '{0}' \n {1}".format(params, json_result))
                #return json_result
                return None
            except:
                self.logger.error("Error in SimbadProvider", exc_info=True)
                raise ProviderException("error", "something")

    def get_identifiers(self, context, **kwargs):
        ids = Simbad.query_objectids(context["MAIN_ID"])
        return FuncResult(ids, merge=True, merge_key='identifiers')
        #context['identifiers'] = TableConverter.to_dict(ids, True)['ID']

    def get_all_coordinates(self, context, **kwargs):
        coordinates = RawCoordinates()
        main_id = context['MAIN_ID']
        coo_default = ['coo_wavelength', 'dec_prec', 'ra_prec']

        frames = {'ICRS' : 'coo(ICRS J2000)',
                  'FK5' : 'coo(FK5 J2000 2000)',
                  'FK4' : 'coo(FK4 B1950 1950)',
                  'GAL' : 'coo(GAL J2000)'}

        extract_input = []

        Simbad.reset_votable_fields()
        Simbad.add_votable_fields(*coo_default)
        Simbad.remove_votable_fields('coordinates', 'main_id')

        for frame in frames:
            field = frames[frame]
            Simbad.add_votable_fields(field)

            table = Simbad.query_object(main_id, wildcard=False)
            coordinates.add(frame, table)
            Simbad.remove_votable_fields(field)

        return FuncResult(coordinates, merge=True, merge_key='coordinates')

    def get_result(self, context, **kwargs):
        result = ProviderResult(context, 'Object', 'Simbad')
        print(dumper(result, cls=ProviderResultEncoder))

    # def _resolve(self, params):
    #     kind = params.target
    #     valid = True
    #
    #     if kind != Target.tostring(0):
    #         valid = False
    #         #return '{"result":"Object"}'
    #     else:
    #         #return self.search_catalog(params)
    #         return '{"result":"Catalog"}'
    #
    #     if valid:
    #         Simbad.reset_votable_fields()
    #
    #         fields = self.config.find("configuration/providers/resolver/search_fields")
    #         Simbad.add_votable_fields(*fields)
    #
    #         cel_objects = []
    #         wildcard = not params.exact
    #
    #         try:
    #             if params.exact:
    #                 result = Simbad.query_object(params.term, wildcard=wildcard)
    #             else:
    #                 Simbad.ROW_LIMIT = 20
    #                 if params.coordinates:
    #                     if params.epoch and params.equinox:
    #                         result = Simbad.query_region(params.coordinates,
    #                                                      radius=params.radius,
    #                                                      epoch=params.epoch,
    #                                                      equinox=params.equinox)
    #                     else:
    #                         result = Simbad.query_region(params.coordinates, radius=params.radius)
    #                 else:
    #                     result = Simbad.query_region(params.term, radius=params.radius)
    #
    #             if result:
    #                 for entry in result:
    #                     identifiers = Simbad.query_objectids(entry["MAIN_ID"])
    #                     celestial_obj = CelestialObject(entry, identifiers)
    #                     cel_objects.append(celestial_obj)
    #             else:
    #                 self.logger.info("Nothing found for '{0}'".format(params))
    #
    #             obj_collection = CelestialObjectCollection(cel_objects)
    #
    #             json_result = dumper(obj_collection, cls=CelestialObjectEncoder)
    #             self.logger.info("Result from Simbad for '{0}' \n {1}".format(params, json_result))
    #             return json_result
    #         except:
    #             self.logger.error("Error in SimbadProvider", exc_info=True)
    #             raise ProviderException("error", "something")