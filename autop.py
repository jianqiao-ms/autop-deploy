#! /usr/bin/python
#-* coding: utf-8 -*

from tornado.web import Application
from tornado.options import parse_command_line
from tornado.ioloop import IOLoop

import os

from handlers.base import GitlabOAuth2LoginHandler
from handlers.root import MainHandler


from handlers.admin import AdminHandler

settings = {
    'login_url':'/login',
    'template_path':os.path.join(os.path.dirname(__file__), "templates")
}

application = Application([
    (r"/", MainHandler),
    (r"/login", GitlabOAuth2LoginHandler),
    (r"/admin", AdminHandler),
], **settings)

if __name__ == "__main__":
    parse_command_line()
    application.listen(60000)
    IOLoop.current().start()