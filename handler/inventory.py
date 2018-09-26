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
from classes.appliacation import LOGGER
from classes.appliacation import Application
from classes.handlers import NotInitialized
from classes.schema.SchemaInventory import SchemaDistrict, SchemaHost, SchemaHostGroup

# CONST

# Class&Function Defination
"""
"""
class InventoryHandler(tornado.web.RequestHandler):
    """
    Base class of inventory items handlers.
    """
    def get(self):
        headers = {"Content-Type":""}
        headers.update(self.request.headers)

        self.finish(self.__json__) if headers["Content-Type"] == "application/json" else \
            self.render(self.__prefix__ + self.__view__, object = self.__object__)

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
        self.finish(str(item.id))

    def delete(self, *args, **kwargs):
        items = self.application.mysql.query(self.__schema__).filter(self.__schema__.id.in_(json_decode(self.request.body))).all()
        for item in items:
            self.application.mysql.delete(item)
        self.finish("DELETED")

    @property
    def __arguments__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}

    @property
    def __object__(self):
        return self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all() if \
            self.__schema__ is not NotInitialized else \
            None

    @property
    def __json__(self):
        records = self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all()
        rst = json.dumps([r.json() for r in records], ensure_ascii=False, indent=2)
        return rst if self.__schema__ is not NotInitialized else \
            json.dumps({"ERROR":"Not supported Content-Type"})

    @property
    def __schema__(self):
        return NotInitialized

    @property
    def __prefix__(self):
        return "inventory/"

    @property
    def __view__(self):
        return "inventory.html"

    @property
    def __alias__(self):
        return "HUMANREADABLENAME"

###############################
# Inventory item handlers
###############################
class DistrictHandler(InventoryHandler):
    @property
    def __schema__(self):
        return SchemaDistrict

    @property
    def __view__(self):
        return "district.html"
    
    @property
    def __alias__(self):
        return "District"

class HostHandler(InventoryHandler):
    @property
    def __schema__(self):
        return SchemaHost

    @property
    def __view__(self):
        return "host.html"

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


class HostGroupHandler(InventoryHandler):
    @property
    def __schema__(self):
        return SchemaHostGroup

    @property
    def __view__(self):
        return "host_group.html"

# application
app_inventory = Application([
    ("/inventory", InventoryHandler),
    ("/inventory/district", DistrictHandler),
    ("/inventory/host", HostHandler),
    ("/inventory/hostgroup", HostGroupHandler),
])

# Logic
if __name__ == "__main__":
    conn = dict(
        fqdn="192.168.3.9",
        port=22,
        username="root",
        password=" "
    )


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(**conn)
    ssh.close()
