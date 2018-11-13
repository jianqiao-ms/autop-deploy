#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from handler.view.CI.ci import CIViewHandler
# CONST

# Class&Function Defination
route = list(map(
    lambda x:(x.route(), x),
    [
        CIViewHandler,
    ]
))

# Logic
if __name__ == '__main__':
    pass
