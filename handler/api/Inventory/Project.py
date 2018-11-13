#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import json

# 3rd-party Packages

# Local Packages
from classes.appliacation import LOGGER
from classes.schema.SchemaInventory import SchemaProject
from ._base import InventoryApiHandler

# CONST

# Class&Function Defination
class ProjectInventoryApiHandler(InventoryApiHandler):
    __route_path__ = "project"

    def post(self, *args, **kwargs):
        project = json.loads(self.request.body)
        modules  = project.pop("param")

        try:
            project = self.__schema__(**project)
            self.application.mysql.add(project)
            self.application.mysql.commit()

            for name, role in modules.items():
                self.application.mysql.add(self.__schema__(**{
                    "visiblename":name,
                    "parent_id":project.id,
                    "role":role
                }))
            self.application.mysql.commit()

        except Exception as e:
            self.application.mysql.rollback()
            LOGGER.exception('Error occur during create item')
            self.finish({"status": False, "msg": e.__str__()})

    @property
    def __schema__(self):
        return SchemaProject


# Logic
if __name__ == '__main__':
    pass
