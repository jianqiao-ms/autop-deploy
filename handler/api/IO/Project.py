#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from classes.schema.SchemaInventory import SchemaProject
from ._base import IOApiHandler


# CONST

# Class&Function Defination
class ProjectIOApiHandler(IOApiHandler):
    __route_path__ = "project"

    @property
    def __schema__(self):
        return SchemaProject


# Logic
if __name__ == '__main__':
    pass
