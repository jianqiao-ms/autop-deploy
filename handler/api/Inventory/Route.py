#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from .District      import DistrictInventoryApiHandler
from .Host          import HostInventoryApiHandler
from .Host_group    import HostgroupInventoryApiHandler
from .Project       import ProjectInventoryApiHandler
# CONST

# Class&Function Defination
route = list(map(
    lambda x:(x.route(), x),
    [
        DistrictInventoryApiHandler,
        HostInventoryApiHandler,
        HostgroupInventoryApiHandler,
        ProjectInventoryApiHandler
    ]
))

# Logic
if __name__ == '__main__':
    pass
