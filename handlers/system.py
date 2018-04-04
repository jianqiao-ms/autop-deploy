#! /usr/bin/env python
#-* coding: utf-8 -*

import tornado.web

from .base import BaseHandler
from .base import authenticated

class SysAdminHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('index.html')

class DbInitHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('index.html')