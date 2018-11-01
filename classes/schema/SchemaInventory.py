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

class SchemaProject(ModalBase, SchemaBase):
    __tablename__ = "t-project"
    __visiblename__ = "Project"

    id = Column(Integer, primary_key=True)
    gitlab_id = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey('t-project.id'))
    visiblename = Column(String(48), nullable=False, unique=True)
    standalone = Column(Boolean, default=True)
    role = Column(Enum("public", "product", "parent"), comment="Role in package for M-in-O Java project")

    ci_rule = relationship("SchemaCIRule", back_populates="project", lazy="joined")
    children = relationship("SchemaProject")

class SchemaCIRule(ModalBase, SchemaBase):
    __tablename__ = "t-ci_rule"
    __visiblename__ = "CI Rule"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("t-project.id"))
    build_cmd = Column(String(256), default="")
    package_name = Column(String(32), default="")


    project = relationship("SchemaProject", back_populates = "ci_rule")

# Logic
if __name__ == "__main__":
    pass