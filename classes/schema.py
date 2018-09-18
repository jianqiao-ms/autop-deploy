#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, ForeignKey, \
    Integer, String, Enum, BigInteger, DateTime, Time, Date, Boolean

# Local Packages

# CONST

# Class&Function Defination
"""
# Many-to-many https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""

ModalBase = declarative_base()

class SchemeBase():
    def __repr__(self):
        """          id     ipaddr  hostname visiblename ssh_auth_type ssh_user ssh_key ssh_password"""
        line_format = "<{tablename}({columns})>"
        column_name = ['"'+x.name+'"={}' for x in self.__table__.columns]
        line_format = line_format.format(tablename = self.__tablename__, columns = ",".join(column_name))

        data = [str(self.__dict__[x.name]) for x in self.__table__.columns]
        return line_format.format(*data)

    def json(self):
        obj_dict = self.__dict__
        return dict((key, obj_dict[key]) for key in obj_dict if not key.startswith("_"))

class ModalDistrict(ModalBase, SchemeBase):
    __tablename__ = "t-district"

    id = Column(Integer, primary_key=True)
    visiblename = Column(String(48), nullable=False, unique=True)
    hosts = relationship("ModalHost", backref = 'district') # One-2-Many

HostToGroup = Table("r-host-group", ModalBase.metadata,
    Column("host_id", ForeignKey("t-host.id"), primary_key = True),
    Column("host_group_id", ForeignKey("t-host_group.id"), primary_key = True),
)
class ModalHost(ModalBase ,SchemeBase):
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

    groups = relationship("ModalHostGroup",
                          secondary = HostToGroup,
                          back_populates = "hosts")

class ModalHostGroup(ModalBase ,SchemeBase):
    __tablename__ = "t-host_group"

    id = Column(Integer, primary_key= True)
    visiblename = Column(String(255), nullable=False)

    hosts = relationship("ModalHost",
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
            bind=engine))()  # http://docs.sqlalchemy.org/en/latest/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session

        # session = mysql()

    ModalBase.metadata.drop_all(engine)
    ModalBase.metadata.create_all(engine)
