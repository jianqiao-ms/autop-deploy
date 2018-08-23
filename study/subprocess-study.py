#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from tornado.process import Subprocess
from tornado.ioloop import IOLoop
import subprocess
import shlex
import sys
from tornado.iostream import StreamClosedError

# Local Packages

# CONST

# Class&Function Defination



async def fsub():
    p = Subprocess(shlex.split('ping -c 10 baidu.com'),stdin=None, stdout=Subprocess.STREAM, stderr=subprocess.STDOUT, universal_newlines=True)

    try:
        a = await p.stdout.read_until(b'\n')
        sys.stdout.write(a.decode())
        while True :
            if p.stdout._read_buffer_size==0:
                break
            a = await p.stdout.read_until(b'\n')
            sys.stdout.write(a.decode())
    except StreamClosedError as e:
        pass



async def fprocess():
    ioloop = IOLoop.instance()
    rst = subprocess.PIPE
    pipe = subprocess.Popen(shlex.split('ping -c 10 baidu.com'),stdin=None, stdout=rst, stderr=subprocess.STDOUT, close_fds=True)
    fd = pipe.stdout.fileno()

    # try:
    def recv(*args):
        data = pipe.stdout.readline()
        if data:
            print(data)
        elif pipe.poll() is not None:
            ioloop.remove_handler(fd)

    ioloop.add_handler(fd, recv, ioloop.READ)


# Logic
if __name__ == '__main__':

    IOLoop.instance().run_sync(fsub)
    IOLoop.instance().start()
