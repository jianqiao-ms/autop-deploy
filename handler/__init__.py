__all__ = ["route", "api", "view"]

from .api import *
from .view import *

route = [
    (r"/api/v1/gitlab/receiver", gitlab.GitlabReceiver)
]