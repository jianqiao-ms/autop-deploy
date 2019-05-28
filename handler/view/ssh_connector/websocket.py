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
from tornado.ioloop import IOLoop
from tornado.iostream import BaseIOStream, IOStream, PipeIOStream
# Local Packages
from classes.req_handler import BaseWebSocketHandler


# CONST
ssh_args = dict(
    host = '192.168.3.9',
    port=22,
    username='root',
    password=' '
)

# Class&Function Defination
def make_call_back(sock):
    def a(data, datatype):
        sock.send_stream(data)
    return a
        
class SSHConnectorSocketHandler(BaseWebSocketHandler):
    """Handler for a terminal websocket"""
    async def open(self, *args: str, **kwargs: str):
        inr, inw = os.pipe()
        INPUT_r = PipeIOStream(inr)
        INPUT = PipeIOStream(inw)

        outr, outw = os.pipe()
        OUTPUT = PipeIOStream(outr)
        OUTPUT_w = PipeIOStream(outw)
        
        self.process = await self.new_channel()
        self.process.redirect(stdin=INPUT_r, stdout=OUTPUT_w, stderr='STDOUT')
        

    async def new_channel(self):
        

        async with asyncssh.connect('192.168.3.9', username='root', password=' ', keepalive_interval=30) as conn:
            async with conn.create_process(term_size=(80, 24), term_type='xterm') as process:
                process.data_received = make_call_back(self)
                
                # await process.communicate('bash')
                
                return process
    
    def send_stream(self, data):
        try:
            self.write_message({
                'type':'stdout',
                'data' : data
            })
        except:
            import traceback
            traceback.print_exc()
            IOLoop.current().stop()
            
    def on_message(self, message):
        msg_object = json.loads(message)
        logging.info(msg_object)

        if msg_object['type'] == 'stdin': 
            self.process.stdin.write(msg_object['data'])
        if msg_object['type'] == 'resize':
            self.process.resize_pty(*msg_object['data'])

# Logic
if __name__ == '__main__':
    pass
