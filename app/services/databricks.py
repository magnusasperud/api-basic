from app import app
from .auth_service import token_required
from app.database import get_db_cursor
from flask import request, jsonify


@app.route('/get_data', methods=['GET'])
@token_required
def get_data_from_databricks():
    schema = request.args.get('schema')
    table = request.args.get('table')
    limit = request.args.get('limit', default=10, type=int)
    skip = request.args.get('skip', default=0, type=int)

    # Input validation
    if not schema or not table or not isinstance(schema, str) or not isinstance(table, str) or limit < 0 or skip < 0:
        return jsonify({'error': 'Invalid input parameters'}), 400

    try:
        with get_db_cursor() as cursor:
            query = f"SELECT * FROM hive_metastore.{schema}.{table} LIMIT {limit} OFFSET {skip}"
            cursor.execute(query, (schema, table, limit, skip))
            data = cursor.fetchall()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500