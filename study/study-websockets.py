#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os, sys
import shlex
import subprocess
import select
import asyncio
# 3rd-party Packages
import paramiko

import tornado.web
import tornado.websocket
from tornado.process import Subprocess
from tornado.options import parse_command_line
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError

# Local Packages

# CONST
desc_proxy = dict(
    hostname = '192.168.3.34',
    port = 22,
    username = 'root',
    password = ' ',
    timeout = 2
)

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
    @asyncio.coroutine
    def get(self):
        p = Subprocess(shlex.split('ping -c 10 baidu.com'), stdin=None, stdout=Subprocess.STREAM,
                       stderr=subprocess.STDOUT, universal_newlines=True)
        try:
            a = yield from p.stdout.read_until(b'\n')
            self.write(a.decode())
            self.flush()
            while True:
                a = yield p.stdout.read_until(b'\n')
                self.write(a.decode())
                self.flush()
        except StreamClosedError as e:
            import traceback
            traceback.print_exc()
            self.finish()

class StaticHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('static.html')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('tty.html')

class SockMainHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        proxy = paramiko.SSHClient()
        proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        proxy.connect(**desc_proxy)

        self.shell = proxy.invoke_shell()
        IOLoop.current().add_handler(self.shell,self.recv, IOLoop.READ)

    def recv(self, *args):
        a = self.shell.recv(128)
        self.write_message(a)

    def on_message(self, message):
        self.shell.send(message)

    def on_close(self):
        self.shell.close()
        print("WebSocket closed")

# Logic
if __name__ == "__main__":
    parse_command_line()
    settings = {
        'login_url': '/login',
        'template_path': os.path.join(os.path.dirname(__file__), "study-template"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    parse_command_line()
    application = Application([
        ('/', IndexHandler),
        ('/static', StaticHandler),
        ('/websocket', SockMainHandler),
    ], **settings)

    application.listen(60000)
    IOLoop.current().start()