#!/usr/bin/env python3
# -*-coding:utf-8-*-

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

__base__ = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
__engine__ = create_engine('mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'.format(
    host='localhost',
    port=3306,
    user='jianqiao',
    password=' ',
    dbname='autop'
))

# reflect the tables
__base__.prepare(__engine__, reflect=True)
session = Session(__engine__)


# mapped classes are now created with names by default
# matching that of the table name.
# User = Base.classes.user
# Address = Base.classes.address

# 

# rudimentary relationships are produced
# session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
# session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
# print (u1.address_collection)

# for table in __base__.classes:
#     print(table)

Label       = __base__.classes.t_label
Brand       = __base__.classes.t_cmdb_brand
Baseinfo    = __base__.classes.t_cmdb_baseinfo
Position    = __base__.classes.t_cmdb_position
Network     = __base__.classes.t_cmdb_network
Device      = __base__.classes.t_cmdb_device
