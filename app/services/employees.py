from flask import request, jsonify
from app import app

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