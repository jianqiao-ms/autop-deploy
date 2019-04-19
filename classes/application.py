#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import json
import logging.config
from concurrent.futures import ThreadPoolExecutor

# 3rd-party Packages
import tornado.web
from tornado.httpclient import AsyncHTTPClient as HTTPClient
from tornado.httpclient import HTTPClient as SyncHTTPClient

# Local Packages
from .logger import *

# CONST
MYSQL_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/mysql.json")
SETTINGS = {
    'login_url': '/login',
    'template_path': os.path.join(os.path.dirname(__file__), "../template"),
    "static_path": os.path.join(os.path.dirname(__file__), "../static"),
    "debug":True
}


# Class&Function Defination
class Application(tornado.web.Application):
    def __init__(self, handlers=None, default_host=None, transforms=None, **settings):
        super(Application, self).__init__(handlers, default_host, transforms, **SETTINGS)
        self.EXECUTOR = ThreadPoolExecutor(max_workers=4)
        self.gitlab = GitlabServer()

    def log_request(self, handler) -> None:
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        log_method("%s \"%d %s %s\" %.2fms", handler.request.remote_ip, handler.get_status(),
                   handler.request.method, handler.request.uri, request_time
        )

class RequestHandler(tornado.web.RequestHandler):
    pass

class GitlabServer():
    def __init__(self):
        self.url = "http://gitlab.shangweiec.com/api/v4/"
        self.token = "K2faEp9ofGwNWNBpUo-L"
        self.client = HTTPClient()
        httpclient = SyncHTTPClient()
        try:
            version = json.loads(
                httpclient.fetch("http://gitlab.shangweiec.com/api/v4/version",
                                 headers={"PRIVATE-TOKEN": self.token}).body.decode()
            )
            log.info("gitlab Connected! Version: {}".format(str(version["version"])))
        except Exception as e:
            log.exception("gitlab connect failed")
            exit(1)

    async def get_all_projects(self):
        api = "projects?simple=true&per_page=100"
        result = list()
        respons = await self.read_api(api)
        result.extend(json.loads(respons.body.decode()))
        __np = respons.headers["X-Next-Page"]
        while __np:
            respons = await self.read_api("projects?simple=true&per_page=100&page={}".format(__np))
            result.extend(json.loads(respons.body.decode()))
            __np = respons.headers["X-Next-Page"]

        return result

    async def read_api(self, api):
        if api.startswith("/"):
            api = api[1:]
        try:
            respons = await self.client.fetch(self.url + api, headers={"PRIVATE-TOKEN": self.token})
            return respons
        except Exception as e:
            log.exception('Error occur reading api [{}]'.format(api))
            return
# Logic
if __name__ == "__main__":
    pass
