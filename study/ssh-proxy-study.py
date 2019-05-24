#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import random
from socket import timeout
# 3rd-party Packages
import paramiko

# Local Packages

# CONST
desc_proxy = dict(
    hostname = '61.240.30.142',
    port = 60000,
    username = 'root',
    pkey = paramiko.RSAKey.from_private_key_file('/home/jianqiao/.key/jianqiao'),
    timeout = 2
)

desc_target = dict(
    hostname = '192.168.0.41',
    port = 22,
    username = 'root',
    timeout = 2
)

# Class&Function Defination
proxy = paramiko.SSHClient()
proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
proxy.connect(**desc_proxy )


proxy_transport = proxy.get_transport()
channel = proxy_transport.open_channel("direct-tcpip",
                                       ('192.168.0.49',22),
                                       ('127.0.0.1',1234))
remote_client = paramiko.SSHClient()
remote_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_client.connect('localhost',port=1234, sock=channel, username='root')


stdin, stdout, stderr = remote_client.exec_command('hostname')
print(stdout.readlines())
