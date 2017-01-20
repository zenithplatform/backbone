import tornado.web

from .handlers.search import SearchHandler
from .handlers.spectra import SpectraHandler
from .handlers.general import GeneralHandler
from .handlers.images import ImagesHandler
from ..vo_config import VoConfig


class VOApplication(tornado.web.Application):
    def __init__(self):
        config = VoConfig()
        base_path = "configuration/services/url_schemes"

        handlers = [
            (config.find(base_path+"/search"), SearchHandler),
            (config.find(base_path+"/general"), GeneralHandler),
            (config.find(base_path+"/spectra"), SpectraHandler),
            (config.find(base_path+"/images"), ImagesHandler)
        ]

        settings = dict(
            #autoescape=None,
        )

        tornado.web.Application.__init__(self, handlers, **settings)