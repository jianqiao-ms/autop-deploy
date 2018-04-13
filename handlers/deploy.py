#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages
from tornado.web import escape
from tornado.websocket import WebSocketHandler
from tornado.process import Subprocess

# system packages
import os
import shlex

# self packages
from handlers.base import BaseHandler
from handlers.base import authenticated
from handlers.base import async_authenticated


class DeployActionHandler(BaseHandler):
    async def get(self):
        # _gitlab_id = self.get_query_argument('gitlab_id', False)
        # _gitlab_id = 39
        # _commit = self.get_query_argument('commit', False)
        # _project = self.db_sesion.query(self.schema.project).filter(self.schema.project.gitlab_id == _gitlab_id).one()

        os.chdir('/home/jianqiao/Workspace/autop/tmp')
        # os.chdir('/home/jianqiao/Workspace/autop/tmp/position_manager')

        process = Subprocess(
                        # shlex.split('git log'),
                        # shlex.split('git clone git@192.168.3.252:wangchengyang/position_manager.git'),
                        shlex.split('ping -c 10 baidu.com'),
                        stdout=Subprocess.STREAM,
                        stderr=Subprocess.STREAM
                    )

        import sys
        import tornado.iostream
        # print(process.returncode)

        # while True:
        #     print(process.returncode)
        #
        #     out = await process.stdout.read_until(b'\n')
        #     err = await process.stderr.read_until(b'\n')
            # sys.stdout.write(out.decode())
            # sys.stdout.flush()

        # ret = await process.wait_for_exit(raise_error=False)
        # print(ret)

        try:
            while True:
                out = await process.stdout.read_until(b'\n')
                # out = await process.stderr.read_until(b'\n')
                # err = await process.stderr.read_until(b'\n')
                sys.stdout.write(out.decode())
                self.write(out.decode() + '<br />')
                self.flush()
                sys.stdout.flush()
        except tornado.iostream.StreamClosedError as e:
            pass
            # except:
            #     traceback.print_exc()
            #     print(out.decode())
            #     print(out)

        # while process.returncode != None:
        #     print(out)

        # for data in out:
        #     self.write(data)
        self.finish('Deployaction done!')

class Test2Handler(BaseHandler):
    def get(self, *args, **kwargs):
        TestHandler.write_message(message='asd')

class TestHandler(WebSocketHandler):
    clients =  []
    def open(self, *args, **kwargs):
        self.clients.append('1')
    def on_message(self, message):
        print('get msg {}'.format(message))
        print(self.clients)
