#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os, sys
import io, json

# 3rd-party Packages
import tornado.web

# Local Packages

# CONST
CFG_FILE_OF_URL_MAP = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'url-map.json')

# Class&Function Defination
def str_to_class(str):
    return getattr(sys.modules[__name__], str)


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


# Logic
if __name__ == '__main__':
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "template")
    }

    with open(CFG_FILE_OF_URL_MAP, 'r') as config_file:
        url_map = list(map(
                lambda x: (x[0], str_to_class(x[1])),
                json.load(config_file).items()
        ))

    from tornado.options import parse_command_line
    from tornado.web import Application
    from tornado.ioloop import IOLoop

    parse_command_line()
    application = Application(url_map, **settings)
    application.listen(60000)
    IOLoop.current().start()
