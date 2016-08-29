#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import traceback
import time
import datetime

import tornado.ioloop
import tornado.web
import tornado.options
from tornado.gen import coroutine

from tasks import mysql_query

# 自定义方法，格式化返回数据
class DateJsonEncoder(json.JSONEncoder, object):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        else:
            return json.JSONEncoder.default(self, obj)

def fdumps(obj, status_code, request_method):
    if status_code >= 200 and status_code < 400:
        obj['status'] = 'OK'
    else:
        obj['status'] = 'ERROR'
    obj['status_code'] = status_code
    obj['request_method'] = request_method
    return json.dumps(obj, indent=4, cls=DateJsonEncoder)

# 自定义方法
def getLocaltime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

# 返回tornad app对象
settings = dict(
    debug = 'True'
)

def make_app():
    return tornado.web.Application([
        (r"/", Index),
        (r"^/assets"
            r"(?P<path0>/?)(?P<item>[A-Za-z]*)"
            r"(?P<path1>/?)(?P<function>[A-Za-z]*)", Assets),
        (r"^/deploy"
            r"(?P<path0>/?)(?P<item>[A-Za-z-]*)"
            r"(?P<path1>/?)(?P<function>[A-Za-z]*)", Deploy),
        (r".*", Error)
    ], **settings)

# 继承RequestHandler的自定基础类
class AddHeaderRequestHandler(tornado.web.RequestHandler,object):
    def __init__(self, application, request, **kwargs):
        super(AddHeaderRequestHandler,self).__init__(application, request, **kwargs)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_status(200)
    def write(self, **chunk):
        try:
            response = fdumps(chunk, self.get_status(), self.request.method)
            super(AddHeaderRequestHandler, self).write(response)
        except Exception,e:
            self.write_error(503, message='Server Internal Error [{}]'.format(traceback.format_exc()))
    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        kwargs['uri']=self.request.uri
        self.write(**kwargs)

class Error(AddHeaderRequestHandler):
    def get(self, *args, **kwargs):
        self.write_error(404, message='No such api [{}]'.format(self.request.uri))

class Index(AddHeaderRequestHandler, object):
    def get(self):
        self.write(message="""Welcome to autop rest api.""")

class Assets(AddHeaderRequestHandler, object):
    def get(self, **kwargs):
        get_items = dict(host           = self.get_host,
                         hostgroup      = self.get_hostgroup,
                         project        = self.get_project)

        if len(kwargs['item']):
            try:
                get_items[kwargs['item']]()
            except Exception,e:
                if isinstance(e,KeyError):
                    self.write_error(404, messages='No such item [{}]'.format(kwargs['item']),module='assets')
                else:
                    self.write_error(503, message='Server Internal Error [{}]'.format(traceback.format_exc()))
        else:
            self.get_base()

    def get_base(self):
        self.write(message='assets module')

    def get_host(self, isreturn = 0):
        sql = """SELECT
                    `host`.id                 AS 'id',
                    `host`.ip_addr            AS 'ip_addr',
                    `hosttype`.name           AS 'type',
                    `hostgroup`.name          AS 'group'
                FROM
                    t_assets_host             AS `host`
                LEFT JOIN t_assets_hosttype   AS `hosttype` ON (`host`.type_id    = `hosttype`.id)
                LEFT JOIN t_assets_hostgroup  AS `hostgroup` ON (`host`.group_id  = `hostgroup`.id)"""

        response = dict(host=mysql_query(sql))
        if isreturn:
            return response
        self.write(**response)

    def get_hostgroup(self, isreturn = 0):
        sql = """SELECT * FROM `t_assets_hostgroup`"""
        response = dict(hostgroup=mysql_query(sql))
        if isreturn:
            return response
        self.write(**response)

    def get_project(self, isreturn = 0):
        sql = """SELECT * FROM `t_assets_project`"""
        response = dict(project=mysql_query(sql))
        if isreturn:
            return response
        self.write(**response)

class Deploy(AddHeaderRequestHandler, object):
    #################
    # get方法
    #################
    def get(self, **kwargs):
        get_items = dict(template       = self.get_template,
                         task           = self.get_task)

        if len(kwargs['item']):
            try:
                get_items[kwargs['item']]()
            except Exception, e:
                if isinstance(e, KeyError):
                    self.write_error(404, messages='No such item [{}]'.format(kwargs['item']), module='deploy')
                else:
                    self.write_error(503, message='Server Internal Error [{}]'.format(traceback.format_exc()))
        else:
            self.get_base()

    #################
    # put方法
    #################
    def put(self, *args, **kwargs):
        put_item = dict(task = self.put_task)

        if len(kwargs['item']):
            try:
                put_item[kwargs['item']](*args, **kwargs)
            except Exception,e:
                if isinstance(e, KeyError):
                    self.write_error(404, messages='No such api [{}]'.format(self.request.uri), module='deploy')
        else:
            self.write_error(404, messages='No such api [{}]'.format(self.request.uri), module='deploy')

    #################
    # get 子 方法
    #################
    def get_base(self):
        self.write(message='deploy module')
        time.sleep(3)
        self.write(message='deploy module')

    def get_template(self, isreturn = 0):
        sql_hostgroup = """SELECT
                            template.`id` AS template_id,
                            project.`name` AS project_name,
                            template.`deploy_method`,
                            hostgroup.`name` AS `hostgroup_name`,
                            template.`deploy_path`
                        FROM
                            t_deploy_template AS template
                        LEFT JOIN t_assets_hostgroup AS hostgroup ON template.infrastructure_id = hostgroup.id
                        LEFT JOIN t_assets_project AS project ON template.project_id = project.id
                        WHERE template.deploy_method = 'hostgroup'"""
        sql_host = """SELECT
                                template.`id` AS template_id,
                                project.`name` AS project_name,
                                template.`deploy_method`,
                                host.`ip_addr` AS `host_name`,
                                template.`deploy_path`
                        FROM
                                t_deploy_template AS template
                        LEFT JOIN t_assets_host AS host ON template.infrastructure_id = host.id
                        LEFT JOIN t_assets_project AS project ON template.project_id = project.id
                        WHERE template.deploy_method = 'host'"""
        response = dict(template=[])
        response['template'].append(mysql_query(sql_hostgroup))
        response['template'].append(mysql_query(sql_host))

        if isreturn:
            return response
        self.write(**response)

    def get_task(self, isreturn=0):
        sql = """SELECT
                            task.`id`,
                            template.`name` AS templte_name,
                            project.`name` AS project_name,
                            task.`create_time`,
                            task.`create_user`,
                            task.`start_time`,
                            task.`start_user`,
                            task.`finish_time`,
                            task.`finish_status`
                        FROM
                            t_deploy_task AS task
                        LEFT JOIN t_deploy_template AS template ON task.template_id = template.id
                        LEFT JOIN t_assets_project AS project ON template.project_id = project.id"""

        response = dict(task=mysql_query(sql))

        if isreturn:
            return response
        self.write(**response)

    #################
    # put 子 方法
    #################
    def put_task(self, *args, **kwargs):
        if not len(kwargs['method']):
            try:
                sql = "INSERT INTO `t_deploy_task` (`template_id`, `create_time`, `create_user`) VALUES (%s, %s, 'admin')"
                db.insert(sql, self.request.arguments['template_id'][0], getLocaltime())
                self.write(message = 'Create new task with template id {} OK.'.format(self.request.arguments['template_id'][0]))
            except:
                traceback.print_exc()
                self.write_error(503, message='Server Internal Error [{}]'.format(traceback.format_exc()))
        else:
            print kwargs['method']

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()