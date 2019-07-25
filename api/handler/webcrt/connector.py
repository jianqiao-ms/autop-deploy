#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import logging
import json
import sys
import traceback

# 3rd-party Packages
import paramiko
import asyncssh
from tornado.platform.asyncio import IOLoop
from tornado.websocket import WebSocketHandler

# Local Packages
from api.classes import BaseWebSocketHandler
from time_generator import timestamp_millisecond

# CONST

# Class&Function Defination
class SSHConnectorSocketHandler(WebSocketHandler):
    """Handler for a terminal websocket"""
    def check_origin(self, origin):
        return True
    def open(self):
        logging.info('websocket opened')
    def send_stream(self, data, event):
        logging.info(data)
        try:
            self.write_message({
                'type':'stdout',
                'data' : data
            })
            self.record.write(('timestamp' + str(timestamp_millisecond()) + data + 'endtimestamp\n').encode())
        except:
            import traceback
            traceback.print_exc()
            IOLoop.current().stop()
        
    async def create_process(self, host, user, password, port=22):
        conn = await asyncssh.connect(host=host, username=user, password=password, port=int(port),known_hosts = None)
        self.process = await conn.create_process(term_type='xterm-color')
        self.process.data_received = self.send_stream
        self.process.eof_received = self.close
        self.record = open('record', 'wb')
        return self.process
            
    async def on_message(self, message):
        msg_object = json.loads(message)
        logging.info(msg_object)
        if msg_object['type'] == 'conn':
            try:
                self.process = await self.create_process(**msg_object['data'])
                await self.write_message({
                    'type' : 'conn',
                    'data' : {
                        'status': True,
                        'details' : ''
                    }
                })
            except:
                await self.write_message({
                    'type': 'conn',
                    'data': {
                        'status': False,
                        'details': traceback.print_exc()
                    }
                })
                self.close()
        elif msg_object['type'] == 'stdin':
            self.process.stdin.write(msg_object['data'])
        elif msg_object['type'] == 'resize':
            self.process.change_terminal_size(*msg_object['data'])
        
    def on_close(self):
        logging.info('websocket closed')
        try:
            self.record.close()
        except:
            pass

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