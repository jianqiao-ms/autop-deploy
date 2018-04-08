#! /usr/bin/env python
#-* coding: utf-8 -*

# create db connectin

from sqlalchemy import  Column, Integer, String

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://majianqiao:jianqiaoA1!@192.168.3.251/autop', encoding='utf-8')
db_session  = sessionmaker(bind = engine)()
Base = declarative_base()

class Project(Base):
    __tablename__ = 't_project'

    gitlab_id   = Column(Integer, primary_key=True)
    name        = Column(String(32))
    deploy_name = Column(String(32))
    description = Column(String(256))
    repo_ssh    = Column(String(256))
    repo_htts   = Column(String(128))
    lang        = Column(String(32))
    tags        = Column(String(128))


if __name__ == '__main__':
    Base.metadata.create_all(engine)