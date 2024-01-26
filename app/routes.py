from flask import request, jsonify
from . import app, get_db_cursor

employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }]


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks])

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

    try:
        schema = request.args.get('schema')
        table = request.args.get('table')
        limit = request.args.get('limit', default=10, type=int)
        skip = request.args.get('skip', default=0, type=int)

        cursor = get_db_cursor()
        query = f"SELECT * FROM hive_metastore.{schema}.{table} LIMIT {limit} OFFSET {skip}"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

