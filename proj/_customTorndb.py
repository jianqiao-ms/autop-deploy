#!/usr/bin/env python2
# -*- coding:UTF-8 -*-

import torndb

class Connection(torndb.Connection):
    def execute_rowcount(self, query, *parameters, **kwparameters):
        super(Connection, self).execute_rowcount(query, *parameters, **kwparameters)

    update = delete = execute_rowcount