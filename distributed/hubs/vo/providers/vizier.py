__author__ = 'civa'

import logging
import json

import requests
from astroquery.vizier import Vizier

from ..model.celestial_object import *
from ..model.catalog import *
from shared.enums import Target
from hubs.vo.providers.exceptions import ProviderException


class VizierProvider():

    logger = None

    def __init__(self):
        self.logger = logging.getLogger('vo')

    def configure(self):
        pass

    def search(self, params):
        target = params.target

        if target == Target.tostring(0):
            return self.search_objects(params)
        else:
            return self.search_catalogs(params)

    def search_objects(self, params):
        json_result = '{"objects":[]}'
        has_catalog_filter = (params.catalog_filter is not None)

        try:
            if params.exact:
                if has_catalog_filter:
                    result = Vizier.query_object(params.term,
                                                 catalog=params.catalog_filter)
                else:
                    result = Vizier.query_object(params.term)
            else:
                Vizier.ROW_LIMIT = 10
                if params.coordinates:
                    if has_catalog_filter:
                        result = Vizier.query_region(params.coordinates,
                                                     radius=params.radius,
                                                     catalog=params.catalog_filter)
                    else:
                        result = Vizier.query_region(params.coordinates,
                                                     radius=params.radius)
                else:
                    if has_catalog_filter:
                        result = Vizier.query_region(params.term,
                                                     radius=params.radius,
                                                     catalog=params.catalog_filter)
                    else:
                        result = Vizier.query_region(params.term, radius=params.radius)

            if result:
                print result
                # for entry in result:
                #     identifiers = Simbad.query_objectids(entry["MAIN_ID"])
                #     celestial_obj = CelestialObject(entry, identifiers)
                #     cel_objects.append(celestial_obj)
            else:
                self.logger.info("Nothing found for '{0}'".format(params))
        except:
            self.logger.error("Error in SimbadProvider", exc_info=True)
            raise ProviderException("error", "something")

        return json_result

    def search_catalogs(self, params):

        json_result = '{"catalogs":[]}'

        try:
            if params.all:
                return self.get_known_catalogs()

            catalog_list = Vizier.find_catalogs(params.term, include_obsolete=params.obsolete_catalogs)

            if catalog_list:
                catalogs = CatalogCollection(catalog_list)
                json_result = dumper(catalogs)
                self.logger.info("Result from Vizier catalog search for '{0}' \n {1}".format(params.term, json_result))
            else:
                self.logger.info("Nothing found for '{0}'".format(params.term))
        except:
            self.logger.error("Error in SimbadProvider", exc_info=True)
            raise ProviderException("error", "something")

        return json_result

    def get_known_catalogs(self):
        vizier_query_url = 'http://vizier.u-strasbg.fr/viz-bin/vizbrowse?type=acronyme'
        response = requests.get(vizier_query_url)
        json_str = response.content

        json_data = json.loads(json_str)
        catalog_collection = KnownCatalogCollection()

        for item in json_data:
            known_catalog = KnownCatalog(item["acro"], item["cat"], item["title"])
            catalog_collection.add(known_catalog)

        return dumper(catalog_collection)

    def search_cone(self, term):
        return ''
