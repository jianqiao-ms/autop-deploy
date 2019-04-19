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
    __route_base__ = "/api/v1/gitlab"
    __route_path__ = ".*"

    async def get(self):
        headers = {"Content-Type": ""}
        headers.update(self.request.headers)

        api = self.request.uri[len(self.__route_base__)+1:]
        _ = await self.application.gitlab.read_api(api)
        try:
            respons = _.body.decode()
        except:
            respons = "[]"

        self.finish(respons)

    @classmethod
    def route(cls):
        return cls.__route_base__ + cls.__route_path__

route = list(map(
    lambda x:(x.route(), x),
    [
        GitlabHandler,
    ]
))
# Logic
if __name__ == '__main__':
    pass
