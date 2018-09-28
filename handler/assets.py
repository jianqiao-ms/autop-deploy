#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import json
from socket import timeout

# 3rd-party Packages
import tornado.web
from tornado.escape import json_decode, json_encode
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import DBAPIError

import paramiko

# Local Packages
# from classes.appliacation import LOGGER
# from classes.appliacation import Application
from classes.handlers import NotInitialized
from classes.schema.SchemaInventory import SchemaDistrict, SchemaHost, SchemaHostGroup, \
    SchemaProjectType, SchemaProject

# CONST

# Class&Function Defination
"""
"""
class AssetsHandler(tornado.web.RequestHandler):
    """
    Base class of assets items handlers.
    """
    def get(self):
        headers = {"Content-Type":""}
        headers.update(self.request.headers)

        self.finish(self.__records_json__) if headers["Content-Type"] == "application/json" else \
            self.render(self.__prefix__ + self.__view__, objects = self.__records__, object_alias = self.__schema_alias__)

    def post(self, *args, **kwargs):
        headers = {"Content-Type": ""}
        headers.update(self.request.headers)
        item = self.__schema__(**json_decode(self.request.body))

        prepare_func = getattr(self, "post_pre", None)
        if prepare_func and callable(prepare_func):
            item = prepare_func(item)

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
        except IntegrityError as e:
            print(e)
            self.application.mysql.rollback()
            _ = e.params.popitem()
            result = {"status":False, "msg":"Dumpicate `{}` valued ({})".format(_[0], _[1])}
            self.finish(result) if headers["Content-Type"] == "application/json" else \
                self.finish(result["msg"])
            return
        except DBAPIError as e:
            self.application.mysql.rollback()
            result = {"status": False, "msg": e.__str__()}
            self.finish(result) if headers["Content-Type"] == "application/json" else \
                self.finish(result["msg"])
            return
        self.finish({"status":True, "msg":str(item.id)})

    def delete(self, *args, **kwargs):
        items = self.application.mysql.query(self.__schema__).filter(self.__schema__.id.in_(json_decode(self.request.body))).all()
        for item in items:
            # LOGGER.info("DELETE {} with id={}".format(self.__schema_alias__, item.id))
            self.application.mysql.delete(item)
        self.finish({"status":True, "msg":"DELETED"})

    @property
    def __arguments__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}

    @property
    def __schema__(self):
        return NotInitialized
    @property
    def __schema_alias__(self):
        return "HUMANREADABLENAME"
    @property
    def __records__(self):
        return self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all() if \
            self.__schema__ is not NotInitialized else \
            None
    @property
    def __records_json__(self):
        records = self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all()
        rst = json.dumps([r.json() for r in records], ensure_ascii=False, indent=2)
        return rst if self.__schema__ is not NotInitialized else \
            json.dumps({"status":False, "msg":"Not supported Content-Type"})

    @property
    def __prefix__(self):
        return "assets/"
    @property
    def __view__(self):
        return "assets.html"
    @property
    def __url__(self):
        return False



###############################
# Inventory item handlers
###############################
class DistrictHandler(AssetsHandler):
    @property
    def __schema__(self):
        return SchemaDistrict
    @property
    def __schema_alias__(self):
        return "HUMANREADABLENAME"
    @property
    def __view__(self):
        return "district.html"
    @property
    def __url__(self):
        return "district"

class HostHandler(AssetsHandler):
    @property
    def __schema__(self):
        return SchemaHost
    @property
    def __schema_alias__(self):
        return "Host"
    @property
    def __view__(self):
        return "host.html"
    @property
    def __url__(self):
        return "host"

    def post_pre(self, item):
        hostname = self.get_hostname(item)

        if not hostname["status"]:
            self.finish(hostname["msg"])
            return
        item.hostname = hostname["msg"]
        return item

    def get_hostname(self, host):
        conn = dict()
        conn["timeout"] = 30
        conn["hostname"] = host.ipaddr
        conn["port"] = 22 if not host.ssh_port else host.ssh_port
        conn["username"] = host.ssh_user
        conn["password"] = host.ssh_password if not host.ssh_auth_type == "rsa_key" else None

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(**conn)
        except timeout:
            pass
            return {"status":False, "msg":"Host {} not avilable, process terminated".format(host.ipaddr)}
        except paramiko.ssh_exception.AuthenticationException:
            pass
            return {"status":False, "msg":"Authentication failed"}
        except Exception as e:
            pass
            return {"status":False, "msg":e.__str__()}

        stdin, stdout, stderr = ssh.exec_command("hostname")
        hostname = stdout.read().decode()
        ssh.close()
        return {"status":True, "msg":hostname}


class HostGroupHandler(AssetsHandler):
    @property
    def __schema__(self):
        return SchemaHostGroup
    @property
    def __schema_alias__(self):
        return "Host Group"
    @property
    def __view__(self):
        return "host_group.html"
    @property
    def __url__(self):
        return "hostgroup"

class ProjectTypeHandler(AssetsHandler):
    @property
    def __schema__(self):
        return SchemaProjectType
    @property
    def __schema_alias__(self):
        return "Project Type"
    @property
    def __view__(self):
        return "project_type.html"
    @property
    def __url__(self):
        return "projecttype"


class ProjectHandler(AssetsHandler):
    @property
    def __schema__(self):
        return SchemaProject
    @property
    def __schema_alias__(self):
        return "Project"
    @property
    def __view__(self):
        return "project.html"
    @property
    def __url__(self):
        return "project"

# application
handler_list = [
    AssetsHandler,
    DistrictHandler,
    HostHandler,
    HostGroupHandler,
    ProjectTypeHandler,
    ProjectHandler
]
route_rules = list(
    map(lambda x:(str(x.__prefix__)+"/"+str(x.__url__) if x.__url__ else x.__prefix__, x), handler_list)
)
print(route_rules)
app_inventory = tornado.web.Application(route_rules)

# Logic
if __name__ == "__main__":
    pass