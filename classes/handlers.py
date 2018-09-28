#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from tornado.web import RequestHandler
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


# Logic
if __name__ == '__main__':
    pass
