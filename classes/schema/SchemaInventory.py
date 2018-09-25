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

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)
    hosts = relationship("SchemaHost", backref = 'district') # One-2-Many

HostToGroup = Table("r-host-group", ModalBase.metadata,
    Column("host_id", ForeignKey("t-host.id"), primary_key = True),
    Column("host_group_id", ForeignKey("t-host_group.id"), primary_key = True),
)
class SchemaHost(ModalBase ,SchemaBase):
    __tablename__ = "t-host"

    id              = Column(Integer, primary_key=True)
    ipaddr          = Column(String(15),  unique=True)
    visiblename     = Column(String(48),  unique=True)
    hostname        = Column(String(255), unique=True)

    is_proxy        = Column(Boolean,nullable = False, default=False)
    type            = Column(Enum("host","template"), nullable=False, default="host")

    ssh_port        = Column(Integer, nullable=False, default=22)
    ssh_auth_type   = Column(Enum("password","rsa_key"), nullable=False)
    ssh_user        = Column(String(32), nullable=False)
    ssh_key         = Column(String(255), default="")
    ssh_password    = Column(String(255), default="")

    ssh_proxy_id    = Column(Integer, ForeignKey('t-host.id'))
    template_id     = Column(Integer, ForeignKey('t-host.id'))
    district_id     = Column(Integer, ForeignKey('t-district.id'))

    groups = relationship("SchemaHostGroup",
                          secondary = HostToGroup,
                          back_populates = "hosts")

class SchemaHostGroup(ModalBase ,SchemaBase):
    __tablename__ = "t-host_group"

    id = Column(Integer, primary_key= True)
    visiblename = Column(String(255), nullable=False)

    hosts = relationship("SchemaHost",
                         secondary = HostToGroup,
                         back_populates = "groups")

# Logic
if __name__ == "__main__":
    pass