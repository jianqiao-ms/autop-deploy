#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os.path
import json

# 3rd-party Packages

# Local Packages
from classes.appliacation import LOGGER
from classes.handlers import NotInitialized
from classes.handlers import RequestHandler

# CONST

# Class&Function Defination
class InventoryApiHandler(RequestHandler):
    __route_base__ = "/api/v1/inventory"
    __route_path__ = ""
    def get(self):
        self.finish(self.__records__)

    def post(self, *args, **kwargs):
        result = None
        item = self.__schema__(**self.__request_data__)

        pre_func = getattr(self, "post_pre", None)
        if pre_func and callable(pre_func):
            try:
                item = pre_func(item)
            except Exception as e:
                LOGGER.exception("Prepare function failed!")
                self.finish({"status":False, "msg":e.__str__()})
                return

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
            result = {"status":True, "msg":str(item.id)}
        except Exception as e:
            self.application.mysql.rollback()
            LOGGER.exception('Error occur during create item')
            result = {"status": False, "msg": e.__str__()}
        finally:
            self.finish(result)

    def delete(self, *args, **kwargs):
        items = self.application.mysql.query(self.__schema__).filter(self.__schema__.id.in_(self.__request_data__)).all()
        for item in items:
            self.application.mysql.delete(item)
        self.finish({"status":True, "msg":"DELETED"})

    @classmethod
    def route(cls):
        return os.path.join(cls.__route_base__, cls.__route_path__)
    @property
    def __schema__(self):
        return NotInitialized
    @property
    def __query_arguments__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}
    @property
    def __request_data__(self):
        return json.loads(self.request.body)
    @property
    def __records__(self):
        try:
            records = self.application.mysql.query(self.__schema__).filter_by(**self.__query_arguments__).all()
            return json.dumps([r.dict() for r in records], ensure_ascii=False, indent=2)
        except Exception as e:
            return {"status":False, "msg": e.__str__()}


# Logic
if __name__ == '__main__':
    pass
