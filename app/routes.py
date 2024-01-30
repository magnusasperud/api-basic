from flask import request, jsonify
from . import app
from app.database import get_db_cursor
import jwt
import datetime
from functools import wraps

employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }, { 'id': 4, 'name': 'Magnus' } ]

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employee/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    global employees
    employee = next((emp for emp in employees if emp['id'] == emp_id), None)

    if employee:
        employees = [emp for emp in employees if emp['id'] != emp_id]
        return jsonify({'message': 'Employee deleted successfully'}), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if ' ' in auth_header:
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/token', methods=['POST'])
def generate_token():
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(
        {
            'exp': expiration
        }, 
        app.config['SECRET_KEY'], 
        algorithm="HS256"
    )

    return jsonify({
        'token': token,
        'expiration': expiration.strftime("%Y-%m-%d %H:%M:%S")
    })

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