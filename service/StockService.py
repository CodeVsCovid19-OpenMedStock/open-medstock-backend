#!/usr/bin/python

from database import Database
from service import UnitService
from exception import Error


class StockService(object):
    def __init__(self):
        self.__db = Database.Database()
        self.__cur = self.__db.get_cursor()
        self.__unit = UnitService.UnitService(self.__db, self.__cur)

    def __del__(self):
        self.__db.close_connect()

    def get_stock_by_medcine_id(self, medicine_id):
        print("search for medicine by id " + str(medicine_id))
        sql_query = "SELECT m.medicine_id, m.name, a.name as manufacturer, m.description, s.description as substance FROM medicine m, manufacturer a, substance s where m.manufacturer_id = a.manufacturer_id and m.substance_id = s.substance_id and m.medicine_id = %s"
        data_tuple = (medicine_id)
        self.__cur.execute(sql_query, data_tuple)
        medicine = self.__cur.fetchone()

        sql_query = "SELECT distinct u.user_id, u.username, u.institution_name, i.description, u.email_address, u.phone_number, u.mobile_number FROM user u, institution_type i, stock s where u.institution_type = i.institution_type_id and u.user_id = s.supplier_id and s.medicine_id = %s"
        data_tuple = (medicine_id)
        self.__cur.execute(sql_query, data_tuple)
        user = self.__cur.fetchall()
        stock_list = list()
        # go through the user list and read stock per user and add the medicine data to one dictionary list
        for oneuser in user:
            sql_query = "SELECT s.gtin, s.amount_packages, s.amount_units, s.unit_size, u.description as unit FROM stock s, unit u where s.unit_id = u.unit_id and s.medicine_id = %s and s.supplier_id = %s"
            data_tuple = (medicine_id, oneuser['user_id'])
            self.__cur.execute(sql_query, data_tuple)
            stock = self.__cur.fetchall()
            med = medicine.copy()
            med['stock'] = stock
            oneuser.pop('user_id')
            stock_dict = {"supplier": oneuser, "medicine": med}
            stock_list.append(stock_dict)
        return stock_list

    def get_stock_by_user_id(self, user_id, medicine_id):
        print("search stock for user_id " + str(user_id))
        sql_query = "SELECT distinct m.medicine_id, m.name, a.name as manufacturer, m.description, s.description as substance FROM medicine m, manufacturer a, substance s, stock t where m.manufacturer_id = a.manufacturer_id and m.substance_id = s.substance_id and m.medicine_id = t.medicine_id and t.supplier_id = %s"
        data_tuple = (user_id)
        self.__cur.execute(sql_query, data_tuple)
        medicine = self.__cur.fetchall()

        stock_list = list()
        # go through the medicine list and read stock per user and add the medicine with stock data to one dictionary list
        for med in medicine:
            sql_query = "SELECT s.gtin, s.amount_packages, s.amount_units, s.unit_size, u.description as unit FROM stock s, unit u where s.unit_id = u.unit_id and s.medicine_id = %s and s.supplier_id = %s"
            data_tuple = (med['medicine_id'], user_id)
            self.__cur.execute(sql_query, data_tuple)
            stock = self.__cur.fetchall()
            if not medicine_id:
                stock_dict = {"medicine": med, "stock": stock}
                stock_list.append(stock_dict)
            elif medicine_id == med['medicine_id']:
                stock_list = {"medicine": med, "stock": stock}
        return stock_list

    def update_stock(self, medicine_id, user_id, stock_dict):
        print("search stock for user_id " + str(user_id))
        stock_response = list()
        for stock_element in stock_dict:
            print(stock_element)
            unit = self.__unit.get_unit_by_description(stock_element['unit'])
            if not unit:
                print("Unit with name " + stock_element['unit'] + " not found -> create unit")
                unit_id = int(self.__unit.create_unit(stock_element['substance']))
            else:
                unit_id = int(unit['unit_id'])

            stock = self.__get_stock(medicine_id, user_id, stock_element['gtin'])
            if not stock:
                self.__insert_stock(medicine_id, user_id, unit_id, stock_element)
            else:
                self.__update_stock(medicine_id, user_id, unit_id, stock_element)

            stock_response.append(self.__get_stock(medicine_id, user_id, stock_element['gtin']))

        self.__delete_stock(stock_dict)

        self.__db.commit()
        return stock_response

    def __insert_stock(self, medicine_id, user_id, unit_id, stock_dict):
        print("create new stock " + str(medicine_id) + " " + str(user_id))
        sql_query = "INSERT INTO stock(supplier_id, medicine_id, gtin, amount_packages, amount_units, unit_size, unit_id) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        data_tuple = (user_id, medicine_id, stock_dict['gtin'], stock_dict['amount_packages'], stock_dict['amount_units'], stock_dict['unit_size'], unit_id)
        print(data_tuple)
        self.__cur.execute(sql_query, data_tuple)

    def __update_stock(self, medicine_id, user_id, unit_id, stock_dict):
        print("update stock " + str(medicine_id) + " " + str(user_id))
        sql_query = "UPDATE stock SET amount_packages = %s, amount_units = %s, unit_size = %s, unit_id = %s WHERE medicine_id = %s and supplier_id = %s and gtin = %s"
        data_tuple = (stock_dict['amount_packages'], stock_dict['amount_units'], stock_dict['unit_size'], unit_id, medicine_id, user_id, stock_dict['gtin'])
        print(data_tuple)
        self.__cur.execute(sql_query, data_tuple)

    def __delete_stock(self, stock_dict):
        self.__cur.execute("SELECT s.gtin FROM stock s")
        gtin = [item['gtin'] for item in self.__cur.fetchall()]
        print(gtin)
        for stock in stock_dict:
            if stock['gtin'] in gtin:
                gtin.remove(stock['gtin'])

        print("gtin to be deleted " + str(gtin))
        for element in gtin:
            sql_query = "DELETE FROM stock WHERE gtin = %s"
            data_tuple = (element)
            self.__cur.execute(sql_query, data_tuple)

    def __get_stock(self, medicine_id, user_id, gtin):
        sql_query = "SELECT s.supplier_id, s.medicine_id, s.gtin, s.amount_packages, s.amount_units, s.unit_size, u.description as unit FROM stock s, unit u WHERE s.unit_id = u.unit_id and s.medicine_id = %s and s.supplier_id = %s and s.gtin = %s"
        data_tuple = (medicine_id, user_id, gtin)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()
