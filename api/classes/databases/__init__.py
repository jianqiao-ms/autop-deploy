#!/usr/bin/env python3
# -*-coding:utf-8-*-

from .tables import session

from .tables import Label
from .tables import Brand
from .tables import Baseinfo
from .tables import Position
from .tables import Network
from .tables import Device

from sqlalchemy import inspect

import logging

def get_columns(__table):
    inst = inspect(__table)
    
    
    attr_names = [( c_attr.key,c_attr.type) for c_attr in __table.__table__.columns]
    
    
    
    print(attr_names)