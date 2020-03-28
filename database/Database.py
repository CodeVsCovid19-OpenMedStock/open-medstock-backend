#!/usr/bin/python

import pymysql
from configparser import ConfigParser


class Database(object):
    def __init__(self):
        config = ConfigParser()
        config.read('./config.properties')
        print("try to connect to the database")
        host = str(config.get('DatabaseSection', 'database.host'))
        port = int(config.get('DatabaseSection', 'database.port'))
        user = str(config.get('DatabaseSection', 'database.user'))
        password = str(config.get('DatabaseSection', 'database.password'))
        db = str(config.get('DatabaseSection', 'database.dbname'))
        host = "sql7.freemysqlhosting.net"
        user = "sql7329640"
        password = "Q6FRAYZr56"
        db = "sql7329640"
        print(host, user, password, db)
        self.__con = pymysql.connect(host=host, user=user, password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
        print("database successfully connected")
        self.__cur = self.__con.cursor()

    def get_cursor(self):
        return self.__cur

    def get_connection(self):
        return self.__con

    def close_connect(self):
        self.__con.close()

    def commit(self):
        self.__con.commit()
