#!/usr/bin/python

from flask import *  # Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import json, os.path
from service import UserService
from service import MedicineService
from service import StockService
from exception import Error

app = Flask(__name__)
Bootstrap(app)


#######################################
####     USER INTERFACE             ###
#######################################
@app.route('/user/me/<string:username>', methods=['GET'])
def get_user_me(username):
    userService = UserService.UserService()
    response = userService.get_me(username)
    if response is None:
        abort(403)
    return jsonify(response), 200


@app.route('/user', methods=['POST'])
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
#def login_user():
#    if not request.json:
#        abort(400)


#######################################
####     MEDICINE INTERFACE         ###
#######################################
@app.route('/medicine', methods=['GET'])
def get_all_medicine():
    medicineService = MedicineService.MedicineService()
    response = medicineService.get_all_medicine()
    if response is None or not response:
        return '', 204
    return jsonify(response), 200


@app.route('/medicine', methods=['POST'])
def create_medicine():
    if not request.json:
        abort(400)
    medicine_dict = request.json
    print(medicine_dict)
    medicineService = MedicineService.MedicineService()
    id = medicineService.create_medicine(medicine_dict)

    return jsonify({'id': id}), 201


@app.route('/medicine/<int:medicine_id>', methods=['PUT'])
def update_medicine(medicine_id):
    try:
        if not request.json or not medicine_id:
            abort(400)
        medicine_dict = request.json
        print(medicine_dict)
        medicineService = MedicineService.MedicineService()
        response = medicineService.update_medicine(medicine_id, medicine_dict)
        return jsonify(response), 200
    except Error.NotFoundError as err:
        abort(404)


#######################################
####     STOCK INTERFACE            ###
#######################################
@app.route('/stock/<int:medicine_id>', methods=['GET'])
def get_stock_by_medicine_id(medicine_id):
    if not medicine_id:
        abort(400)




@app.route('/')
def hello_world():
    return 'Hello World!'


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error', 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error', 'Not found'}), 404)


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error', 'Internal Server Error'}), 500)


if __name__ == '__main__':
    app.run()
