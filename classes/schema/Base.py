#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy.ext.declarative import declarative_base

# Local Packages
from classes.newdict import dict

# CONST

# Class&Function Defination
class NonSenseObject(object):
    """This Class HAS NO ACTUAL USAGE
    The ONLY function is avoid warnings in SchemaBase
    """
    columns = []

ModalBase = declarative_base()
class SchemaBase():
    __table__ = NonSenseObject
    __tablename__ = ""
    __visiblename__ = ""
    # def __repr__(self):
    #     line_format = "<{tablename}({columns})>"
    #     column_name = [x.name+'={}' for x in self.__table__.columns]
    #     line_format = line_format.format(tablename = self.__visiblename__, columns = ",".join(column_name))
    #
    #     data = [str(self.__dict__[x.name]) if self.__dict__[x.name] is not None else '""' for x in self.__table__.columns]
    #     return line_format.format(*data)

    def dict(self):
        return dict(
            (key, self.__dict__[key] if not isinstance(self.__dict__[key], SchemaBase) else
                    self.__dict__[key].dict()
             ) for key in self.__dict__.keys() if not key.startswith("_")
        )

# Logic
if __name__ == "__main__":
    import os, json
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker

    from classes.schema.SchemaInventory import *
    from classes.schema.SchemaDeploy import *

    MYSQL_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "../../conf/mysql.json")
    with open(MYSQL_CONFIG_FILE, "r") as file:
        engine = create_engine(
            "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset=utf8".format(**json.load(file)),
        )
        mysql = scoped_session(sessionmaker(
            bind=engine))()  # http://docs.sqlalchemy.org/en/latest/orm/contextual.html#sqlalchemy.orm.scoping.scoped_session

    ModalBase.metadata.drop_all(engine)
    ModalBase.metadata.create_all(engine)

