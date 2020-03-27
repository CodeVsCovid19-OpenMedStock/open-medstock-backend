#!/usr/bin/python

from flask import * #Flask, render_template, request, redirect
import pymysql
from flask_bootstrap import Bootstrap
from configparser import ConfigParser
import json, os.path

app = Flask(__name__)
Bootstrap(app)


class Database:
    def __init__(self):
        config = ConfigParser()
        config.read('config.properties')
        host = config['DatabaseSection']['database.host']
        user = config['DatabaseSection']['database.user']
        password = config['DatabaseSection']['database.password']
        db = config['DatabaseSection']['database.dbname']
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
