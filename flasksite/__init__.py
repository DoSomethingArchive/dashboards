from flask import Flask, request, jsonify
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors
from MySQLdb.constants import FIELD_TYPE
from random import choice as choice
from cache import cache
import json
import os
import sys
#get current dir and set path for env dir so can import config vars
current_path = os.getcwd()
path_env = current_path + '/env'
sys.path.insert(0, path_env)
#also add parent path
parent_path = os.sep.join(os.getcwd().split(os.sep)[:-1])
parent_path_env = parent_path + '/env'
sys.path.insert(0, parent_path_env)
from config import basedir

#initialize app
app = Flask(__name__)
app.config.from_pyfile('../env/config.py')
app.config['CACHE_TYPE'] = 'simple'

#db settings
db = SQLAlchemy(app)

#login settings
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
cache.init_app(app)

#MySQL conversions
my_conv = { FIELD_TYPE.LONG: int }

#Connect to MySQL
def openDB():
  db = MySQLdb.connect(host=app.config['HOST'], #hostname
                    user=app.config['USER'], # username
                    passwd=app.config['PW'], # password
                    db=app.config['DB'], # db
                    conv=my_conv,# datatype conversions
                    cursorclass=MySQLdb.cursors.DictCursor)
  cur = db.cursor()
  return cur

#handles quering mysql, output to json
def queryToData(cursor_obj,query,index=None,keyname=None,need_json=None):

	if index==None and keyname==None and need_json==None:

		cursor_obj.execute(query)
		data = cursor_obj.fetchall()
		data_f = json.dumps(data)

		return data_f

	if index!=None and keyname!=None and need_json==None:

		cursor_obj.execute(query)
		data = cursor_obj.fetchall()[index][keyname]
		data_f = json.dumps(data)

		return data_f

	if index==None and keyname==None and need_json!=None:

		cursor_obj.execute(query)
		data = cursor_obj.fetchall()

		return data

import views, models
if __name__ == '__main__':
  app.run()
