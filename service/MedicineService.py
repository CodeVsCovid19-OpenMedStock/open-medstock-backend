#!/usr/bin/python

from database import Database
from service import SubstanceService
from service import ManufacturerService
from exception import Error


class MedicineService(object):
    def __init__(self):
        self.__db = Database.Database()
        self.__cur = self.__db.get_cursor()
        self.__substance = SubstanceService.SubstanceService(self.__db, self.__cur)
        self.__manufacturer = ManufacturerService.ManufacturerService(self.__db, self.__cur)

    def __del__(self):
        self.__db.close_connect()

    def get_all_medicine(self):
        self.__cur.execute("SELECT m.medicine_id, m.name, a.name as manufacturer, m.description, s.description as substance FROM medicine m, manufacturer a, substance s where m.manufacturer_id = a.manufacturer_id and m.substance_id = s.substance_id")
        result = self.__cur.fetchall()

        return result

    def get_all_medicine_with_stock(self):
        self.__cur.execute("SELECT distinct m.medicine_id, m.name, a.name as manufacturer, m.description, s.description as substance FROM medicine m, manufacturer a, substance s, stock t where m.manufacturer_id = a.manufacturer_id and m.substance_id = s.substance_id and m.medicine_id = t.medicine_id")
        result = self.__cur.fetchall()

        return result

    def get_medicine_by_id(self, medicine_id):
        print("search for medicine by id " + str(medicine_id))
        sql_query = "SELECT m.medicine_id, m.name, a.name as manufacturer, m.description, s.description as substance FROM medicine m, manufacturer a, substance s where m.manufacturer_id = a.manufacturer_id and m.substance_id = s.substance_id and m.medicine_id = %s"
        data_tuple = (medicine_id)
        self.__cur.execute(sql_query, data_tuple)
        return self.__cur.fetchone()


    def create_medicine(self, medicine_dict):
        substance = self.__substance.get_substance_by_description(medicine_dict['substance'])
        if not substance:
            print("Substance with name " + medicine_dict['substance'] + " not found -> create substance")
            substance_id = int(self.__substance.create_substance(medicine_dict['substance']))
        else:
            substance_id = int(substance['substance_id'])

        manufacturer = self.__manufacturer.get_manufacturer_by_name(medicine_dict['manufacturer'])
        if not manufacturer:
            print("Manufacturer with name " + medicine_dict['manufacturer'] + " not found -> create manufacturer")
            manufacturer_id = int(self.__manufacturer.create_manufacturer(medicine_dict['manufacturer']))
        else:
            manufacturer_id = int(manufacturer['manufacturer_id'])

        medicine_id = self.__insert_medicine(medicine_dict, substance_id, manufacturer_id)

        self.__db.commit()
        return medicine_id


    def update_medicine(self, medicine_id, medicine_dict):
        curr_medicine = self.get_medicine_by_id(medicine_id)
        if not curr_medicine:
            raise Error.NotFoundError('Medicine', 'Medicine by id not found')

        substance = self.__substance.get_substance_by_description(medicine_dict['substance'])
        if not substance:
            print("Substance with name " + medicine_dict['substance'] + " not found -> create substance")
            substance_id = int(self.__substance.create_substance(medicine_dict['substance']))
        else:
            substance_id = int(substance['substance_id'])

        manufacturer = self.__manufacturer.get_manufacturer_by_name(medicine_dict['manufacturer'])
        if not manufacturer:
            print("Manufacturer with name " + medicine_dict['manufacturer'] + " not found -> create manufacturer")
            manufacturer_id = int(self.__manufacturer.create_manufacturer(medicine_dict['manufacturer']))
        else:
            manufacturer_id = int(manufacturer['manufacturer_id'])

        self.__update_medicine(medicine_id, medicine_dict, substance_id, manufacturer_id)

        self.__db.commit()
        return self.get_medicine_by_id(medicine_id)


    def __insert_medicine(self, medicine_dict, substance_id, manufacturer_id):
        print("create new medicine " + medicine_dict['name'])
        sql_query = "INSERT INTO medicine(manufacturer_id, substance_id, name, description) VALUES(%s,%s,%s,%s)"
        data_tuple = (manufacturer_id, substance_id, medicine_dict['name'], medicine_dict['description'])
        print(data_tuple)
        self.__cur.execute(sql_query, data_tuple)
        if self.__cur.lastrowid:
            print('last insert id', self.__cur.lastrowid)
            id = self.__cur.lastrowid
        else:
            print('last insert id not found')
            id = None
        return id

    def __update_medicine(self, medicine_id, medicine_dict, substance_id, manufacturer_id):
        print("update medicine " + medicine_dict['name'])
        sql_query = "UPDATE medicine set manufacturer_id = %s, substance_id = %s, name = %s, description = %s WHERE medicine_id = %s"
        data_tuple = (manufacturer_id, substance_id, medicine_dict['name'], medicine_dict['description'], medicine_id)
        print(data_tuple)
        self.__cur.execute(sql_query, data_tuple)

