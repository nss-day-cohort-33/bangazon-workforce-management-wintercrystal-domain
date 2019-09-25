import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .list import create_department
from ..connection import Connection
from ..employees.employee_list import get_employees
from hrapp.models import model_factory, Department



def get_department(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id department_id,
            d.dept_name,
            d.budget
        FROM hrapp_department d
        WHERE d.id = ?
        """, (department_id,))

        return db_cursor.fetchone()



def department_details(request, department_id):
    # Still using if just incase request method ever can be something else (user can edit individual departments)
    if request.method == 'GET':
        department = get_department(department_id)
        all_employees = get_employees()
        dept_employees = []

        template_name = 'departments/details.html'
    # sending in list of employees that work in department
        for employee in all_employees:
            if employee.department_id_id is department_id:
                dept_employees.append(employee)
        context = {
            'department': department,
            'dept_employees' : dept_employees

        }
        return render(request, template_name, context)

