import sqlite3
from django.shortcuts import render
from datetime import date
from django.urls import reverse
from django.shortcuts import redirect
from hrapp.models import Employee
from hrapp.models import model_factory
from hrapp.models import Employee
from ..connection import Connection

def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            e.department_id_id
        from hrapp_employee e
        """)
        return db_cursor.fetchall()

def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Employee)
            db_cursor = conn.cursor()
            employees = get_employees()

            # TODO: Add to query: e.department,
            db_cursor.execute("""
            select
                c.id relationId,
                c.computer_id_id,
                c.employee_id_id,
                cc.id computerId,
                cc.make,
                cc.model
            from hrapp_employeecomputer c
            join hrapp_computer cc on cc.id = c.computer_id_id
            where c.unassigned_date is NULL
            """)

            dataset = db_cursor.fetchall()

        template = 'employees/employees_list.html'
        context = {
            'computers': dataset,
            'employees': employees
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            start_date = date.today().strftime("%Y/%m/%d")

            db_cursor.execute("""
            INSERT INTO hrapp_employee
            (
                first_name, last_name, start_date, is_supervisor, department_id_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (form_data['first_name'], form_data['last_name'], start_date, form_data["supervisor"], form_data["department"] ))

        return redirect(reverse('hrapp:employee_list'))


