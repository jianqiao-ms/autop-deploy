#! /usr/bin/env python3
#-* coding: utf-8 -*

"""
包含
    Enviroment
    DeployRule
"""
# Official packages

# 3rd-party Packages
from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# Local Packages
from public import BaseTable, Base

# CONST

# Class&Function Defination
class TableEnviroment(BaseTable):
    __tablename__       = 'environment'

    id                  = Column(Integer, primary_key = True)
    name                = Column(String(32))
    permmit_auto_deploy = Column(Boolean())
    member              = relationship('TableContainer') # 一对多


# Logic
if __name__ == '__main__':
    from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker

    from classes import ConfigManager
    db_cfg = ConfigManager().get_config().db
    engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'.format(
        host        = db_cfg['host'],
        port        = db_cfg['port'],
        user        = db_cfg['user'],
        password    = db_cfg['password'],
        dbname      = db_cfg['database']
    ))
    # Session = sessionmaker(bind=engine)
    # session = Session()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)