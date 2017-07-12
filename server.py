#!/usr/bin/env python
# -*- coding:UTF-8 -*-


import os
import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from tornado import options
from tornado import ioloop
from tornado.web import Application

from main.handlers import handlers
from main.settings import settings

# 创建Orm对象的基类:
OrmBase = declarative_base()

class autop(Application, object):
    def __init__(self, handlers=None, default_host=None, transforms=None,
                 **settings):

        # 读取配置文件
        config_file = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'autop.conf'))
        config = configparser.ConfigParser()
        config.read(config_file)
        dbconfig = config['db']
        engine = create_engine('mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{dbname}'.format(
            user=dbconfig['user'],
            passwd=dbconfig['pass'],
            host=dbconfig['host'],
            port=dbconfig['port'],
            dbname=dbconfig['name']
        ))

        self.db = scoped_session(sessionmaker(bind=engine,
                                              autocommit=False,
                                              autoflush=True,
                                              expire_on_commit=False))

        super(autop, self).__init__(handlers=handlers, default_host=default_host, transforms=transforms,
                                    **settings)

if __name__ == "__main__":
    print('Starting Server...')
    options.parse_command_line()
    autop(handlers = handlers, **settings).listen(8888)
    ioloop.IOLoop.instance().start()