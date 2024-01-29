from flask import request, jsonify
from . import app
from app.database import get_db_cursor

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

@app.route('/get_data', methods=['GET'])
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
            query = "SELECT * FROM hive_metastore.%s.%s LIMIT %s OFFSET %s"
            cursor.execute(query, (schema, table, limit, skip))
            data = cursor.fetchall()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500

