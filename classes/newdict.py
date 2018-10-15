#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages

# CONST

# Class&Function Defination
class NewDict(dict):
    def __getattr__(self, item):
        return self.get(item)
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

# Logic
