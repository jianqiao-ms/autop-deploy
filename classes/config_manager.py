#! /usr/bin/env python3
#-* coding: utf-8 -*

# Official packages
import os
import json
import logging

# 3rd-party Packages

# Local Packages


# CONST
__BASEPATH__    = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
__CONFIG_FILE__ = os.path.join(__BASEPATH__, 'conf/autop.json')

# Class&Function Defination


class Configuration():
    app = dict(
        debug           = False,
        upload_path     = os.path.join(__BASEPATH__, 'upload'),
        login_url       = '/login',
        template_path   = os.path.join(__BASEPATH__, "template"),
        static_path     = os.path.join(__BASEPATH__, "static")
    )
    db = dict(
        server          =  'localhost',
        port            =  3306,
        user            =  'user',
        password        =  'password',
        database        =  'autop'
    )
    log = dict(
        level           =  'info',
        console         =  True,
        path            =  os.path.join(__BASEPATH__, 'logs'),
        format          =  '[%(asctime)s] %(levelname)s %(filename)s %(funcName)s %(lineno)d -- %(message)s'
    )
    def __init__(self, **kwargs):
        self.app.update(kwargs['app'])
        self.db.update(kwargs['db'])
        self.log.update(kwargs['log'])

class ConfigManager():
    def get_config(self):
        logging.info("Configuration read start")
        with open(os.path.join(__BASEPATH__, 'conf/autop.json')) as fp:
            self.configuration = Configuration(**json.load(fp))
        logging.info("Configuration read ok")
        return self.configuration

    def validate(self):
        # 验证upload目录是否可写
        logging.info("Configuration validate start")
        try:
            with open(os.path.join(self.configuration.app['upload_path'], '__configuration_validate__'), 'w')  as fp:
                fp.write('configuration validate only. Delete free.')
            fp.close()
            os.remove(fp.name)
            logging.info(
                'Configuration validate upload_path \"{}\" is valid'.format(self.configuration.app['upload_path']))
        except:
            logging.exception(
                'Configuration validate upload_path \"{}\" is invalid'.format(self.configuration.app['upload_path']))
            exit(102)

        # 验证log目录是否可写
        try:
            with open(os.path.join(self.configuration.log['path'], '__configuration_validate__'),'w')  as fp:
                fp.write('configuration validate only. Delete free.')
            fp.close()
            os.remove(fp.name)
            logging.info(
                'Configuration validate log_path \"{}\" valid'.format(self.configuration.log['path']))
        except:
            logging.exception(
                'Configuration validate log_path \"{}\" invalid'.format(self.configuration.log['path']))
            exit(103)
        logging.info("Configuration validata ok")

# Logic
if __name__ == '__main__':
    print(__BASEPATH__)
