import tornado.auth
import tornado.web
import tornado.ioloop
import tornado.httpserver
from .services import auth_service

def main():
    start_auth_service()
    tornado.ioloop.IOLoop.instance().start()

def start_auth_service():
    http_server = tornado.httpserver.HTTPServer(auth_service.AuthServiceApplication())
    http_server.listen(9192)
    print "Auth service is running on : http://{0}:{1}/{2}".format('localhost', 9192, "api")

if __name__ == "__main__":
    main()