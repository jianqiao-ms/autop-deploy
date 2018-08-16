#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os

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


proxy_channel = proxy_transport.open_channel(kind="forwarded-tcpip",dest_addr=('192.168.0.41',22), src_addr=('192.168.2.200',11111))

print(proxy_channel)



target = paramiko.SSHClient()
target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target.connect(sock=proxy_channel, **desc_target)
stdin, stdout, stderr = target.exec_command('hostname')
print(stdout.read())


# Logic
# if __name__ == '__main__':
#     stdin, stdout, stderr = target.exec_command('hostname')
#     print(stdout.read())

