#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import logging
import traceback

# 3rd-party Packages
from tornado.web import RequestHandler

# Local Packages

# CONST

# Class&Function Defination
class BaseRequestHandler(RequestHandler):
    pass

class RESTRequestHandler(BaseRequestHandler):
    """
    返回json格式的错误信息
    默认格式
    {
        "message": "reason"
    }
    """
    def write_error(self, status_code: int, **kwargs):
        logging.exception(self._reason)
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header("Content-Type", "text/plain")
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish(dict(
                message = self._reason
            ))

class BashRequestHandler(BaseRequestHandler):
    """
    返回Raw格式的错误信息
    """
    def write_error(self, status_code: int, **kwargs):
        self.finish(self._reason)
        
class UIRequestHandler(BaseRequestHandler):
    """
    返回Raw格式的错误信息
    """
    def write_error(self, status_code: int, **kwargs):
        self.finish(self._reason)

# Logic
if __name__ == '__main__':
    pass
