#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from handler.view.CD.cd import CDViewHandler
# CONST

# Class&Function Defination
route = list(map(
    lambda x:(x.route(), x),
    [
        CDViewHandler,
    ]
))

# Logic
if __name__ == '__main__':
    pass
