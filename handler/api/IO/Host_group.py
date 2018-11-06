#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.schema.SchemaInventory import SchemaHostGroup
from ._base import IOApiHandler


# CONST

# Class&Function Defination
class HostgroupIOApiHandler(IOApiHandler):
    __route_path__ = "hostgroup"

    @property
    def __schema__(self):
        return SchemaHostGroup


# Logic
if __name__ == '__main__':
    pass
