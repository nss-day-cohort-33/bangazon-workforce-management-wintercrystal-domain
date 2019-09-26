import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from hrapp.models import Employee
from hrapp.models import Training
from hrapp.models import EmployeeTraining
from hrapp.models import Department
from hrapp.models import model_factory
from ..connection import Connection

def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory =model_factory(Employee)
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

def get_training(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(EmployeeTraining)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            et.id,
            et.employee_id_id,
            COUNT(training_id_id) as booked,
            et.training_id_id,
            t.title,
            t.start_date,
            t.end_date,
            t.capacity
        from hrapp_employeetraining et
        left join hrapp_training t on t.id = et.training_id_id
        where et.employee_id_id = ?
        group by training_id_id
        """, (employee_id,))

        return db_cursor.fetchall()

def get_trainings():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Training)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            t.id,
            t.title,
            t.start_date,
            t.end_date,
            t.capacity
        from hrapp_training t
        """)

        return db_cursor.fetchall()

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
        trainings = get_training(employee_id)

        past_trainings = list()
        plan_trainings = list()

        for training in trainings:
            if training.start_date is not None:
                if datetime.today() > datetime.strptime(training.start_date, '%Y/%m/%d'):
                    past_trainings.append(training)
                else:
                    plan_trainings.append(training)

        template = 'employees/details.html'
        context = {
            'employee': employee,
            'past_trainings': past_trainings,
            'plan_trainings': plan_trainings
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

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "assignTraining"
        ):
            with sqlite3.connect(Connection.db_path) as conn:

                assigned = list()
                allowed_training = list()

                all_trainings = get_trainings()
                trainings = get_training(employee_id)



                for training in trainings:
                    assigned.append(training.training_id_id)

                for training in all_trainings:
                    if training.id not in assigned:
                        allowed_training.append(training)



                template = "employees/training.html"
                context = {
                    'employee_id': employee_id,
                    'booked_training': allowed_training
                }

            return render(request, template, context)

