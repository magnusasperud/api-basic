from databricks import sql
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def get_db_cursor():

    access_token = os.getenv("databricks_token")
    server_hostname = os.getenv("server_hostname")
    http_path = os.getenv("http_path")

    connection = sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token
    )
    cursor = connection.cursor()
    cursor.execute("SET STATEMENT_TIMEOUT = 200")  # Set timeout to 20 seconds
    return cursor
