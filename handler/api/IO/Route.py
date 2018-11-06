#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from .District      import DistrictIOApiHandler
from .Host          import HostIOApiHandler
from .Host_group    import HostgroupIOApiHandler
from .Project       import ProjectIOApiHandler
# CONST

# Class&Function Defination
route = list(map(
    lambda x:(x.route, x), [
        DistrictIOApiHandler,
        HostIOApiHandler,
        HostgroupIOApiHandler,
        ProjectIOApiHandler
    ]
))
# Logic
if __name__ == '__main__':
    pass
