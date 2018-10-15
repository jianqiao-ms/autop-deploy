#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.web

# Local Packages
from classes.appliacation import Application

# CONST

# Class&Function Defination
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('base.html')

app_dashboard = Application([
    ('/', IndexHandler),
])

# Logic
if __name__ == '__main__':
    pass
