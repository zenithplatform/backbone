__author__ = 'civa'

import logging

import tornado.web

from ...providers.params import BaseVOParams
from ...providers.skyview import SkyViewProvider
from ...providers.exceptions import ProviderException


class ImagesHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.logger = logging.getLogger("vo")

    def post(self, type):
        self.logger.info("Search handler received : \n\n {0}".format(self.request.body))
        params = BaseVOParams()

        try:
            provider = SkyViewProvider()
            provider.configure()

            u_params = params.unpack(self.request.body)
            response = provider.get_image(u_params)

            if response is not None:
                return self.write(response)

        except ProviderException as provider_exc:
            return self.write(provider_exc.message)
