#! /usr/bin/env python
#-* coding: utf-8 -*

"""
Reference:
    Basic Relationship Patterns
    http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
"""

# Official packages
import os
import json
# 3rd-party Packages
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, \
    Integer, String, Enum, BigInteger, DateTime, Time, Date

# Local Packages

# CONST
MYSQL_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/mysql.json")

# Class&Function Defination
ModalBase = declarative_base()
class SchemeBase():
    def __repr__(self):
        # """          id     ipaddr  hostname visiblename ssh_auth_type ssh_user ssh_key ssh_password"""
        line_format = "<{tablename}({columns})>"
        column_name = ['"'+x.name+'"={}' for x in self.__table__.columns]
        line_format = line_format.format(tablename = self.__tablename__, columns = ",".join(column_name))

        data = [str(self.__dict__[x.name]) for x in self.__table__.columns]
        return line_format.format(*data)

HostToGroup = Table("relation_host-group", ModalBase.metadata,
    Column("host_id", ForeignKey("data_host.id"), primary_key = True),
    Column("hostgroup", ForeignKey("data_hostgroup.id"), primary_key = True),
)

class HostType(ModalBase, SchemeBase):
    __tablename__ = "data_hosttype"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    ssh_auth_type = Column(Enum("password", "rsa_key"), nullable=False)
    ssh_user = Column(String(32), nullable=False)
    ssh_key = Column(String(255))
    ssh_password = Column(String(255))

    hosts = relationship("Host", backref="type")

class Host(ModalBase, SchemeBase):
    __tablename__ = "data_host"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    ipaddr = Column(String(15), nullable=False)
    hostname = Column(String(255), nullable=False)
    ssh_auth_type = Column(Enum("password","rsa_key"), nullable=False)
    ssh_user = Column(String(32), nullable=False)
    ssh_key = Column(String(255))
    ssh_password = Column(String(255))

    type_id = Column(Integer, ForeignKey('data_hosttype.id'))

    groups = relationship("HostGroup",
                          secondary = HostToGroup,
                          back_populates = "hosts")

class HostGroup(ModalBase, SchemeBase):
    __tablename__ = "data_hostgroup"

    id = Column(Integer, primary_key= True)
    visiblename = Column(String(255), nullable=False)

    hosts = relationship("Host",
                         secondary = HostToGroup,
                         back_populates = "groups")
# Logic
if __name__ == '__main__':
    with open(MYSQL_CONFIG_FILE, "r") as file:
        engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset=utf8".format(**json.load(file)),
        )
        mysql = sessionmaker(
            bind=engine)() # http://docs.sqlalchemy.org/en/latest/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session
        schemas = engine.table_names()

    # ModalBase.metadata.drop_all(engine)
    # ModalBase.metadata.create_all(engine)

    record = mysql.query(Host).all()[0]
    print(record.type)

