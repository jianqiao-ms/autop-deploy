#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from autophandlers import index
from autophandlers import admin
from autophandlers import deploy
from main.basehandler import ErrorHandler

handlers = [
        (r'/', index.Index),
        # 页面请求 map
        (r'/admin', admin.Admin),
        (r'/admin/(?P<modules>[a-z]+)', admin.Admin),
        (r"/deploy", deploy.Deploy),
        (r"/deploy/?(?P<modules>[a-z]+)", deploy.Deploy),

        # 数据库操作/管理操作 map
        (r'/new/host', admin.NewHost),
        (r'/new/hostgroup', admin.NewHostgroup),
        (r'/new/project', admin.NewProject),
        (r'/new/autorule', deploy.NewAutoRule),
        (r'/del/autorule', deploy.DelAutoRule),

        # 发布操作 map
        (r'/auto/(?P<token>.+)', deploy.Auto),

        (r".*", ErrorHandler)       # 404
    ]