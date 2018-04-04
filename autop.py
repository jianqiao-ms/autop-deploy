#! /usr/bin/env python
#-* coding: utf-8 -*
# DZf_HJFdxeVzQorkQhMo

import tornado.ioloop
import tornado.web
import tornado.gen
import tornado.concurrent
import functools
from concurrent.futures import ThreadPoolExecutor
from tornado.options import parse_command_line
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class SyncHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        # 耗时的代码
        os.system("ping -c 2 www.baidu.com")
        self.finish('It works')

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        tornado.ioloop.IOLoop.instance().add_timeout(1, callback=functools.partial(self.ping, 'www.google.com'))

        # do something others
        self.finish('It works')

    @tornado.gen.coroutine
    def ping(self, url):
        os.system("ping -c 2 {}".format(url))
        return 'after'


class AsyncTaskHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # yield 结果
        response = yield tornado.gen.Task(self.ping, ' www.google.com')
        print('response', response)
        self.finish('hello')

    @tornado.gen.coroutine
    def ping(self, url):
        os.system("ping -c 10 {}".format(url))
        return 'after'

class FutureHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):

        url = 'www.google.com'
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.ping, url))
        self.finish('It works')

    @tornado.concurrent.run_on_executor
    def ping(self, url):
        os.system("ping -c 100 {}".format(url))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/sync", SyncHandler),
        (r"/async", AsyncHandler),
        (r"/asynctask", AsyncTaskHandler),
        (r"/asyncfuture", FutureHandler),
    ])

if __name__ == "__main__":
    parse_command_line()
    app = make_app()
    app.listen(60000)
    tornado.ioloop.IOLoop.current().start()