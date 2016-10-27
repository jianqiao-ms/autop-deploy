#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

# ucd
# u - update
# c - compile
# d - deploy

# celery App 子模块必须引入的包
from __future__ import absolute_import
from proj.celery import App
from proj.db import db_conn

# 异常
from torndb import IntegrityError
from socket import gaierror