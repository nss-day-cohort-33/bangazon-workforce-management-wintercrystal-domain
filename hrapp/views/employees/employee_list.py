import sqlite3
from django.shortcuts import render
from hrapp.models import Employee
from hrapp.models import model_factory
from hrapp.models import Employee
from ..connection import Connection
import datetime


def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Employee)
            db_cursor = conn.cursor()

            # TODO: Add to query: e.department,
            db_cursor.execute("""
            select
                e.id,
                e.first_name,
                e.last_name,
                e.start_date,
                e.is_supervisor,
                e.department_id_id,
                c.id relationId,
                cc.id computerId,
                cc.make,
                cc.model
            from hrapp_employee e
            join hrapp_employeecomputer c on c.employee_id_id = e.id
            join hrapp_computer cc on cc.id = c.computer_id_id
            where c.unassigned_date is NULL
            """)

            dataset = db_cursor.fetchall()

        template = 'employees/employees_list.html'
        context = {
            'employees': dataset
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_department
            (
                first_name, last_name, start_date, is_supervisor, department_id_id
            )
            VALUES (?, ?)
            """,
            (form_data['first_name'], form_data['last_name'], ))

        return redirect(reverse('libraryapp:libraries'))


