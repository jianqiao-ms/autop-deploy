#! /usr/bin/env python3
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# Local Packages
from database import BaseTable

# CONST

# Class&Function Defination
class TableProject(BaseTable):
    """自关联表"""
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    gitlab_id = Column(Integer)
    role = Column(Enum('repo', 'project', 'public'), nullable = True)
    repo_id = Column(Integer, ForeignKey('project.id'))
    path = Column(String(32))
    artifact_path = Column(String(128))
    children = relationship('TableProject',
                backref = backref('parent', remote_side = [id])
            )


# Logic
if __name__ == '__main__':
    pass
