#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from tornado.web import RequestHandler

class BaseHandler(RequestHandler, object):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.db = self.application.db

class ErrorHandler(BaseHandler, object):
    def __init__(self, application, request, **kwargs):
        super(ErrorHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        self.write_error(404)

    def write_error(self, status_code, **kwargs):
        self.render('error.html', error_code=status_code)