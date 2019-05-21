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
from tornado.web import HTTPError
from tornado.httpclient import HTTPClientError
from tornado.httpclient import AsyncHTTPClient as HTTPClient
from tornado.httpclient import HTTPClient as SyncHTTPClient


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local Packages
from cfg_manager import Configuration
# CONST
# Class&Function Defination
class GitlabServer():
    def __init__(self):
        __gitlab_url__  = None
        __ret__         = None
        self.url        = "http://192.168.3.252/api/v4/"
        self.token      = "K2faEp9ofGwNWNBpUo-L"
        self.client     = HTTPClient()
        try:
            __gitlab_url__ = self.url + "version"
            __ret__ = SyncHTTPClient().fetch(__gitlab_url__, headers={"PRIVATE-TOKEN": self.token}, request_timeout = 3.0)
            version = json.loads(__ret__.body.decode())
            logging.info("gitlab Connected! Version: {}".format(str(version["version"])))
        except json.decoder.JSONDecodeError as e:
            logging.debug('\n' + __ret__.body.decode())
            logging.error('Gitlab 返回结果不正确。检查gitlab版本、权限 或dns解析是否跳转到宽带运营商页面')
            exit(111)
        except HTTPClientError as e:
            logging.error('Gitlab 连接失败。请检查gitlab url路径"{}"'.format(__gitlab_url__))
            exit(112)
        except:
            logging.exception("Gitlab 连接失败")
            exit(113)

    async def read_api(self, api):
        if api.startswith("/"):
            api = api[1:]
        try:
            respons = await self.client.fetch(self.url + api, headers={"PRIVATE-TOKEN": self.token})
            return respons.body.decode()
        except:
            logging.exception('Error occur reading api [{}]'.format(api))
            HTTPError(503, reason='Error occur reading api [{}]'.format(api))


class Application(OriginApplication):
    def __init__(self, handlers=None, default_host=None, transforms=None, configuration:Configuration = None):
        # catm : CI Access Token Manager
        self.catm = dict()
        self.gitlab = GitlabServer()
        self.EXECUTOR = ThreadPoolExecutor(max_workers=4)

        db_cfg = configuration.db
        engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'.format(
            host=db_cfg['host'],
            port=db_cfg['port'],
            user=db_cfg['user'],
            password=db_cfg['password'],
            dbname=db_cfg['database']
        ))
        self.session = sessionmaker(bind=engine)()
        super(Application, self).__init__(handlers, default_host, transforms, **configuration.app)

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

# Logic
if __name__ == "__main__":
    pass