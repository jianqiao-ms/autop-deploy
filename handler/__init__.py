__all__ = ["route"]

from .api import *
from .view import *

route = [
    (r"/api/v1/gitlab/jobscripts", gitlab.CIScriptGenerator),
    (r"/api/v1/gitlab/receiver", gitlab.CIArtifactReceiver)
]