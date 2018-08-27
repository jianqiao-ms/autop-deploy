#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
try:
    from urllib.parse import unquote
except ImportError:
    # Python 2.
    from urllib import unquote

# 3rd-party Packages
import tornado.web
import logging
# Local Packages

# CONST

# Class&Function Defination
@tornado.web.stream_request_body
class UploadHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bytes_read = 0
        self.file = open('a', 'wb')

    def data_received(self, chunk):
        self.file.write(chunk)

    def post(self, *args, **kwargs):
        print(args)
        print(kwargs)
        self.file.close()
        filename = unquote(args)
        mtype = self.request.headers.get('Content-Type')
        logging.info('PUT "%s" "%s" %d bytes', filename, mtype, self.bytes_read)
        self.write('OK')

# Logic
if __name__ == '__main__':
    pass
