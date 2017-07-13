#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from autophandlers import index
from system.hd_base import ErrorHandler

handlers = [
        (r'/', index.Index),


        (r".*", ErrorHandler)       # 404
]