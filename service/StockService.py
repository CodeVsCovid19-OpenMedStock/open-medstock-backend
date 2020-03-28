#!/usr/bin/python

from database import Database
from exception import Error


class StockService(object):
    def __init__(self):
        self.__db = Database.Database()
        self.__cur = self.__db.get_cursor()

    def __del__(self):
        self.__db.close_connect()

    def get_stock_by_medcine_id(self, medicine_id):
        print("search for medicine by id " + str(medicine_id))
        sql_query = "SELECT m.medicine_id, m.name, a.name as manufacturer, m.description, s.description as substance FROM medicine m, manufacturer a, substance s where m.manufacturer_id = a.manufacturer_id and m.substance_id = s.substance_id and m.medicine_id = %s"
        data_tuple = (medicine_id)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()
        pass