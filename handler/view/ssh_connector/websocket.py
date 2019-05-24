#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import os.path
import logging
import json
import sys

# 3rd-party Packages
import paramiko
from tornado.ioloop import IOLoop
# Local Packages
from classes.req_handler import BaseWebSocketHandler


# CONST
ssh_args = dict(
    hostname='192.168.3.9',
    port=22,
    username='root',
    password=' ',
    timeout=2
)

# Class&Function Defination
class SSHConnectorSocketHandler(BaseWebSocketHandler):
    """Handler for a terminal websocket"""
    def open(self, *args: str, **kwargs: str):
        self.channel = self.new_channel()
        
        IOLoop.current().add_handler(self.channel, self.send_asd, IOLoop.current().READ)
    
    def new_channel(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**ssh_args)
        return client.invoke_shell()
    
    def send_asd(self, fd, events):
        try:
            if fd.closed:
                self.close()
                return 0
            a = fd.recv(1024)
            sys.stdout.write(a.decode())
            self.write_message(a)
        except:
            import traceback
            traceback.print_exc()
            IOLoop.current().stop()
            
    def on_message(self, message):
        self.channel.send(message)

# Logic
if __name__ == '__main__':
    pass
