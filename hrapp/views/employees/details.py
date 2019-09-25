import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee
from hrapp.models import Department
from hrapp.models import model_factory
from ..connection import Connection


def get_employee(employee_id):
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
            ec.id relationId,
            ec.computer_id_id,
            ec.employee_id_id,
            c.make,
            c.model,
            d.dept_name
        from hrapp_employee e
        left join hrapp_department d on d.id = e.department_id_id
        left join hrapp_employeecomputer ec on ec.employee_id_id = e.id
        left join hrapp_computer c on c.id = ec.computer_id_id
        where e.id = ?
        """, (employee_id,))

        return db_cursor.fetchone()

def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        select
            d.id,
            d.dept_name,
            d.budget
        from hrapp_department d
        """)
        return db_cursor.fetchall()

@login_required
def employee_details(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)

        template = 'employees/details.html'
        context = {
            'employee': employee
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for deleting a book
        #
        # Note: You can use parenthesis to break up complex
        #       `if` statements for higher readability
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_employee
                WHERE id = ?
                """, (employee_id,))

            return redirect(reverse('hrapp:employee_list'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "EDIT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                employee = get_employee(employee_id)

                departments = get_departments()

                template = "employees/form.html"
                context = {
                    'employee': employee,
                    'departments': departments
                }

            return render(request, template, context)

