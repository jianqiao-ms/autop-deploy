#! /usr/bin/env python
#-* coding: utf-8 -*

# create db connectin

from sqlalchemy import  Column, Integer, String, DateTime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://majianqiao:jianqiaoA1!@192.168.3.251/autop?charset=utf8')
session  = sessionmaker(bind = engine)()
Base = declarative_base()

class Environment(Base):
    __tablename__ =  't_environment'
    id = Column(Integer, primary_key=True)
    name = Column(String(16))

class Host(Base):
    __tablename__ = 't_host'
    id = Column(Integer, primary_key=True)
    gid = Column(Integer)
    eid = Column(Integer)

class HostGroup(Base):
    __tablename__ = 't_hostgroup'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))

class App(Base):
    __tablename__ = 't_app'
    gitlab_id   = Column(Integer, primary_key=True)
    deploy_name = Column(String(32))
    lang_id     = Column(Integer)

class AppLang(Base):
    __tablename__ = 't_app_lang'
    id = Column(Integer, primary_key=True)
    lang = Column(String(16))

class DeployAutoRule(Base):
    __tablename__ = 't_deploy_auto_rule'
    appid = Column(Integer, primary_key=True)
    eid = Column(Integer)
    dst_device = Column(Integer)
    dst_path = Column(String(128))
    dst_ln = Column(String(128))
    rst_cmd = Column(String(32))

class DeployManualRequest(Base):
    __tablename__ = 't_deploy_manual_request'
    appid = Column(Integer, primary_key=True)
    eid = Column(Integer)
    dst_device = Column(Integer)
    dst_path = Column(String(128))
    dst_ln = Column(String(128))
    rst_cmd = Column(String(32))
    commit = Column(String(48))

class DeployHistory(Base):
    __tablename__ = 't_history_deploy'
    gitlab_id   = Column(Integer, primary_key=True)
    commit      = Column(String(48))
    commit_msg  = Column(String(256))
    commit_time = Column(DateTime)
    op_time     = Column(DateTime)
    type        = Column(String(8))
    user_id     = Column(Integer)

if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)