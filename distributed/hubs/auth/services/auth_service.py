import os.path
import tornado.web
from .handlers.authentication import *

class AuthServiceApplication(tornado.web.Application):
    def __init__(self):
          project_dir = os.getcwd()

          handlers = [
                    (r"/api/users/login", LoginHandler),
                    (r"/api/users/signup", SignupHandler),
                    (r"/api/users/logout", LogoutHandler),
                ]

          settings = dict(
          )

          tornado.web.Application.__init__(self, handlers, **settings)
