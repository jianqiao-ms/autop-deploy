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
        host          =  'localhost',
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

    def validate(self):
        # 验证upload目录是否可写
        logging.info("Configuration validate start")
        try:
            with open(os.path.join(self.app['upload_path'], '__configuration_validate__'), 'w')  as fp:
                fp.write('configuration validate only. Delete free.')
            fp.close()
            os.remove(fp.name)
            logging.info(
                'Configuration upload_path \"{}\" validate OK'.format(self.app['upload_path']))
        except:
            logging.exception(
                'Configuration upload_path \"{}\" validate Failed'.format(self.app['upload_path']))
            exit(102)

        # 验证log目录是否可写
        try:
            with open(os.path.join(self.log['path'], '__configuration_validate__'),'w')  as fp:
                fp.write('configuration validate only. Delete free.')
            fp.close()
            os.remove(fp.name)
            logging.info(
                'Configuration log_path \"{}\" validate OK'.format(self.log['path']))
        except:
            logging.exception(
                'Configuration log_path \"{}\" validate Failed'.format(self.log['path']))
            exit(103)


        # 验证MySQL配置，并返回mysql connection session
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from classes import ConfigManager

            engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'.format(
                host        = self.db['host'],
                port        = self.db['port'],
                user        = self.db['user'],
                password    = self.db['password'],
                dbname      = self.db['database']
            ))
            session = sessionmaker(bind=engine)()
            session.close()
            logging.info(
                'Configuration database@\"{}\" validate OK'.format(self.db['host']))
        except:
            logging.exception(
                'Configuration database@\"{}\" validate Failed'.format(self.db['host']))
            exit(103)

        logging.info("Configuration validata ok")

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
                'Configuration upload_path \"{}\" validate OK'.format(self.configuration.app['upload_path']))
        except:
            logging.exception(
                'Configuration upload_path \"{}\" validate invalid'.format(self.configuration.app['upload_path']))
            exit(102)

        # 验证log目录是否可写
        try:
            with open(os.path.join(self.configuration.log['path'], '__configuration_validate__'),'w')  as fp:
                fp.write('configuration validate only. Delete free.')
            fp.close()
            os.remove(fp.name)
            logging.info(
                'Configuration log_path \"{}\" validate valid'.format(self.configuration.log['path']))
        except:
            logging.exception(
                'Configuration log_path \"{}\" validate invalid'.format(self.configuration.log['path']))
            exit(103)
        logging.info("Configuration validata ok")

# Logic
if __name__ == '__main__':
    print(__BASEPATH__)
