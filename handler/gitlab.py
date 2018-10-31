#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import json

# 3rd-party Packages
from tornado.web import RequestHandler
# Local Packages

# CONST

# Class&Function Defination
class GitlabHandler(RequestHandler):
    route_path = "/api/gitlab.*"

    async def get(self):
        headers = {"Content-Type": ""}
        headers.update(self.request.headers)

        api = self.request.uri[12:]
        _ = await self.application.gitlab.read_api(api)
        try:
            respons = _.body.decode()
        except:
            respons = "[]"

        if headers["Content-Type"] == "application/json":
            self.finish(respons)

app_api = list(map(
    lambda x:(x.route_path, x),
    [
        GitlabHandler,
    ]
))
# Logic
if __name__ == '__main__':
    pass
