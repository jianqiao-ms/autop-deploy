#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.web

# Local Packages

# CONST

# Class&Function Defination
class HostHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.application.logger.info('asd')
        self.render('index.html')


# Logic
if __name__ == '__main__':
    pass
