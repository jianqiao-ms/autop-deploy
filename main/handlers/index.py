#!/usr/bin/env python
# -*- coding:UTF-8 -*-



class Index(BaseHandler, object):
    def get(self):
        self.render("index.html")