#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import sys
import random
# 3rd-party Packages
import paramiko
import select
# Local Packages

# CONST
ssh_args = dict(
    hostname='192.168.3.9',
    port=22,
    username='root',
    password=' ',
    timeout=2
)

# Class&Function Defination

def output(msg):
    sys.stdout.write(msg.decode())




if __name__ == '__main__':
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(**ssh_args)
    
    
    pty = client.invoke_shell()
    pty.sendall('ping 192.168.3.1\n')
    fd = pty.fileno()
    readable, _,_ = select.select([fd],[],[])
    while True:
        if readable:
            sys.stdout.write(pty.recv(1024).decode()) 