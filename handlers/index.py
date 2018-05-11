#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages

# system packages

# self packages
from .base import BaseHandler

class MainHandler(BaseHandler):
    def get(self):
        self.render('index.html')