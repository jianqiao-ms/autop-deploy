#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import os.path
import logging
import json
import sys
import asyncio
# 3rd-party Packages
import paramiko
import asyncssh
from tornado.platform.asyncio import IOLoop
from tornado.iostream import BaseIOStream, IOStream, PipeIOStream

# Local Packages
from classes.req_handler import UIRequestHandler
from classes.req_handler import BaseWebSocketHandler

from classes.time_generator import timestamp_millisecond

# CONST
ssh_args = dict(
    host = '192.168.3.9',
    port=22,
    username='root',
    password=' '
)

# Class&Function Defination
class A(asyncssh.SSHClientProcess):
    def data_received(self, data, datatype):
        sys.stdout.write(data)
        
class SSHConnectorViewHandler(UIRequestHandler):
    """
    ssh_connector UI
    """
    def get(self):
        self.render("ssh_connector/login.html")
        
class SSHConnectorSocketHandler(BaseWebSocketHandler):
    """Handler for a terminal websocket"""
    async def open(self, *args: str, **kwargs: str):
        conn = await asyncssh.connect('192.168.3.9', username='root', password=' ')
        self.process = await conn.create_process(term_type='xterm-color')
        self.process.data_received = self.send_stream
        self.process.eof_received = self.close
        self.record = open('record', 'wb')

    def send_stream(self, data, event):
        try:
            self.write_message({
                'type':'stdout',
                'data' : data
            })
            self.record.write(('timestamp' + str(timestamp_millisecond()) + data + 'endtimestamp\n').encode())
            # self.record.write(data)
        except:
            import traceback
            traceback.print_exc()
            IOLoop.current().stop()
            
    async def on_message(self, message):
        msg_object = json.loads(message)
        if msg_object['type'] == 'stdin':
            self.process.stdin.write(msg_object['data'])
        if msg_object['type'] == 'resize':
            self.process.change_terminal_size(*msg_object['data'])
        
    def on_close(self):
        logging.info('websocket closed')
        self.record.close()


class SSHConnectorParamikoSocketHandler(BaseWebSocketHandler):
    """Handler for a terminal websocket"""

    def open(self, *args: str, **kwargs: str):
        ssh_args = dict(
            hostname='192.168.3.9',
            port=22,
            username='root',
            password=' ',
            timeout=2
        )
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**ssh_args)

        self.pty = client.invoke_shell()
        IOLoop.current().add_handler(self.pty, self.send_stream, IOLoop.READ)
        self.record = open('record','wb')
   
    def send_stream(self, chan, e):
        try:
            data = chan.recv(8).decode()
            self.write_message({
                'type': 'stdout',
                'data': data
            })
            logging.info(data)
            self.record.write(data)
        except:
            import traceback
            traceback.print_exc()
            IOLoop.current().stop()

    def on_message(self, message):
        msg_object = json.loads(message)
        if msg_object['type'] == 'stdin':
            self.pty.send(msg_object['data'])
            # self.record.write(msg_object['data'].decode())
        if msg_object['type'] == 'resize':
            self.pty.resize_pty(*msg_object['data'])
    
    def on_close(self):
        logging.info('websocket closed')
        self.record.close()

# Logic
if __name__ == '__main__':
    pass