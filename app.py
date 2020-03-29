#!/usr/bin/python

from flask import *  # Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import json, os.path
from service import UserService
from service import MedicineService
from service import StockService
from exception import Error
from flask_cors import CORS, cross_origin
#import jwt

app = Flask(__name__)
Bootstrap(app)


#######################################
####     USER INTERFACE             ###
#######################################
@app.route('/user/me/<string:username>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_user_me(username):
    userService = UserService.UserService()
    response = userService.get_me(username)
    if response is None:
        abort(403)
    return jsonify(response), 200


@app.route('/user', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_user():
    try:
        if not request.json:
            abort(400)
        user_dict = request.json
        userService = UserService.UserService()
        id = userService.create_user(user_dict)

        return jsonify({'id': id}), 201
    except Error.InputError as err:
        return jsonify({'error': err.message}), 400


#@app.route('/user/login', methods=['POST'])
# @cross_origin() # allow all origins all methods.
#def login_user():
#    if not request.json:
#        abort(400)


#######################################
####     MEDICINE INTERFACE         ###
#######################################
@app.route('/medicine', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_all_medicine():
    medicineService = MedicineService.MedicineService()
    response = medicineService.get_all_medicine()
    if response is None or not response:
        return '', 204
    return jsonify(response), 200


@app.route('/medicine', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_medicine():
    if not request.json:
        abort(400)
    medicine_dict = request.json
    print(medicine_dict)
    medicineService = MedicineService.MedicineService()
    id = medicineService.create_medicine(medicine_dict)

    return jsonify({'id': id}), 201


@app.route('/medicine/<int:medicine_id>', methods=['PUT', 'GET'])
@cross_origin() # allow all origins all methods.
def medicine(medicine_id):
    if not medicine_id:
        abort(400)
    medicineService = MedicineService.MedicineService()
    try:
        # get medicine by id
        if request.method == 'GET':
            response = medicineService.get_medicine_by_id(medicine_id)
            if response is None or not response:
                return '', 204
        # update medicine
        elif request.method == 'PUT':
            if not request.json:
                abort(400)
            medicine_dict = request.json
            # print(medicine_dict)
            response = medicineService.update_medicine(medicine_id, medicine_dict)
        else:
            abort(400)
    except Error.NotFoundError as err:
        abort(404)

    return jsonify(response), 200


@app.route('/medicine/<int:medicine_id>/stock', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_medicine_stock(medicine_id):
    if not request.json or not medicine_id or not request.headers.get('Authorization'):
        abort(400)

    username = __username()
    stock_dict = request.json

    userService = UserService.UserService()
    me = userService.get_me(username)

    if not me:
        abort(404)

    medicineService = MedicineService.MedicineService()
    medicine = medicineService.get_medicine_by_id(medicine_id)

    if not medicine:
        abort(404)

    try:
        stockService = StockService.StockService()
        print(me)
        response = stockService.update_stock(medicine_id, me['user_id'], stock_dict)
        return jsonify(response), 200
    except Error.NotFoundError as err:
        abort(404)

#######################################
####     SUPPLIER INTERFACE         ###
#######################################
@app.route('/supplier/stock', methods=['GET'])
@cross_origin() # allow all origins all methods.
def supplier_stock():
    if not request.headers.get('Authorization'):
        abort(400)

    username = __username()
    userService = UserService.UserService()
    me = userService.get_me(username)

    if not me:
        abort(404)

    stockService = StockService.StockService()
    response = stockService.get_stock_by_user_id(me['user_id'])

    return jsonify(response), 200

#######################################
####     STOCK INTERFACE            ###
#######################################
@app.route('/stock/<int:medicine_id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_stock_by_medicine_id(medicine_id):
    if not medicine_id:
        abort(400)

    stockService = StockService.StockService()
    response = stockService.get_stock_by_medcine_id(medicine_id)

    return jsonify(response), 200


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error', 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error', 'Not found'}), 404)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error', 'Internal Server Error'}), 500)


def __username():
    token = request.headers.get('Authorization').replace('Bearer ', '')
    #if len(token) == 1:
    if token == '1':
        return 'apotheke_alpha'
    elif token == '2':
        return 'spital_beta'
    elif token == '3':
        return 'arzt_delta'
    else:
        abort(400)
    #else:
        #payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        #print(payload)


if __name__ == '__main__':
    app.run()
