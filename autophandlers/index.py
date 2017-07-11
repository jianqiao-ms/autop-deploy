#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# 系统包
from __future__ import absolute_import
from tornado.gen import coroutine


# 三方包
import torncelery

# 自定义包
from ._handler import BaseHandler

from proj.db import mysql_insert
from proj.db import mysql_delete
from proj.db import mysql_update
from proj.db import mysql_query
from proj.db import mysql_get

class Index(BaseHandler, object):
    def get(self):
        self.render("index.html")