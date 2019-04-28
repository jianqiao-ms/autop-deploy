#! /usr/bin/env python
#-* coding: utf-8 -*

# __all__ = ['log', 'access_log', 'app_log', 'gen_log']

# Official packages
import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler

# 3rd-party Packages
import tornado.log

# Local Packages

# CONST
# CONFIG_FILE = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)), 'conf/log.json')
# with open(CONFIG_FILE, 'r') as fp:
#     configuration = json.load(fp)
# access_log = tornado.log.access_log
# access_log.setLevel(logging._nameToLevel[configuration['level'].upper()])
# app_log = tornado.log.app_log
# app_log.setLevel(logging._nameToLevel[configuration['level'].upper()])
#
# # Class&Function Defination
# def getHandler(cls:callable, filename='autop.log',
#                formatString='[%(asctime)s] %(levelname)s %(filename)s %(funcName)s %(lineno)d -- %(message)s'):
#
#     handler = cls() if logging.StreamHandler == cls else \
#         cls(filename = os.path.join(configuration['path'], filename), when='D')
#     handler.setFormatter(logging.Formatter(formatString))
#     return handler
#
# # Logic
# access_log.addHandler(
#     getHandler(TimedRotatingFileHandler, filename='access.log', formatString = '[%(asctime)s] %(message)s'))
# app_log.addHandler(getHandler(TimedRotatingFileHandler, filename='autop.log', formatString = configuration['format']))
# if configuration['console']:
#     access_log.addHandler(getHandler(logging.StreamHandler, formatString = '[%(asctime)s] %(message)s'))
#     app_log.addHandler(getHandler(logging.StreamHandler, formatString = configuration['format']))
# gen_log     = tornado.log.gen_log
# map(gen_log.addHandler, app_log.handlers)
# log = app_log


class LogManager():
    def __init__(self):
        self.root = logging.getLogger()


    def get_base_logger(self):
        self.root.setLevel(logging._nameToLevel['DEBUG'])
        __handler_during_start__ = logging.StreamHandler()
        __handler_during_start__.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(filename)s %(funcName)s %(lineno)d -- %(message)s'))
        self.root.addHandler(__handler_during_start__)

    def get_logger(self, log_configuration):
        # 获取配置参数
        __log_level__ = logging._nameToLevel[log_configuration['level'].upper()]
        __access_log_formater__ = logging.Formatter('[%(asctime)s] %(message)s')
        __app_log_formater__ = logging.Formatter(log_configuration['format'])


        # 配置文件handler
        __access_file_handler = TimedRotatingFileHandler(
            os.path.join(log_configuration['path'], 'access.log'), when='D')
        __access_file_handler.setFormatter(__access_log_formater__)
        __app_file_handler__ = TimedRotatingFileHandler(
            os.path.join(log_configuration['path'], 'autop.log'), when='D')
        __app_file_handler__.setFormatter(__app_log_formater__)


        #
        # list(map(root_log.removeHandler, root_log.handlers))  # 清空root logger的所有handler


        from tornado.log import access_log
        from tornado.log import gen_log
        from tornado.log import app_log
        root_log = self.root
        __loggers__   = [root_log, access_log, gen_log, app_log]




        # 设置logger级别
        # self.root.setLevel(__log_level__)
        list(map(lambda x: x.setLevel(__log_level__), __loggers__))



        # 添加handler到logger
        access_log.addHandler(__access_file_handler)
        app_log.addHandler(__app_file_handler__)
        gen_log.addHandler(__app_file_handler__)
        root_log.addHandler(__app_file_handler__)


        # if log_configuration['console']:
        #     ___console_handler_ = logging.StreamHandler()
        #     ___console_handler_.setFormatter(__formater__)
            # list(map(lambda x: x.addHandler(___console_handler_), __loggers__))

            # access_log.addHandler(___console_handler_)
            # app_log.addHandler(___console_handler_)
            # gen_log.addHandler(___console_handler_)
            # root_log.addHandler(__app_file_handler__)

if __name__ == '__main__':
    import time
    # log.debug(time.strftime("%Y-%m-%d %H:%M:%S"))
