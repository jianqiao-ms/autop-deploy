#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import json

# 3rd-party Packages
import tornado.web
from tornado.escape import json_decode, json_encode

from sqlalchemy.exc import IntegrityError

# Local Packages
from classes.appliacation import LOGGER
from classes.newdict import NewDict
from classes.appliacation import Application

from classes.schema import ModalDistrict, ModalHost, ModalHostGroup

# CONST

# Class&Function Defination
class NotInitialized(object):
    def __init__(self):
        self.visiblename = ''
        self.id = ''

class InventoryHandler(tornado.web.RequestHandler):
    def get(self):
        headers = {"Content-Type":""}
        headers.update(self.request.headers)

        self.finish(self.__json__) if headers["Content-Type"] == "application/json" else \
            self.render(self.__view__, object = self.__object__)

    def post(self, *args, **kwargs):
        item = self.__schema__(**json_decode(self.request.body))

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
        except IntegrityError as e:
            LOGGER.exception()
            self.application.mysql.rollback()
            self.finish('{} named {} already exist!'.format(kwargs['item'], item.visiblename))
            return
        except:
            self.application.mysql.rollback()
            LOGGER.exception('Except during Create {}'.format(kwargs['item']))
            return
        self.finish(str(item.id))

    @property
    def __arguments__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}

    @property
    def __object__(self):
        return self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all() if \
            self.__schema__ is not NotInitialized else \
            None

    @property
    def __json__(self):
        records = self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all()
        rst = json.dumps([r.json() for r in records], ensure_ascii=False, indent=2)
        return rst if self.__schema__ is not NotInitialized else \
            json.dumps({"ERROR":"Not supported Content-Type"})

    @property
    def __schema__(self):
        return NotInitialized

    @property
    def __view__(self):
        return 'inventory.html'

class DistrictHandler(InventoryHandler):
    @property
    def __schema__(self):
        return ModalDistrict

    @property
    def __view__(self):
        return 'district.html'

class HostHandler(InventoryHandler):
    @property
    def __schema__(self):
        return ModalHost

    @property
    def __view__(self):
        return 'host.html'

class HostGroupHandler(InventoryHandler):
    @property
    def __schema__(self):
        return ModalHostGroup

    @property
    def __view__(self):
        return 'host_group.html'

# application
app_inventory = Application([
    ('/inventory', InventoryHandler),
    ('/inventory/district', DistrictHandler),
    ('/inventory/host', HostHandler),
    ('/inventory/hostgroup', HostGroupHandler),
])

# Logic
if __name__ == '__main__':
    pass
