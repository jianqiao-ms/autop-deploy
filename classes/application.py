#! /usr/bin/env python3
#-* coding: utf-8 -*

# Official packages
import os
import json
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor

# 3rd-party Packages
from tornado.web import access_log
from tornado.web import Application as OriginApplication
from tornado.web import RequestHandler as OriginRequestHandler
from tornado.web import Finish, HTTPError
from tornado.httpclient import AsyncHTTPClient as HTTPClient
from tornado.httpclient import HTTPClient as SyncHTTPClient

# Local Packages
from config_manager import ConfigManager

from ci_artifact_token_manager import CIArtifactTokenManager

# CONST
MYSQL_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/mysql.json")


# Class&Function Defination
class Application(OriginApplication):
    def __init__(self, handlers=None, default_host=None, transforms=None, **settings):
        self.gitlab = GitlabServer()
        self.catm = dict()
        self.EXECUTOR = ThreadPoolExecutor(max_workers=4)
        super(Application, self).__init__(handlers, default_host, transforms, **settings)

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

class RequestHandler(OriginRequestHandler):
    def get_form_data(self, name):
        return self.request.arguments[name][0]

class RESTRequestHandler(RequestHandler):
    """
    返回json格式的错误信息
    默认格式
    {
        "message": "reason"
    }
    """
    def write_error(self, status_code: int, **kwargs):
        logging.exception(self._reason)
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header("Content-Type", "text/plain")
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish(dict(
                message = self._reason
            ))

class BashRequestHandler(RequestHandler):
    """
    返回Raw格式的错误信息
    """
    def write_error(self, status_code: int, **kwargs):
        self.finish(self._reason)

class GitlabServer():
    def __init__(self):
        self.url = "http://192.168.3.252/api/v4/"
        self.token = "K2faEp9ofGwNWNBpUo-L"
        self.client = HTTPClient()
        try:
            httpclient = SyncHTTPClient()
            version = json.loads(
                httpclient.fetch("http://192.168.3.252/api/v4/version",
                                 headers={"PRIVATE-TOKEN": self.token}).body.decode()
            )
            logging.info("gitlab Connected! Version: {}".format(str(version["version"])))
        except Exception as e:
            logging.exception("gitlab connect failed")
            exit(103)

    async def read_api(self, api, request_handler:RequestHandler=None):
        if api.startswith("/"):
            api = api[1:]
        try:
            respons = await self.client.fetch(self.url + api, headers={"PRIVATE-TOKEN": self.token})
            return respons.body.decode()
        except Exception as e:
            ERROR_CODE = 503
            ERROR_MSG = 'Error occur reading api [{}]'.format(api)
            logging.exception(ERROR_MSG)
            if request_handler:
                raise HTTPError(ERROR_CODE, reason="aasd")

# Logic
if __name__ == "__main__":
    pass
