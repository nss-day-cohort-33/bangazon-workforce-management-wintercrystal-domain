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
            e.department_id_id,
            d.dept_name
        from hrapp_employee e
        left join hrapp_department d on d.id = e.department_id_id
        """)
        return db_cursor.fetchall()

def employee_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Employee)
            db_cursor = conn.cursor()
            employees = get_employees()

            dataset = db_cursor.fetchall()

        template = 'employees/employees_list.html'
        context = {
            'employees': employees
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST
        if  "actual_method" not in form_data:
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

        if (
                    "actual_method" in form_data
                    and form_data["actual_method"] == "Add It"
                ):
                form_data = request.POST

                with sqlite3.connect(Connection.db_path) as conn:
                    db_cursor = conn.cursor()

                    db_cursor.execute("""
                    UPDATE hrapp_employee
                    SET
                        first_name = ?,
                        last_name = ?,
                        is_supervisor = ?,
                        department_id_id = ?
                    WHERE id = ?;
                    """,
                    (form_data['first_name'], form_data['last_name'], form_data['supervisor'], form_data['department'], form_data["employee_id"]))

                return redirect(reverse('hrapp:employee_details', args = [form_data["employee_id"]]))


