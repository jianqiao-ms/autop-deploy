#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.escape
import torndb

import traceback

# 自定义方法，格式化返回数据
def fdumps(obj,status_code):
    if status_code >= 200 and status_code < 400:
        obj['status'] = 'OK'
    else:
        obj['status'] = 'ERROR'
    obj['status_code'] = status_code
    # return obj
    return json.dumps(obj, indent=4)
    # return tornado.escape.json_encode(obj)

# 返回tornad app对象
settings = dict(

)

def make_app():
    return tornado.web.Application([
        (r"/", Index),
        (r"^/assets(?P<path>/?)(?P<item>[A-Za-z]*)", Assets),
        (r"^/deploy(?P<path>/?)(?P<item>[A-Za-z]*)", Deploy),
        (r".*", Error)
    ], **settings)

# 继承RequestHandler的自定基础类
class AddHeaderRequestHandler(tornado.web.RequestHandler,object):
    def __init__(self, application, request, **kwargs):
        super(AddHeaderRequestHandler,self).__init__(application, request, **kwargs)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_status(200)
    def write(self, chunk):
        try:
            response = fdumps(chunk, self.get_status())
            super(AddHeaderRequestHandler, self).write(response)
        except Exception,e:
            self.write_error(503)
    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        kwargs['uri']=self.request.uri
        self.write(kwargs)

class Error(AddHeaderRequestHandler):
    def get(self, *args, **kwargs):
        self.write_error(404, message='No such api [{}]'.format(self.request.uri))

class Index(AddHeaderRequestHandler, object):
    def get(self):
        self.write(dict(message="""Welcome to autop rest api."""))

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
        self.write(dict(message='deploy module'))
        # self.write(dict(self.get_host(isreturn = 1), **self.get_project(isreturn = 1)))

    def get_host(self, isreturn = 0):
        # get_host_arguments = ['id', 'ip_addr', 'type', 'group']
        get_host_arguments = dict(id        = '`host`.id',
                                  ip_addr   = '`host`.ip_addr',
                                  type      = '`hosttype`.name',
                                  group     = '`hostgroup`.name')

        sql = """SELECT
                    `host`.id         AS 'id',
                    `host`.ip_addr    AS 'ip_addr',
                    `hosttype`.name   AS 'type',
                    `hostgroup`.name  AS 'group'
                FROM
                    t_assets_host AS `host`
                LEFT JOIN t_assets_hosttype AS hosttype ON `host`.type_id = hosttype.id
                LEFT JOIN t_assets_hostgroup AS hostgroup ON `host`.group_id = hostgroup.id"""

        append_where = False
        if len(self.request.arguments):
            for k in self.request.arguments:
                if k not in get_host_arguments.keys():
                    return self.write_error(503, message='no such attribute [{}] for host.'.format(k))
            append_where = True

        if append_where:
            sql = sql + ' WHERE '
            for arg in self.request.arguments:
                sql = sql + get_host_arguments[arg] + ' IN ({})'.format(self.request.arguments[arg][0])
                sql += ' and '

        print sql[:-5]

        # response = dict(host=db.query(sql))
        # if isreturn:
        #     return response
        # self.write(response)

    def get_hostgroup(self, isreturn = 0):
        sql = """SELECT * FROM `t_assets_hostgroup`"""
        response = dict(hostgroup=db.query(sql))
        if isreturn:
            return response
        self.write(response)

    def get_project(self, isreturn = 0):
        sql = """SELECT * FROM `t_assets_project`"""
        response = dict(project=db.query(sql))
        if isreturn:
            return response
        self.write(response)

class Deploy(AddHeaderRequestHandler, object):
    def get(self, **kwargs):
        print self.request.arguments

        get_items = dict(template       = self.get_template)

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

    def get_base(self):
        self.write(dict(message='deploy module'))

    def get_template(self, isreturn = 0):
        sql_hostgroup = """SELECT
                            template.id AS template_id,
                            project.`name` AS project_name,
                            template.deploy_method,
                            hostgroup.`name` AS `hostgroup_name`,
                            template.deploy_path
                        FROM
                            t_deploy_template AS template
                        LEFT JOIN t_assets_hostgroup AS hostgroup ON template.infrastructure_id = hostgroup.id
                        LEFT JOIN t_assets_project AS project ON template.project_id = project.id
                        WHERE template.deploy_method = 'hostgroup'"""
        sql_host = """SELECT
                                template.id AS template_id,
                                project.`name` AS project_name,
                                template.deploy_method,
                                host.`ip_addr` AS `host_name`,
                                template.deploy_path
                        FROM
                                t_deploy_template AS template
                        LEFT JOIN t_assets_host AS host ON template.infrastructure_id = host.id
                        LEFT JOIN t_assets_project AS project ON template.project_id = project.id
                        WHERE template.deploy_method = 'host'"""
        response = dict(template=[])
        response['template'].append(db.query(sql_hostgroup))
        response['template'].append(db.query(sql_host))

        if isreturn:
            return response
        self.write(response)

if __name__ == "__main__":
    try:
        db = torndb.Connection('192.168.0.195','autop','cupid','everyone2xhfz')
    except Exception,e:
        print e
        pass

    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()