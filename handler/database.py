#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.web

# Local Packages
from classes.appliacation import LOGGER

# CONST

# Class&Function Defination
class DatabaseHandler(tornado.web.RequestHandler):
    def get(self, *args,**kwargs):
        print(args)
        print(kwargs)
        print(self.application.engine.table_names())

    def traversal_table(self, name):
        self.application.mysql.query()



# Logic
if __name__ == '__main__':
    pass
