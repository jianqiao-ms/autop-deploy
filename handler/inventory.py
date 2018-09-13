#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
import tornado.web
from tornado.web import Application
from tornado.escape import json_decode, json_encode

from sqlalchemy.exc import IntegrityError

# Local Packages
from classes.newdict import NewDict
from classes.appliacation import LOGGER
from classes.handlers import restricted
from classes.schema import HostType
from classes.schema import Host

# CONST
items = NewDict(
    host = Host,
    hosttype = HostType
)

# Class&Function Defination
class InventoryHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')

    @restricted(items)
    def post(self, *args, **kwargs):
        item = items[kwargs['item']](**json_decode(self.request.body))

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
        except IntegrityError as e:
            self.application.mysql.rollback()
            self.finish('{} named {} already exist!'.format(kwargs['item'], item.visiblename))
            return

        self.finish(str(item.id))

    @restricted(items)
    def delete(self, *args, **kwargs):
        _ids = json_decode(self.request.body)["id"]

        try:
            line_deleted = self.application.mysql.query(items[kwargs['item']]).filter(items[kwargs['item']].id.in_(_ids)).delete()
            self.application.mysql.commit()
            self.finish(str(line_deleted))
        except Exception as e:
            LOGGER.exception('Error deleting {}'.format(kwargs['item']))
            self.finish(str(0))

    def put(self, *args, **kwargs):
        _ids = json_decode(self.request.body)["id"]
        a = self.application.mysql.query(items[kwargs['item']]).filter(items[kwargs['item']].id.in_(_ids))
        print(a.statement)

        a.all()
        for aa in a:
            print(aa)


# Logic
if __name__ == '__main__':
    pass
