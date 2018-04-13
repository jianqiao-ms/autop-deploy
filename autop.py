#! /usr/bin/python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import Application
from tornado.options import parse_command_line
from tornado.ioloop import IOLoop

# system packages
import os

# self packages
from handlers.base import GitlabOAuth2LoginHandler
from handlers.root import MainHandler

from handlers.project import ProjectListHandler

from handlers.deploy import DeployHandler
from handlers.deploy import DeployActionHandler
from handlers.deploy import TestHandler
from handlers.deploy import Test2Handler

from handlers.admin import AdminHandler
from handlers.admin import DbInitHandler

settings = {
    'login_url':'/login',
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path' : os.path.join(os.path.dirname(__file__), 'statics'),
    'static_url_prefix':'/statics/'
}

application = Application([
    (r"/", MainHandler),
    (r"/login", GitlabOAuth2LoginHandler),

    (r"/project", ProjectListHandler),
    (r"/project", ProjectListHandler),

    (r"/deploy", DeployHandler),
    (r"/deployaction", DeployActionHandler),

    (r"/admin", AdminHandler),
    (r"/dbinit", DbInitHandler),


    (r"/test", TestHandler),
    (r"/test2", Test2Handler),
], **settings)

if __name__ == "__main__":
    parse_command_line()
    application.listen(60000)
    IOLoop.current().start()