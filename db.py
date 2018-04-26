#! /usr/bin/env python
#-* coding: utf-8 -*

# create db connectin

from sqlalchemy import  Column, Integer, String, DateTime, Binary

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

class Container(Base):
    __tablename__ = 't_container'
    id = Column(Integer, primary_key=True)
    name = Column(String(16))
    ipaddr = Column(String(16))
    type = Column(Integer)
    group_id = Column(Integer)
    env_id = Column(Integer)

class AppType(Base):
    __tablename__ = 't_app_type'
    id = Column(Integer, primary_key=True)
    type = Column(String(16))

class App(Base):
    __tablename__ = 't_app'
    gitlab_id   = Column(Integer, primary_key=True)
    deploy_name = Column(String(32))
    type_id     = Column(Integer)

class DeployRule(Base):
    __tablename__ = 't_deploy_rule'
    id = Column(Integer, primary_key=True)
    gitlab_id = Column(Integer)
    env_id = Column(Integer)
    container_id = Column(Integer)
    deploy_path = Column(String(128))
    run_path = Column(String(128))
    automatic = Column(Binary)
    exclude = Column(String(2048))

class DeployHistory(Base):
    __tablename__ = 't_history_deploy'
    id = Column(Integer, primary_key=True)
    rule_id   = Column(Integer)
    type        = Column(String(8))
    state = Column(Integer)
    commit      = Column(String(48))
    commit_time = Column(DateTime)
    action_time     = Column(DateTime)
    user_id     = Column(Integer)


if __name__ == '__main__':
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)