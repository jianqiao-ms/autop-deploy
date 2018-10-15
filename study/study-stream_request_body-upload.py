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
        self.meta = dict()
        self.receiver = self.get_receiver()

    # def prepare(self):
    """If no stream_request_body"""
    #     self.request.connection.set_max_body_size(MAX_STREAMED_SIZE)

    def data_received(self, chunk):
        self.receiver(chunk)

    def get_receiver(self):
        index = 0
        SEPARATE = b'\r\n'

        def receiver(chunk):
            nonlocal index
            if index == 0:
                index +=1
                split_chunk             = chunk.split(SEPARATE)
                self.meta['boundary']   = SEPARATE + split_chunk[0] + b'--' + SEPARATE
                self.meta['header']     = SEPARATE.join(split_chunk[0:3])
                self.meta['header']     += SEPARATE *2
                self.meta['filename']   = split_chunk[1].split(b'=')[-1].replace(b'"',b'').decode()

                chunk = chunk[len(self.meta['header']):] # Stream掐头
                import os
                self.fp = open(os.path.join('upload',self.meta['filename']), "wb")
                self.fp.write(chunk)
            else:
                self.fp.write(chunk)
        return receiver

    def post(self, *args, **kwargs):
        # Stream去尾
        self.meta['content_length'] = int(self.request.headers.get('Content-Length')) - \
                                      len(self.meta['header']) - \
                                      len(self.meta['boundary'])

        self.fp.seek(self.meta['content_length'], 0)
        self.fp.truncate()
        self.fp.close()
        self.finish('OK')

# Logic
if __name__ == '__main__':
    pass
