#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from .Dashboard     import DashboardInventoryViewHandler
from .District      import DistrictInventoryViewHandler
from .Host          import HostInventoryViewHandler
from .Host_group    import HostgroupInventoryViewHandler
from .Project       import ProjectInventoryViewHandler
# CONST

# Class&Function Defination
route = list(map(
    lambda x:(x.route(), x),
    [
        DashboardInventoryViewHandler,
        DistrictInventoryViewHandler,
        HostInventoryViewHandler,
        HostgroupInventoryViewHandler,
        ProjectInventoryViewHandler
    ]
))

# Logic
if __name__ == '__main__':
    pass
