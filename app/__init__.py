from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from databricks import sql
import os

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def get_db_cursor():
    connection = sql.connect(
        server_hostname="adb-5030209865440091.11.azuredatabricks.net",
        http_path="/sql/1.0/warehouses/0e4e7b6ae372d919",
        access_token=os.getenv("DATABRICKS_ACCESS_TOKEN")
    )
    cursor = connection.cursor()
    cursor.execute("SET STATEMENT_TIMEOUT = 10")  # Set timeout to 20 seconds
    return cursor

from . import routes
