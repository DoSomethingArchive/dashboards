import sys
#get parent path and set path to /env
parent_path = os.sep.join(os.getcwd().split(os.sep)[:-1])
path_env = parent_path + '/env'
sys.path.insert(0, path_env)
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

#run after updates made to models.py
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))