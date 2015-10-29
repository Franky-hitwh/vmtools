#!/usr/bin/env python
#coding=utf8
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

Base = declarative_base()


class Auth_User(Base):

    __tablename__ = 'auth_user'

    username = Column(String(20), primary_key=True)

class VM(Base):

    __tablename__ = 'vmtools_vm'

    id = Column(Integer,  primary_key=True)
    username = Column(String(20))
    VMName = Column(String(30))
    STATE = Column(Integer)
    CPU = Column(Integer)
    Memory = Column(Integer)
    Hard_disk = Column(Integer)
    VNC = Column(String(20))

class OSVersion(Base):

    __tablename__ = 'vmtools_osversion'

    id = Column(Integer,  primary_key=True)
    Version = Column(String(20))
    OSBit = Column(Integer)
