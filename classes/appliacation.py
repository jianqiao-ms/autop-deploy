#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import os
import json
import logging.config
from concurrent.futures import ThreadPoolExecutor

# 3rd-party Packages
import tornado.web
from tornado.log import access_log

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Local Packages

# CONST
LOG_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/logging.json")
MYSQL_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/mysql.json")

with open(LOG_CONFIG_FILE, "r") as file:
    logging.config.dictConfig(json.load(file))
    LOGGER = logging.getLogger("autop")

# Class&Function Defination
class Application(tornado.web.Application):
    def __init__(self, handlers=None, default_host=None, transforms=None,**settings):
        super(Application, self).__init__(handlers, default_host, transforms,**settings)
        self.EXECUTOR = ThreadPoolExecutor(max_workers=4)
        if "log_function" in self.settings:
            LOGGER.warning("Dumplicate log_function in settings")

        with open(MYSQL_CONFIG_FILE, "r") as file:
            self.engine = create_engine(
                "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset=utf8".format(**json.load(file)),
            )
            self.mysql = scoped_session(sessionmaker(bind=self.engine)) # http://docs.sqlalchemy.org/en/latest/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session
            LOGGER.info("MySQL connected!")
            self.schemas = self.engine.table_names()

    def log_request(self, handler):
        request_time = 1000.0 * handler.request.request_time()
        access_log.info("%d %s %.2fms", handler.get_status(),
                   handler._request_summary(), request_time)

# Logic
if __name__ == "__main__":
    pass
