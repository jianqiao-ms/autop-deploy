#! /usr/bin/env python
#-* coding: utf-8 -*

# Official packages

# 3rd-party Packages
from sqlalchemy.ext.declarative import declarative_base

# Local Packages

# CONST

# Class&Function Defination
Base = declarative_base()


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