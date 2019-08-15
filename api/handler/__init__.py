
from cmdb import *
from webcrt import *

route = [
    (r"/api/cmdb/label", CMDBLabelHandler),
    (r"/websocket", SSHConnectorSocketHandler),
]