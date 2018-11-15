#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
# 3rd-party Packages
import tornado.web
from tornado.escape import json_encode

# Local Packages

# CONST

# Class&Function Defination
def restricted(items):
    def decorator(func):
        import functools
        @functools.wraps(func)
        def pick_item(*args, **kwargs):
            if kwargs['item'] in items.keys():
                return func(*args, **kwargs)
            else:
                return args[0].finish(
                    json_encode({'result': 'ERROR', 'message': 'No such item [{}]'.format(kwargs['item'])}))
        return pick_item
    return decorator

class NotInitialized(object):
    id = ""
    visiblename = ""
    __visiblename__ = ""

class RequestHandler(tornado.web.RequestHandler):
    """
        FULL URI(route path) for handlers in /{__route_base__}/{__route_module__}/{__route_path__}
        __route_package__ : base directory in handler
        __route_module__ : modules in base
        __route_item__ : item(specific class) module
        For example : /view/inventory/project
        """
    __route_base__      = ""
    __route_module__    = ""
    __route_item__      = ""

    @classmethod
    def route(cls):
        return os.path.join("/", *filter(
            lambda x:len(x), (cls.__route_base__, cls.__route_module__, cls.__route_item__)
        ))

    @property
    def __arguments_dict__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}

class ViewRequestHandler(RequestHandler):
    """
    Handlers responsable for explorer get request, render a template and return to the client.
      Mostly used for data representation.
    Template html choosen based on __route_module__ and __route_item__, turns to \
      {TEMPLATE_PATH}/__route_modale__/__route_item__.html
    """
    __route_base__      = "view"
    __route_module__    = ""
    __route_item__      = ""

    @property
    def __template_new__(self):
        return "{}/new/{}.html".format(self.__route_module__, self.__route_item__)

    @property
    def __template__(self):
        return "{}.html".format(
            "/".join(filter(
                lambda x: len(x), (self.__route_module__, self.__route_item__)
            ))
        )

# Logic
if __name__ == '__main__':
    pass
