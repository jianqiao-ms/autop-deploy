#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from tornado import gen
from tornado.web import stream_request_body

# Local Packages
from classes import RequestHandler

# CONST

# Class&Function Defination
@stream_request_body
class GitlabReceiver(RequestHandler):
    def prepare(self):
        self.fp = open(self.request.arguments['filename'][0], 'wb')

    def get(self):
        print(self.request.__dict__)
        self.finish()
    def post(self):
        for i in self.request.__dict__.items():
            print(i)
        self.finish()
    def put(self):
        self.fp.close()
        self.finish({"msg":"ok"})

    @gen.coroutine
    def data_received(self, chunk: bytes):
        self.fp.write(chunk)

    _route = "/api/v1/gitlab/receiver"


# Logic
if __name__ == '__main__':
    from tornado.ioloop import IOLoop
    from tornado.web import Application
    import tornado.options

    tornado.options.options.logging = None
    tornado.options.parse_command_line()
    application = Application([
        (GitlabReceiver._route, GitlabReceiver)
    ])
    application.listen(60000)
    IOLoop.current().start()
