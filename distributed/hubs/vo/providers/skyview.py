__author__ = 'civa'

import logging
from astroquery.skyview import SkyView
import vo_config as voconfig

class SkyViewProvider():

    logger = None
    config = None

    def __init__(self):
        self.config = voconfig.VoConfig()
        self.logger = logging.getLogger("vo")

    def configure(self):
        pass

    def get_images(self, params):
        if params.coordinates:
            paths = SkyView.get_images(coordinates=params.coordinates,
                                       survey=params.survey)
        else:
            paths = SkyView.get_images(position=params.term,
                                       survey=params.survey)

