from databricks import sql
import os

def get_db_cursor():

    access_token = os.getenv("p-ofnanlt-databricks_token")
    if not access_token:
        raise ValueError("Missing environment variable: 'p-ofnanlt-databricks_token'")
    connection = sql.connect(
        server_hostname="adb-5030209865440091.11.azuredatabricks.net",
        http_path="/sql/1.0/warehouses/0e4e7b6ae372d919",
        access_token=access_token
    )
    cursor = connection.cursor()
    cursor.execute("SET STATEMENT_TIMEOUT = 200")  # Set timeout to 20 seconds
    return cursor
