#!/usr/bin/python


class UnitService(object):
    def __init__(self, db, cur):
        self.__db = db
        self.__cur = cur


    def get_unit_by_description(self, unit):
        print("search for unit " + unit)
        sql_query = "SELECT unit_id, description FROM unit WHERE description = %s"
        data_tuple = (unit)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()

    def create_unit(self, unit_name):
        print("create new unit " + unit_name)
        sql_query = "INSERT INTO unit(description) VALUES(%s)"
        data_tuple = (unit_name)
        self.__cur.execute(sql_query, data_tuple)
        if self.__cur.lastrowid:
            print('last insert id', self.__cur.lastrowid)
            id = self.__cur.lastrowid
        else:
            print('last insert id not found')
            id = None
        return id