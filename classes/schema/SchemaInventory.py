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
"""
# Many-to-many https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""

class SchemaDistrict(ModalBase, SchemaBase):
    __tablename__ = "t-district"
    __visiblename__ = "District"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)
    hosts = relationship("SchemaHost", back_populates = "district") # One-2-Many

HostToGroup = Table("r-host-group", ModalBase.metadata,
    Column("host_id", ForeignKey("t-host.id"), primary_key = True),
    Column("host_group_id", ForeignKey("t-host_group.id"), primary_key = True),
)
class SchemaHost(ModalBase ,SchemaBase):
    __tablename__ = "t-host"
    __visiblename__ = "Host"

    id              = Column(Integer, primary_key=True)
    ipaddr           = Column(String(15), unique=True, default="")
    visiblename     = Column(String(48), unique=True, nullable=False)
    hostname        = Column(String(255), unique=True, default="")

    type            = Column(Enum("host","template","proxy"), nullable=False, default="host")

    ssh_port        = Column(Integer, nullable=False, default=22)
    ssh_auth_type   = Column(Enum("password","rsa_key"), nullable=False, default="password")
    ssh_user        = Column(String(32), nullable=False)
    ssh_key         = Column(String(255), default="")
    ssh_password    = Column(String(255), default="")

    ssh_proxy_id    = Column(Integer, ForeignKey('t-host.id'))
    template_id     = Column(Integer, ForeignKey('t-host.id'))
    district_id     = Column(Integer, ForeignKey('t-district.id'))
    district        = relationship("SchemaDistrict", back_populates = "hosts", lazy="joined")
    ssh_proxy       = relationship("SchemaHost", foreign_keys = [ssh_proxy_id])
    template        = relationship("SchemaHost", foreign_keys = [template_id])

    groups = relationship("SchemaHostGroup",
                          secondary = HostToGroup,
                          back_populates = "hosts")

class SchemaHostGroup(ModalBase ,SchemaBase):
    __tablename__ = "t-host_group"
    __visiblename__ = "Host Group"

    id = Column(Integer, primary_key= True)
    visiblename = Column(String(255), nullable=False)

    hosts = relationship("SchemaHost",
                         secondary = HostToGroup,
                         back_populates = "groups")

class SchemaProjectType(ModalBase, SchemaBase):
    __tablename__ = "t-project_type"
    __visiblename__ = "Project Type"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    deploy_path = Column(String(128), nullable=False, unique=False, default="/data/apps")
    run_path = Column(String(128), nullable=False, unique=False, default="/data/run")
    projects = relationship("SchemaProject", backref = "type")

class SchemaProject(ModalBase, SchemaBase):
    __tablename__ = "t-project"
    __visiblename__ = "Project"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    deploy_name = Column(String(64), nullable=False)
    gitlab_id = Column(Integer, nullable=False, unique=True)
    type_id = Column(Integer, ForeignKey("t-project_type.id"))

# Logic
if __name__ == "__main__":
    pass