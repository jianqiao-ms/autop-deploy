#! /usr/bin/env python3
#-* coding: utf-8 -*

# Official packages
import os
import json

# 3rd-party Packages

# Local Packages


# CONST
__BASEPATH__    = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
__CONFIG_FILE__ = os.path.join(__BASEPATH__, 'conf/autop.json')

# Class&Function Defination
class ConfigManager():
    def get_config(self):
        return Configuration()

    def validate_config_log(self, _c:dict):
        try:
            with open(os.path.join(_c['path'], '__configuration_validate__'))  as fp:
                fp.write('configuration validate only. Delete free.')
            fp.close()
            os.remove(fp.name)
        from logger import log

class Configuration():
    app = dict(
        debug       = False,
        upload_path = os.path.join(__BASEPATH__, 'upload'),
    )
    db = dict(
        server      = 'localhost',
        port        = 3306,
        user        = 'user',
        password    = 'password',
        database    = 'autop'
    )
    log = dict(
        level       = 'info',
        console     = True,
        path        = os.path.join(__BASEPATH__, 'logs'),
        format      = '[%(asctime)s] %(levelname)s %(filename)s %(funcName)s %(lineno)d -- %(message)s'
    )
    def __init__(self):
        __c = None
        try:
            log.info('开始读取配置文件')
            with open(__CONFIG_FILE__) as fp:
                __c = json.load(fp)
        except:
            log.exception('Error code:101. 读取配置文件失败')
            exit(101)

        self.app.update(__c['app'])
        self.db.update(__c['db'])
        self.log.update(__c['log'])
        self.validate_app_config()

    def validate_app_config(self):
        try:
            with open(os.path.join(self.app['upload_path'], '__configuration_validate__'), 'w') as fp:
                fp.write('configuration validate only. Delete free.')
                fp.close()
            os.remove(fp.name)
            log.info("app配置文件验证成功")
        except:
            log.exception('配置文件验证失败.upload目录{}没有写入权限.'.format(self.app['upload_path']))

# Logic
if __name__ == '__main__':
    print(__BASEPATH__)
