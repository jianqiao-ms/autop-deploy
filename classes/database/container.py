#! /usr/bin/env python3
#-* coding: utf-8 -*

"""
包含
    Container
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
class TableContainer(BaseTable):
    __tablename__   = "container"

    id              = Column(Integer, primary_key = True)
    env_id          = Column(Integer, ForeignKey('environment.id')) # 多对一
    fqdn            = Column(String(32))
    ssh_user        = Column(String(32))
    ssh_port        = Column(Integer)
    ssh_auth_type   = Column(Enum('password', 'pubkey'), nullable=False)
    ssh_auth        = Column(String(256))
    type            = Column(Enum('host', 'hostgroup'), nullable=False)
    is_proxy        = Column(Boolean())
    group_id        = Column(Integer, ForeignKey('container.id')) # 自关联，多对一
    proxy_id        = Column(Integer, ForeignKey('container.id')) # 自关联，多对一
    enviroment      = relationship('Enviroment', backref='member')
    children        = relationship('TableContainer',
                            backref=backref('group', remote_side=[id]),
                            foreign_keys=[group_id])
    pchildren       = relationship('TableContainer',
                            backref=backref('proxy', remote_side=[id]),
                            foreign_keys = [proxy_id])

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