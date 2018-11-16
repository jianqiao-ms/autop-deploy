#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from handler.view.Inventory.Inventory import DashboardInventoryViewHandler
from handler.view.Inventory.Inventory import DistrictInventoryViewHandler
from handler.view.Inventory.Inventory import HostInventoryViewHandler
from handler.view.Inventory.Inventory import HostgroupInventoryViewHandler
from handler.view.Inventory.Inventory import ProjectInventoryViewHandler
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
