#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, \
    Integer, String, Enum, Boolean

# Local Packages
from classes.schema.Base import ModalBase, SchemaBase

# CONST

# Class&Function Defination
class SchemaProjectType(ModalBase, SchemaBase):
    __tablename__ = "t-project_type"

    id = Column(Integer, primary_key=True)
    name = Column(String(48), nullable=False, unique=True)
    projects = relationship("ModalProject", backref = "type")

class SchemaProject(ModalBase, SchemaBase):
    __tablename__ = "t-project"

    id = Column(Integer, primary_key=True)
    gitlab_id = Column(Integer, nullable=False, unique=True)
    visiblename = Column(String(48), nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey("t-project_type.id"))

# Logic
if __name__ == '__main__':
    pass
