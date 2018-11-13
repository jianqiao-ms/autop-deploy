#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages

# Local Packages
from handler.view.Inventory.Dashboard import DashboardInventoryViewHandler
from handler.view.Inventory.District import DistrictInventoryViewHandler
from handler.view.Inventory.Host import HostInventoryViewHandler
from handler.view.Inventory.Host_group import HostgroupInventoryViewHandler
from handler.view.Inventory.Project import ProjectInventoryViewHandler
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
