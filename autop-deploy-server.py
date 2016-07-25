#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.gen
import gevent.wsgi
import time
import tornado.httpserver
import torndb

def fdumps(obj,status_code=200):
    if status_code == 200:
        obj['status'] = 'OK'
    else:
        obj['status'] = 'ERROR'
    obj['status_code'] = status_code
    return json.dumps(obj, indent=4)

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
            self.write_error(503, message='ERROR occur during formatting response object')
    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        kwargs['uri']=self.request.uri
        self.write(kwargs)

class Error(AddHeaderRequestHandler):
    def get(self, *args, **kwargs):
        self.write_error(404, message='No such api [{}]'.format(self.request.uri))

class Index(AddHeaderRequestHandler):
    def get(self):
        self.write(dict(message='Welcome to autop rest api.'))

class Assets(AddHeaderRequestHandler):
    def get(self, **kwargs):
        get_items = dict(host = self.get_host)

        if kwargs['item']:
            try:
                get_items[kwargs['item']]()
            except:
                self.write_error(404,   message='No such item [{}]'.format(kwargs['item']),
                                        module='assets')
        else:
            self.get_base()

    def get_base(self):
        self.write(dict(message='assets module'))

    def get_host(self, isreturn = 0):
        sql = """SELECT
                    `host`.ip_addr,
                    `hosttype`. NAME AS 'type',
                    `hostgroup`. NAME AS 'group'
                FROM
                    t_assets_host AS `host`
                LEFT JOIN t_assets_hosttype AS hosttype ON `host`.type_id = hosttype.id
                LEFT JOIN t_assets_hostgroup AS hostgroup ON `host`.group_id = hostgroup.id"""
        response = dict(host=db.query(sql))
        if isreturn:
            return response
        self.write(response)

    def get_project(self, isreturn = 0):
        response = dict(host=db.query('SELECT * FROM `t_assets_project`'))
        if isreturn:
            return response

application = tornado.web.Application([
# application = tornado.wsgi.WSGIApplication([
    (r"/", Index),
    (r"^/assets(?P<path>/?)(?P<item>[A-Za-z]*)",Assets),
    (r".*", Error)
])

if __name__ == "__main__":
    # server = gevent.wsgi.WSGIServer(('', 8888), application)
    # server.serve_forever()

    try:
        # db = mysql.connector.connect(**dbConfig)
        # cursor = db.cursor()
        db = torndb.Connection('192.168.0.195','autop','cupid','everyone2xhfz')
    except Exception,e:
        print e
        pass

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

    # server = tornado.httpserver.HTTPServer(application)
    # server.bind(8888)
    # server.start(0)  # Forks multiple sub-processes
    # tornado.ioloop.IOLoop.current().start()