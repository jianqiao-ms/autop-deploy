#! /usr/bin/env python3
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# Local Packages
from public import BaseTable, Base

# CONST

# Class&Function Defination
class TableProject(BaseTable):
    """自关联表"""
    __tablename__   = 'project'

    id              = Column(Integer, primary_key=True)
    gitlab_id       = Column(Integer)
    name            = Column(String(32))
    build_cmd       = Column(String(128))
    role            = Column(Enum('repo', 'project', 'public'), nullable = True)
    path            = Column(String(32))
    artifact_path   = Column(String(128))

    repo_id = Column(Integer, ForeignKey('project.id'))
    children        = relationship('TableProject', backref = backref('parent', remote_side = [id]))

class TableProjectCIHistory(BaseTable):
    __tablename__ = "project_ci_history"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    branch = Column(String(32))
    commit = Column(String(8))


# Logic
if __name__ == '__main__':
    from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker

    from classes import ConfigManager
    mysql_config = ConfigManager().get_config().db
    engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'.format(
        host = mysql_config['host'],
        port = mysql_config['port'],
        user = mysql_config['user'],
        password = mysql_config['password'],
        dbname = mysql_config['database']
    ))
    # Session = sessionmaker(bind=engine)
    # session = Session()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)