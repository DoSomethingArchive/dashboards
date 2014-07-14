from flask import Flask, request, jsonify
import MySQLdb
import MySQLdb.converters
import MySQLdb.cursors
from MySQLdb.constants import FIELD_TYPE
from random import choice as choice
import json

app = Flask(__name__)

app.config.from_pyfile('../env/config.cfg')
my_conv = { FIELD_TYPE.LONG: int }

def openDB():
  db = MySQLdb.connect(host=app.config['HOST'], #hostname
                    user=app.config['USER'], # username
                    passwd=app.config['PW'], # password
                    db=app.config['DB'], # db
                    conv=my_conv,# datatype conversions
                    cursorclass=MySQLdb.cursors.DictCursor)
  cur = db.cursor()
  return cur


import views
if __name__ == '__main__':
  app.run()
