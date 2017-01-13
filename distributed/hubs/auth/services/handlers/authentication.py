__author__ = 'civa'

import tornado.web

class LoginHandler(tornado.web.RequestHandler):

    def post(self):
        if self.request.body:
            print self.request.body
            # user = AppUser()
            # requestData = json.loads(self.request.body)
            # user.login(requestData['username'], requestData['password'])
            #
            # json_result = dumper(user)
            #
            # return self.write(json_result)

class LogoutHandler(tornado.web.RequestHandler):

    def post(self):
        if self.request.body:
            print self.request.body
            # user = AppUser()
            # requestData = json.loads(self.request.body)
            # user.create_new(requestData['email_address'], requestData['username'], requestData['password'])
            #
            # json_result = dumper(user)
            #
            # return self.write(json_result)

class SignupHandler(tornado.web.RequestHandler):

    def post(self):
        if self.request.body:
            print self.request.body
            # user = AppUser()
            # requestData = json.loads(self.request.body)
            # user.create_new(requestData['email_address'], requestData['username'], requestData['password'])
            #
            # json_result = dumper(user)
            #
            # return self.write(json_result)
