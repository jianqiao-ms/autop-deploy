#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, \
    Integer, String, Enum, Boolean, DateTime

# Local Packages
from classes.database.public import Base

# CONST

# Class&Function Defination


class SchemaAutoRule(ModalBase, SchemaBase):
    __tablename__ = "t-deploy_auto"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    project_id = Column(Integer, nullable=False, unique=True)
    host_id  = Column(Integer, ForeignKey('t-host.id'))
    host_group_id = Column(Integer, ForeignKey('t-host_group.id'))
    path = Column(DateTime)

class SchemaAutoHistory(ModalBase, SchemaBase):
    __tablename__ = "t-deploy_history"

    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey('t-deploy_auto.id'))
    deploy_time = Column(DateTime)

class SchemaManul(ModalBase, SchemaBase):
    __tablename__ = "t-deploy_manul"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    project_id = Column(Integer, nullable=False, unique=True)
    branch = Column(String(16))
    sha = Column(String(48))
    host_id  = Column(Integer, ForeignKey('t-host.id'))
    host_group_id = Column(Integer, ForeignKey('t-host_group.id'))
    path = Column(String(128))


# Logic
if __name__ == '__main__':
    pass
