#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import logging

# 3rd-party Packages

# Local Packages
from api.classes import BaseRequestHandler
from classes import BaseWebSocketHandler

# CONST

# Class&Function Defination
class SSHSessionRecorderViewHandler(BaseRequestHandler):
    """Handler for a terminal websocket"""
    def get(self):
        self.render('webcrt/record.html')

class SSHSessionRecorderSocketHandler(BaseWebSocketHandler):
    """Handler for a terminal websocket"""
    def open(self, *args: str, **kwargs: str):
        with open('record','rb') as self.record:
            self.write_message(self.record.read())

    def on_close(self):
        logging.info('websocket closed')
        self.record.close()

# Logic
if __name__ == '__main__':
    pass
