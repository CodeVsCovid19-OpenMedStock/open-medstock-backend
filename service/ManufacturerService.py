#!/usr/bin/python


class ManufacturerService(object):
    def __init__(self, db, cur):
        self.__db = db
        self.__cur = cur


    def get_manufacturer_by_name(self, manufacturer):
        print("search for manufacturer " + manufacturer)
        sql_query = "SELECT manufacturer_id, name FROM manufacturer WHERE name = %s"
        data_tuple = (manufacturer)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()

    def create_manufacturer(self, manufacturer_name):
        print("create new manufacturer " + manufacturer_name)
        sql_query = "INSERT INTO manufacturer(name) VALUES(%s)"
        data_tuple = (manufacturer_name)
        self.__cur.execute(sql_query, data_tuple)
        if self.__cur.lastrowid:
            print('last insert id', self.__cur.lastrowid)
            id = self.__cur.lastrowid
        else:
            print('last insert id not found')
            id = None
        return id