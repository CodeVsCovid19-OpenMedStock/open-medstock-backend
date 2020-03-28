#!/usr/bin/python

from database import Database
from exception import Error


class UserService:
    def __init__(self):
        self.__db = Database.Database()
        self.__cur = self.__db.get_cursor()

    def __del__(self):
        self.__db.close_connect()

    def get_me(self, username):
        sql_query = "SELECT u.user_id, u.username, u.institution_name, i.description, u.email_address, u.phone_number, u.mobile_number FROM user u, institution_type i where u.institution_type = i.institution_type_id and username = %s"
        data_tuple = (username)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchall()

    def create_user(self, user_dict):
        me = self.get_me(user_dict['username'])
        if me:
            raise Error.InputError('User', 'Username already exist')

        institution = self.__get_institution_by_type(user_dict['institution_type'])
        if not institution:
            print("institution_type with name " + user_dict['institution_type'] + " not found -> create institution_type")
            institution_type_id = int(self.__create_institution(user_dict['institution_type']))
        else:
            institution_type_id = int(institution['institution_type_id'])

        user_id = self.__insert_user(user_dict, institution_type_id)

        self.__db.commit()
        return user_id

    def __insert_user(self, user_dict, institution_type_id):
        print("create new user " + user_dict['username'])
        sql_query = "INSERT INTO user(username, institution_name, institution_type, contact_person, email_address, phone_number, mobile_number) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        data_tuple = (user_dict['username'], user_dict['institution_name'], institution_type_id, user_dict['contact_person'], user_dict['email_address'], user_dict['phone_number'], user_dict['mobile_number'])
        print(data_tuple)
        self.__cur.execute(sql_query, data_tuple)
        if self.__cur.lastrowid:
            print('last insert id', self.__cur.lastrowid)
            id = self.__cur.lastrowid
        else:
            print('last insert id not found')
            id = None
        return id

    def __get_institution_by_type(self, institution_type):
        print("get institution by name " + institution_type)
        sql_query = "SELECT institution_type_id, description FROM institution_type WHERE description = %s"
        data_tuple = (institution_type)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()

    def __create_institution(self, institution_type):
        print("create new institution " + institution_type)
        sql_query = "INSERT INTO institution_type(description) VALUES(%s)"
        data_tuple = (substance_name)
        self.__cur.execute(sql_query, data_tuple)
        if self.__cur.lastrowid:
            print('last insert id', self.__cur.lastrowid)
            id = self.__cur.lastrowid
        else:
            print('last insert id not found')
            id = None
        return id