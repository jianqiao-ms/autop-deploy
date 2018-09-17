#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import json

# 3rd-party Packages
import tornado.web
from tornado.web import Application
from tornado.escape import json_decode, json_encode

from sqlalchemy.exc import IntegrityError

# Local Packages
from classes.appliacation import LOGGER
from classes.newdict import NewDict
from classes.appliacation import Application

from classes.schema import District, HostTemplate, HostGroup, Host

# CONST

# Class&Function Defination

class DistrictHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        records = self.application.mysql.query(District).all()
        self.finish(json.dumps([r.json() for r in records], ensure_ascii=False, indent=2))

    def post(self, *args, **kwargs):
        item = District(**json_decode(self.request.body))

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

class HostTemplateHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        records = self.application.mysql.query(HostTemplate).all()
        self.finish(json.dumps([r.json() for r in records], ensure_ascii=False, indent=2))

    def post(self, *args, **kwargs):
        item = HostTemplate(**json_decode(self.request.body))

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
        except IntegrityError as e:
            LOGGER.exception()
            self.application.mysql.rollback()
            self.finish('HostTemplate named {} already exist!'.format(item.visiblename))
            return
        except:
            self.application.mysql.rollback()
            LOGGER.exception('Except during Create HostTemplate')
            return
        self.finish(str(item.id))

class HostHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        records = self.application.mysql.query(Host).all()
        self.finish(json.dumps([r.json() for r in records], ensure_ascii=False, indent=2))

    def post(self, *args, **kwargs):
        item = Host(**json_decode(self.request.body))

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
        except IntegrityError as e:
            LOGGER.exception()
            self.application.mysql.rollback()
            self.finish('Host named {} already exist!'.format(item.visiblename))
            return
        except:
            self.application.mysql.rollback()
            LOGGER.exception('Except during Create Host')
            return
        self.finish(str(item.id))

# application
app_inventory = Application([
    ('/inventory/district', DistrictHandler),
    ('/inventory/hosttemplate', HostTemplateHandler),
    ('/inventory/host', HostHandler)
])

# Logic
if __name__ == '__main__':
    pass
