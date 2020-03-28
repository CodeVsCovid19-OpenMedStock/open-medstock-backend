#!/usr/bin/python

from database import Database


class SubstanceService(object):
    def __init__(self, db, cur):
        self.__db = db
        self.__cur = cur


    def get_substance_by_description(self, substance):
        print("search for substance " + substance)
        sql_query = "SELECT substance_id, description FROM substance WHERE description = %s"
        data_tuple = (substance)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()

    def create_substance(self, substance_name):
        print("create new substance " + substance_name)
        sql_query = "INSERT INTO substance(description) VALUES(%s)"
        data_tuple = (substance_name)
        self.__cur.execute(sql_query, data_tuple)
        if self.__cur.lastrowid:
            print('last insert id', self.__cur.lastrowid)
            id = self.__cur.lastrowid
        else:
            print('last insert id not found')
            id = None
        return id