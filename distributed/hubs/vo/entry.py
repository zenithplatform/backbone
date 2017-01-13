__author__ = 'civa'

import logging
import logging.config

import tornado.auth
import tornado.web
import tornado.ioloop
import tornado.httpserver

from hubs.vo.services import vo_app
import vo_config as cfg


class EntryPoint(object):

    logger = None

    def __init__(self):
        self.config = cfg.VoConfig()

    def configure(self):
        self.config.load(filename='vo_config.json')
        self.setup_logging()

    def start(self):
        success = True

        try:
            http_server = tornado.httpserver.HTTPServer(vo_app.VOApplication())

            port = self.config.find("configuration/vo_app/port")
            api_name = self.config.find("configuration/vo_app/api_name")

            http_server.listen(port)
            self.logger.info("VO application is running on : http://{0}:{1}/{2}".format('localhost', port, api_name))
        except Exception:
            self.logger.error("Unexpected error while starting VO application.", exc_info=True)
            success = False

        if success:
            tornado.ioloop.IOLoop.instance().start()


    def setup_logging(self, default_path='vo_config.json', default_level=logging.INFO):
        section = self.config.find("configuration/logging")

        if section:
            logging.config.dictConfig(section)
        else:
            logging.basicConfig(level=default_level)

        self.logger = logging.getLogger("vo")

