#!/usr/bin/python

from database import Database


class UserService:
    def __init__(self):
        self.__db = Database.Database()
        self.__cur = self.__db.get_cursor()

    def __del__(self):
        self.__db.close_connect()

    def get_me(self, username):
        sql_query = "SELECT u.username, u.institution_name, i.description, u.email_address, u.phone_number, u.mobil_number FROM user u, institution_type i where u.institution_type = i.instituttion_type_id and username = %s"
        data_tuple = (username)
        self.__cur.execute(sql_query, data_tuple)
        result = self.__cur.fetchall()

        return result