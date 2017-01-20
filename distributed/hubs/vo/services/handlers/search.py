__author__ = 'civa'

import logging

import tornado.web

from ...providers.params import BaseVOParams
from ...providers import ned, simbad, vizier
from ...providers.exceptions import ProviderException


class SearchHandler(tornado.web.RequestHandler):
    logger = None
    bootstrap = None

    def initialize(self):
        self.logger = logging.getLogger("vo")
        self.bootstrap = SearchBootstrap()

    def post(self, type):
        self.logger.info("Search handler received : \n\n {0}".format(self.request.body))
        params = BaseVOParams()

        try:
            provider = self.bootstrap.initialize(type)
            u_params = params.unpack(self.request.body)
            response = provider.search(u_params)

            if response is not None:
                return self.write(response)

        except ProviderException as provider_exc:
            return self.write(provider_exc.message)

class SearchBootstrap:

    def initialize(self, option):
        return self.options[option](self)

    def create_simbad(self):
        simbad_provider = simbad.SimbadProvider()
        simbad_provider.configure()

        return simbad_provider

    def create_vizier(self):
        vizier_provider = vizier.VizierProvider()
        vizier_provider.configure()

        return vizier_provider

    def create_ned(self):
        ned_provider = ned.NedProvider()
        ned_provider.configure()

        return ned_provider

    options = {'0' : create_simbad,
               '1' : create_vizier,
               '2' : create_ned,
    }
