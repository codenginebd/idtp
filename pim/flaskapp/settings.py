import os
import dj_database_url

print(dj_database_url)

DEBUG = True

db_path = os.path.abspath(".")
db_path = os.path.join(db_path, "db.sqlite3")

DATABASES = { 'default': dj_database_url.config(default='sqlite:////' + db_path) }

INSTALLED_APPS = ( 'lib', 'pim')

SECRET_KEY = '233py4*7g63%1kjoroqfb^l4*964!sa=n*yfi4@u4u^ofb94*h'