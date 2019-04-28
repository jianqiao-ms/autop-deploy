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

# Class&Function Defination
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


        from tornado.log import access_log
        from tornado.log import gen_log
        from tornado.log import app_log
        root_log = self.root
        __loggers__   = [root_log, access_log, gen_log, app_log]

        # 设置logger级别
        list(map(lambda x: x.setLevel(__log_level__), __loggers__))
        list(map(root_log.removeHandler, root_log.handlers))  # 清空root logger的所有handler

        # 添加handler到logger
        access_log.addHandler(__access_file_handler)
        app_log.addHandler(__app_file_handler__)
        gen_log.addHandler(__app_file_handler__)
        root_log.addHandler(__app_file_handler__)

        if log_configuration['console']:
            ___console_handler_ = logging.StreamHandler()
            ___console_handler_.setFormatter(__app_log_formater__)
            list(map(lambda x: x.addHandler(___console_handler_), __loggers__))

# Logic
if __name__ == '__main__':
    import time
    # log.debug(time.strftime("%Y-%m-%d %H:%M:%S"))
