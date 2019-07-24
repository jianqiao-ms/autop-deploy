#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import sys
import random
# 3rd-party Packages
import paramiko

# Local Packages

# CONST
desc_proxy = dict(
    hostname = '192.168.3.9',
    port = 22,
    username = 'root',
    password = ' ',
    timeout = 2
)

# Class&Function Defination
proxy = paramiko.SSHClient()
proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
proxy.connect(**desc_proxy )

a = proxy.invoke_shell()
a.sendall('ip a')
rst = a.recv(4096)
sys.stdout.write(rst.decode())

proxy.close()

from tornado.ioloop import IOLoop
print(IOLoop.READ)
print(IOLoop.WRITE)
print(IOLoop.ERROR)