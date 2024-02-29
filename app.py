from flask import Flask,jsonify, request
import psycopg2

import os
from db import *
from util.blueprints import register_blueprints


app = Flask(__name__)

app_host = os.getenv('APP_HOST')
app_port = os.getenv('APP_PORT')


database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://127.0.0.1:5432/{database_name}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app,db)

def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created succesfully")

register_blueprints(app)

if __name__ == '__main__':
    create_tables()
    app.run(host=app_host, port=app_port, debug=True)