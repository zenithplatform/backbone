__author__ = 'civa'

import tornado.web

class GeneralHandler(tornado.web.RequestHandler):

    def url_scheme(self):
        return r"/api/general/([a-zA-Z0-9_\-]+)/?$"

    def get(self):
        return ''
