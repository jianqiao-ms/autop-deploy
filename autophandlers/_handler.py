#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

from tornado.web import RequestHandler

class BaseHandler(RequestHandler, object):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)