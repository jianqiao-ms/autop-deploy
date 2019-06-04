__all__ = ["route"]

from .api import *
from .view import *

route = [
    # (r"/api/v1/gitlab/jobscripts", gitlab.CIScriptGenerator),
    # (r"/api/v1/gitlab/receiver", gitlab.CIArtifactReceiver)
    (r"/", ssh_connector.SSHConnectorViewHandler),
    (r"/websocket", ssh_connector.SSHConnectorSocketHandler),
    (r"/record", ssh_connector.SSHSessionRecorderViewHandler),
    (r"/recordwebsocket", ssh_connector.SSHSessionRecorderSocketHandler),
    # (r"/websocket", ssh_connector.SSHConnectorParamikoSocketHandler)
]