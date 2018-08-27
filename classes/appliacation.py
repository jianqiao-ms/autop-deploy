#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages
import logging
from concurrent.futures import ThreadPoolExecutor

# 3rd-party Packages
import tornado.web
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Local Packages

# CONST

# Class&Function Defination

class Application(tornado.web.Application):
    def __init__(self, handlers=None, default_host=None, transforms=None,**settings):
        super(Application, self).__init__(handlers, default_host, transforms,**settings)
        self.logger = logging.getLogger()
        self.EXECUTOR = ThreadPoolExecutor(max_workers=4)

        import os, json
        CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf/mysql.json')
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
        engine = create_engine(
            'mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset=utf8'.format(**config),
        )
        self.mysql = scoped_session(sessionmaker(bind=engine))
        self.logger.info('MySQL connected!')

# Logic
if __name__ == '__main__':
    pass
