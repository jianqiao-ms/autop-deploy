#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, \
    Integer, String, Enum, BigInteger, DateTime, Time, Date

# Local Packages

# CONST

# Class&Function Defination
"""
# Many-to-many https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""

ModalBase = declarative_base()

HostToGroup = Table("relation_host-group", ModalBase.metadata,
    Column("host_id", ForeignKey("data_host.id"), primary_key = True),
    Column("hostgroup", ForeignKey("data_hostgroup.id"), primary_key = True),
)

class HostType(ModalBase):
    __tablename__ = "data_hosttype"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)

    ssh_auth_type = Column(Enum("password", "rsa_key"), nullable=False)
    ssh_user = Column(String(32), nullable=False)
    ssh_key = Column(String(255))
    ssh_password = Column(String(255))

    hosts = relationship("Host",
                         backref = "data_hosttype")

    def __repr__(self):
        # """          id     ipaddr  hostname visiblename ssh_auth_type ssh_user ssh_key ssh_password"""
        line_format = "<{tablename}({columns})>"
        column_name = ['"'+x.name+'"={}' for x in self.__table__.columns]
        line_format = line_format.format(tablename = self.__tablename__, columns = ",".join(column_name))

        data = [str(self.__dict__[x.name]) for x in self.__table__.columns]
        return line_format.format(*data)


class Host(ModalBase):
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
    def __repr__(self):
        # """          id     ipaddr  hostname visiblename ssh_auth_type ssh_user ssh_key ssh_password"""
        line_format = "<{tablename}({columns})>"
        column_name = ['"'+x.name+'"={}' for x in self.__table__.columns]
        line_format = line_format.format(tablename = self.__tablename__, columns = ",".join(column_name))

        data = [str(self.__dict__[x.name]) for x in self.__table__.columns]
        return line_format.format(*data)

class HostGroup(ModalBase):
    __tablename__ = "data_hostgroup"

    id = Column(Integer, primary_key= True)
    visiblename = Column(String(255), nullable=False)

    hosts = relationship("Host",
                         secondary = HostToGroup,
                         back_populates = "groups")

# Logic
if __name__ == "__main__":
    import os, json
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    MYSQL_CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/mysql.json")
    with open(MYSQL_CONFIG_FILE, "r") as file:
        engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset=utf8".format(**json.load(file)),
        )
        mysql = scoped_session(sessionmaker(
            bind=engine))  # http://docs.sqlalchemy.org/en/latest/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session

        session = mysql()

    ModalBase.metadata.drop_all(engine)
    ModalBase.metadata.create_all(engine)

    # host = session.query(Host).filter_by(ipaddr = "192.168.3.2").all()

    # host[0].__repr__()
    #
    # print(host[0])

    # for h in host:
    #     print(h)
        # print(dir(h))
        # print(h.__dict__)
        # a = [x.name for x in h.__table__.columns]
        # print(a)
        # print(type(a))
        # print(" ".join(a))

