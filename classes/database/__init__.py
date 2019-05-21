#! /usr/bin/env python3
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import ConfigManager

# Local Packages
from public import BaseTable, Base

from project import TableProjectType, TableProject, TableProjectCIHistory
# from enviroment import TableEnviroment
# from container import TableContainer

# CONST

# Class&Function Defination

# Logic
if __name__ == '__main__':
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