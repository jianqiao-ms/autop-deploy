#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os, sys
import shlex
import subprocess

# 3rd-party Packages
import tornado.web
from tornado.process import Subprocess
from tornado.options import parse_command_line
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError

# Local Packages

# CONST

# Class&Function Defination
def fsub():
    p = Subprocess(shlex.split('ping -c 10 baidu.com'),stdin=None, stdout=Subprocess.STREAM, stderr=subprocess.STDOUT, universal_newlines=True)
    fd = p.stdout.fileno()

    def recv(*args):
        data = p.stdout.read_until(b'\n')
        if data:
            print(data.result().decode())
        elif p.proc.poll() is not None:
            IOLoop.current().remove_handler(fd)

    IOLoop.current().add_handler(fd, recv, IOLoop.current().READ)

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        # p = Subprocess(shlex.split('ping -c 10 baidu.com'), stdin=None, stdout=Subprocess.STREAM,
        #                stderr=subprocess.STDOUT, universal_newlines=True)

        p = Subprocess(shlex.split("ping -c 10 baidu.com"), stdin=Subprocess.STREAM, stdout=Subprocess.STREAM,
                                         stderr=Subprocess.STREAM)
        IOLoop.instance().add_handler(p.stdout, self.transfer, IOLoop.READ)

        await p.stdout.read_until_close()

    def transfer(self, fd, events):
        # try:
        #     a = fd.read_until(b'\n')
        #     rst = a.result().decode().replace('\n', '<br />')
        #
        # except tornado.iostream.StreamClosedError:
        #     print('ERROR')
        a = fd.read_bytes(128)
        rst = a.result().decode().replace('\n', '<br />')
        self.write(rst)
        self.flush()


        # try:
        #     a = await p.stdout.read_until(b'\n')
            # self.write(a.decode())
            # self.flush()
            # while True:
                # if p.stdout._read_buffer_size == 0:
                #     break
                # a = await p.stdout.read_until(b'\n')
                # self.write(a.decode())
                # self.flush()
        # except StreamClosedError as e:
        #     import traceback
        #     traceback.print_exc()
        #     self.finish()

class AsyncHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish('aysnc')

class AjaxHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("base.html")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

# Logic
if __name__ == "__main__":
    parse_command_line()
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "study-template")
    }

    parse_command_line()
    application = Application([
        ('/', MainHandler),
        ('/aysnc', AsyncHandler),
    ], **settings)

    application.listen(60000)
    IOLoop.current().start()