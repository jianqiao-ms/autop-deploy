#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os.path
import json

# 3rd-party Packages
# Local Packages
from classes.application import LOGGER
from classes.handlers import NotInitialized
from classes.handlers import RequestHandler

# CONST

# Class&Function Defination
class CIViewHandler(RequestHandler):
    """
    展示页面Handler
    继承这个类并重写__schema__和__template__属性，get方法默认查询__schema__所有记录并渲染__template__模板返回
    如果要自定义返回的内容，重写get_pre()方法

    render模板的数据格式：
    [{字段：值, 字段：值, ...}]
    """
    __route_base__ = "/view/ci"
    __route_path__ = ""
    def get(self):
        self.render(self.__template__, data = [])


    @classmethod
    def route(cls):
        if not len(cls.__route_path__):
            return cls.__route_base__
        return os.path.join(cls.__route_base__, cls.__route_path__)
    @property
    def __template__(self):
        if not len(self.__route_path__):
            return "ci/dashboard.html"
        return "ci/{}.html".format(self.__route_path__)

    @property
    def __schema__(self):
        return NotInitialized
    @property
    def __records_json__(self):
        if self.__schema__ is not NotInitialized:
            records = self.application.mysql.query(self.__schema__).order_by(self.__schema__.id).all()
            return [r.dict() for r in records]

# Logic
if __name__ == '__main__':
    pass
