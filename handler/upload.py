#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import sys
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
MB = 1024 * 1024
GB = 1024 * MB
TB = 1024 * GB
MAX_STREAMED_SIZE = 16*GB

# Class&Function Defination
@tornado.web.stream_request_body
class UploadHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bytes_read = 0
        self.filename = None
        self.receiver = self.get_receiver()

    def prepare(self):
        self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def data_received(self, chunk):
        self.receiver(chunk)
        # self.bytes_read += len(chunk)
        # self.file.write(chunk)
        # print(type(chunk))
        # print(chunk)
        # return 0
        # print(chunk)
        # print('\r\n=============================\n\n\n\n\n')

    def get_receiver(self):
        index = 0
        def receiver(chunk):
            nonlocal index
            if index == 0:
                split_chunk = chunk.split(b'\r\n')
                self.filename = split_chunk[1].split(b'=')[-1].replace(b'"',b'').decode()
                data = split_chunk[4]

                import os
                self.fp = open(os.path.join('upload',self.filename), "wb")
                self.fp.write(data)
            else:
                self.fp.write(chunk)
            index+=1
        return receiver

    def post(self, *args, **kwargs):
        self.fp.close()
        self.finish('OK')



# Logic
if __name__ == '__main__':
    pass
