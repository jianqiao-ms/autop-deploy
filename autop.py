#!/usr/bin/python2.7
#-*- coding=utf-8 -*-

import shlex
from tornado.gen import coroutine, Task, Return
from tornado.process import Subprocess
from tornado.ioloop import IOLoop


@coroutine
def call_subprocess(cmd, stdin_data=None, stdin_async=True):
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

    if stdin_data:
        if stdin_async:
            yield Task(sub_process.stdin.write, stdin_data)
        else:
            sub_process.stdin.write(stdin_data)

    # if stdin_async or stdin_data:
    #     sub_process.stdin.close()
    #
    retcode, result, error = yield [
        sub_process.wait_for_exit(raise_error=False),
        Task(sub_process.stdout.read_until_close),
        Task(sub_process.stderr.read_until_close),
    ]

    raise Return((retcode, result.strip(), error.strip()))


@coroutine
def example_main():
    for cmd in ['git clone http://gitlab.shangweiec.com/shangwei/shangwei.gitlab.shangweiec.com.git']:
        retcode, stdout, stderr = yield call_subprocess(cmd)
        print('command: %s' % cmd)
        print('retcode: %s' % retcode)
        print('stdout: %s' % stdout)
        print('stderr: %s' % stderr)
        print('---')
    IOLoop.instance().stop()


if __name__ == "__main__":
    IOLoop.instance().add_callback(example_main)
    IOLoop.instance().start()