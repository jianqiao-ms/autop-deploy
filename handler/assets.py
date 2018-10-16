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
    route_path = "/assets"
    def get(self):
        headers = {"Content-Type":""}
        headers.update(self.request.headers)

        self.finish(self.__records_json__) if headers["Content-Type"] == "application/json" else \
            self.render(self.__prefix__ + self.__view__,
                        records = self.__records__,
                        schemaVisibleName = self.__schema__.__visiblename__,
                        formAction = self.route_path,
                        **self.__render_object__)

    def post(self, *args, **kwargs):
        result = None
        item = self.__schema__(**json_decode(self.request.body))

        pre_func = getattr(self, "post_pre", None)
        if pre_func and callable(pre_func):
            try:
                item = pre_func(item)
            except Exception as e:
                LOGGER.exception('Failed to get host name of {}'.format(item.ipaddr))
                self.finish({"status":False, "msg":e.__str__()})
                return

        try:
            self.application.mysql.add(item)
            self.application.mysql.commit()
            result = {"status":True, "msg":str(item.id)}
        except Exception as e:
            LOGGER.exception('Failed to get host name of {}'.format(item.ipaddr))
            result = {"status": False, "msg": e.__str__()}
        finally:
            self.application.mysql.rollback()
            self.finish(result)

    def delete(self, *args, **kwargs):
        items = self.application.mysql.query(self.__schema__).filter(self.__schema__.id.in_(json_decode(self.request.body))).all()
        for item in items:
            self.application.mysql.delete(item)
        self.finish({"status":True, "msg":"DELETED"})

    @property
    def __arguments__(self):
        return {k: self.get_argument(k) for k in self.request.arguments}

    @property
    def __schema__(self):
        return NotInitialized
    @property
    def __records__(self):
        return self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all() if \
            self.__schema__ is not NotInitialized else \
            None
    @property
    def __records_json__(self):
        records = self.application.mysql.query(self.__schema__).filter_by(**self.__arguments__).all()

        rst = json.dumps([r.dict() for r in records], ensure_ascii=False, indent=2)
        return rst if self.__schema__ is not NotInitialized else \
            json.dumps({"status":False, "msg":"Not supported Content-Type"})

    @property
    def __prefix__(self):
        return self.route_path.split("/")[1] + "/"
    @property
    def __view__(self):
        return "assets.html"

    @property
    def __render_object__(self):
        return dict()

###############################
# Inventory item handlers
###############################
class DistrictHandler(AssetsHandler):
    route_path = "/assets/district"
    @property
    def __schema__(self):
        return SchemaDistrict
    @property
    def __view__(self):
        return "district.html"

class HostHandler(AssetsHandler):
    route_path = "/assets/host"
    @property
    def __schema__(self):
        return SchemaHost
    @property
    def __view__(self):
        return "host.html"

    def post_pre(self, item):
        if item.type == "template":
            return item
        try:
            hostname = self.get_hostname(item)
        except Exception as e:
            raise e

        item.hostname = hostname
        return item

    def get_hostname(self, host):
        conn = dict()
        conn["timeout"] = 1
        conn["hostname"] = host.ipaddr
        conn["port"] = 22 if not host.ssh_port else host.ssh_port
        conn["username"] = host.ssh_user
        conn["password"] = host.ssh_password if not host.ssh_auth_type == "rsa_key" else None

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**conn)

        stdin, stdout, stderr = ssh.exec_command("hostname")
        hostname = stdout.read().decode()
        ssh.close()
        return hostname

    @property
    def __render_object__(self):
        return dict(
            districts = self.application.mysql.query(SchemaDistrict).all()
        )

class HostGroupHandler(AssetsHandler):
    route_path = "/assets/hostgroup"

    @property
    def __schema__(self):
        return SchemaHostGroup
    @property
    def __view__(self):
        return "host_group.html"

class ProjectTypeHandler(AssetsHandler):
    route_path = "/assets/projecttype"

    @property
    def __schema__(self):
        return SchemaProjectType
    @property
    def __view__(self):
        return "project_type.html"


class ProjectHandler(AssetsHandler):
    route_path = "/assets/project"

    @property
    def __schema__(self):
        return SchemaProject
    @property
    def __view__(self):
        return "project.html"


# application
app_inventory = Application(list(map(
    lambda x:(x.route_path, x),
    [
        AssetsHandler,
        DistrictHandler,
        HostHandler,
        HostGroupHandler,
        ProjectTypeHandler,
        ProjectHandler
    ]
)))

# Logic
if __name__ == "__main__":
    pass