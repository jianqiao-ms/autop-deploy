#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import logging
import traceback

# 3rd-party Packages
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler

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
    pass

class BashRequestHandler(BaseRequestHandler):
    """
    
    """
    pass
class UIRequestHandler(BaseRequestHandler):
    """
    
    """
    pass

class BaseWebSocketHandler(WebSocketHandler):
    pass

# Logic
if __name__ == '__main__':
    pass
