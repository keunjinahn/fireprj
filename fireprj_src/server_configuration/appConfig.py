#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib


class CommonConfig(object):
    # User Type
    API_HEADERS = {'Content-type': 'application/json'}
    SMTP_SENDER = "akj2996@daum.net"
    SMTP_ADDR = "smtp.daum.net"
    SMTP_PORT = 465
    SMTP_LOGIN_ID = "akj2996"
    SMTP_LOGIN_PW = "deepir12!@"
#     SMTP_SENDER = "sosedu@koies.or.kr"
#     SMTP_ADDR = "gw.koies.or.kr"
#     SMTP_PORT = 25
#     SMTP_LOGIN_ID = "sosedu"
#     SMTP_LOGIN_PW = "111111"

class DevelopmentConfig(CommonConfig):
    DATABASE = "typhoon"
    BIND_PORT = 8081
    #SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/edufadb'
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/edufadb'
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


