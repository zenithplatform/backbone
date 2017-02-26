__author__ = 'civa'

import tornado.web

class SpectraHandler(tornado.web.RequestHandler):

    def url_scheme(self):
        return r"/api/spectra/([a-zA-Z0-9_\-]+)/?$"

    def get(self):
        return ''
