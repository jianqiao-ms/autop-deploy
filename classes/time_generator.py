#! /usr/bin/env python
# -* coding: utf-8 -*

# Official packages
import time

# 3rd-party Packages

# Local Packages

# CONST

def timestamp_millisecond():
    return int(time.time() * 1000)

# Class&Function Defination



# Logic
if __name__ == '__main__':
    print(timestamp_millisecond())