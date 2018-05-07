#! /usr/bin/env python
#-* coding: utf-8 -*

# tornado packages

# system packages

# self packages
from .base import BaseHandler
from .base import authenticated

class MainHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('index.html')

# class PingHandler(BaseHandler):
#     async def get(self):
#         process = Subprocess(
#             shlex.split('ping -c 10 baidu.com'),
#             stdout=Subprocess.STREAM,
#             stderr=Subprocess.STREAM
#         )
#
#         while True:
#             line = await process.stdout.read_bytes(4)
#             sys.stdout.write(line.decode())
#             self.write(line.decode())
#             self.flush()