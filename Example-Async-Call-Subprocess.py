#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import tornado.ioloop
import tornado.web
import shlex
from tornado.gen import coroutine, Task, Return
from tornado.process import Subprocess
from tornado.ioloop import IOLoop



async def call_subprocess(cmd, stdin_data=None, stdin_async=True):
    """call sub process async
        Args:
            cmd: str, commands
            stdin_data: str, data for standard in
            stdin_async: bool, whether use async for stdin
    """
    try:
        sub_process = Subprocess(shlex.split(cmd),
                                 stdin=None,
                                 stdout=Subprocess.STREAM,
                                 stderr=Subprocess.STREAM,)
    except OSError as err:
        raise Return((err.errno, '', err.strerror))

    retcode, result, error = yield [
        sub_process.wait_for_exit(raise_error=False),
        Task(sub_process.stdout.read_until_close),
        Task(sub_process.stderr.read_until_close),
    ]

    raise Return((retcode, result.strip(), error.strip()))

class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        _STREAM = Subprocess.STREAM
        _SUBPROCESS = Subprocess(shlex.split('git clone http://gitlab.shangweiec.com/shangwei/shangwei.gitlab.shangweiec.com.git'),
                                 stdin=None,
                                 stdout=_STREAM,
                                 stderr=_STREAM)

        stdout = await _SUBPROCESS.stderr.read_until('\n')

        while not _SUBPROCESS.closed():
            self.write(stdout)
            self.flush()

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()