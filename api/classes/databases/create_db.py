#! /usr/bin/env python3
# -* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum

# Local Packages

# CONST
Base = declarative_base()


# Class&Function Defination
class Label(Base):
    __tablename__ = 't_label'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))


class BaseInformation(Base):
    __tablename__ = 't_cmdb_baseinfo'

    id = Column(Integer, primary_key=True)
    local_ip = Column(String(15))
    www_ip = Column(String(15))
    sn = Column(String(128))
    fixed_assets_number = Column(String(128))
    vendor_id = Column(Integer)
    group_id = Column(Integer)


class Vendor(Base):
    __tablename__ = 't_cmdb_brand'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    comment = Column(String(1024))


class Position(Base):
    __tablename__ = 't_cmdb_position'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('City', 'DC', 'RACK', 'Sequence'))
    description = Column(String(64))


class Network(Base):
    __tablename__ = 't_cmdb_network'

    id = Column(Integer, primary_key=True)
    position_id = Column(Integer)
    bandwidth = Column(Integer)
    ip = Column(String(18))


class Device(Base):
    __tablename__ = 't_cmdb_device'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('firewall', 'router', 'switch', 'physical', 'vm'))
    position_id = Column(Integer)
    baseinfo_id = Column(Integer)
    label_id = Column(Integer)


# Logic
if __name__ == '__main__':
    engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'.format(
        host='localhost',
        port=3306,
        user='jianqiao',
        password=' ',
        dbname='autop'
    ))
    # Session = sessionmaker(bind=engine)
    # session = Session()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)