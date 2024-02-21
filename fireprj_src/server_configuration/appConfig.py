#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib


class CommonConfig(object):
    # User Type
    API_HEADERS = {'Content-type': 'application/json'}

class DevelopmentConfig(CommonConfig):
    DATABASE = "typhoon"
    BIND_PORT = 8081
    # SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/edufadb'
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/fireprjdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {'Content-type': 'application/json'}
    UPLOAD_FOLDER = "./"


class ProductionConfig(CommonConfig):
    DATABASE = "typhoon"
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:edufa12!@127.0.0.1/edufadb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {'Content-type': 'application/json'}
    UPLOAD_FOLDER = "./"


