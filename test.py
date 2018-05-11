 #! /usr/bin/python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import Application
from tornado.options import parse_command_line
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

# system packages
import os

# self packages
from handlers.index import MainHandler

from handlers.project import ProjectListHandler

from handlers.deploy import DeployHandler
from handlers.deploy import DeployActionHandler
from handlers.deploy import TestHandler
from handlers.deploy import Test2Handler

from handlers.admin import AdminHandler
from handlers.admin import AdminEnvHandler
from handlers.admin import AdminContainerHandler
from handlers.admin import AdminAppTypeHandler
from handlers.admin import AdminAppHandler
from handlers.admin import AdminDeployRuleHandler
from handlers.admin import AdminDeployHistoryHandler
from handlers.admin import DbInitHandler

settings = {
    'login_url':'/login',
    'template_path':os.path.join(os.path.dirname(__file__), "templates"),
    'static_path' : os.path.join(os.path.dirname(__file__), 'statics'),
    'static_url_prefix':'/statics/'
}

application = Application([
    (r"/", MainHandler),

    (r"/admin", AdminHandler),
    (r"/admin/environment", AdminEnvHandler),
    (r"/admin/container", AdminContainerHandler),
    (r"/admin/app_type", AdminAppTypeHandler),
    (r"/admin/app", AdminAppHandler),
    (r"/admin/deploy_rule", AdminDeployRuleHandler),
    (r"/admin/deploy_history", AdminDeployHistoryHandler),
    (r"/dbinit", DbInitHandler),


    (r"/test", TestHandler),
    (r"/test2", Test2Handler),
], **settings)

if __name__ == "__main__":
    parse_command_line()
    # application.listen(60000)
    server = HTTPServer(application)
    server.listen(60000)
    IOLoop.current().start()