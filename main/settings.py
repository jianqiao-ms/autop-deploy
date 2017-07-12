#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import os
from main.jinja import JinjaLoader

settings = dict(
    debug           = True,
    gzip            = True,
    template_path   = os.path.join(os.path.dirname(__file__), "templates"),
    static_path     = os.path.join(os.path.dirname(__file__), "static"),
)

settings.update(dict(
    template_loader = JinjaLoader(os.path.join(os.path.dirname(__file__), settings['template_path']))
))