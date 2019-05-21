#! /usr/bin/env python3
#-* coding: utf-8 -*

"""
包含
    Project
    ProjectType
    ProjectCIHistory
"""
# Official packages

# 3rd-party Packages
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# Local Packages
from public import BaseTable, Base

# CONST

# Class&Function Defination
class TableProjectType(BaseTable):
    __tablename__   = "project_type"

    id              = Column(Integer, primary_key = True)
    name            = Column(String(32))
    deploy_path     = Column(String(256))
    link_type       = Column(Enum('soft', 'hard'), nullable = True)
    link_path       = Column(String(256))
    start_cmd       = Column(String(64))
    restart_cmd     = Column(String(64))

    # member = relationship('TableProject')

class TableProject(BaseTable):
    """自关联表"""
    __tablename__   = 'project'

    id              = Column(Integer, primary_key=True)
    gitlab_id       = Column(Integer)
    name            = Column(String(32))
    build_cmd       = Column(String(128))
    role            = Column(Enum('repo', 'project', 'public','parent'), nullable = True)
    path            = Column(String(32))
    artifact_path   = Column(String(128))

    repo_id         = Column(Integer, ForeignKey('project.id'))
    children        = relationship('TableProject', backref = backref('repo', remote_side = [id]))

    type_id         = Column(Integer, ForeignKey('project_type.id'))
    type            = relationship(TableProjectType, backref = 'member')

class TableProjectCIHistory(BaseTable):
    __tablename__   = "project_ci_history"

    id              = Column(Integer, primary_key=True)
    project_id      = Column(Integer, ForeignKey('project.id'))
    branch          = Column(String(32))
    commit          = Column(String(8))

# Logic
if __name__ == '__main__':
    pass