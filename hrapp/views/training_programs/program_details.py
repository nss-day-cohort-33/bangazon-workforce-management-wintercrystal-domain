import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from hrapp.models import Training, Employee
from hrapp.models import model_factory
from ..connection import Connection


def get_programs(program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Training)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.title,
            t.start_date,
            t.end_date,
            t.capacity
        FROM hrapp_training t
        WHERE t.id = ?
        """, (program_id,))

        return db_cursor.fetchone()

def get_employees(program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.first_name,
            e.last_name
        FROM hrapp_employee e
        JOIN hrapp_employeetraining et
        ON et.employee_id_id = e.id
        WHERE et.training_id_id = ?
        """, (program_id,))

        return db_cursor.fetchall()

@login_required
def program_details(request, program_id):
    if request.method == 'GET':
        program = get_programs(program_id)
        employees = get_employees(program_id)

        template = 'training_programs/program_detail.html'
        context = {
            'Program': program,
            'Employees': employees
        }

        return render(request, template, context)

    if request.method == 'POST':
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
                DELETE FROM hrapp_training
                WHERE id = ?
                """, (program_id,))

            return redirect(reverse('hrapp:training_list'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "EDIT"
        ):
            program = get_programs(program_id)
            start_date = datetime.datetime.strptime(program.start_date, '%Y/%m/%d').strftime('%Y-%m-%d')
            end_date = datetime.datetime.strptime(program.end_date, '%Y/%m/%d').strftime('%Y-%m-%d')

            template = 'training_programs/training_form.html'
            context = {
                'Program': program,
                'Start': start_date,
                'End': end_date
            }

            return render(request, template, context)

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_training
                SET
                    title = ?,
                    start_date = ?,
                    end_date = ?,
                    capacity = ?
                WHERE id = ?
                """,
                (form_data['title'], datetime.datetime.strptime(form_data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d'), datetime.datetime.strptime(form_data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d'), form_data['capacity'], program_id ))

            return redirect(reverse('hrapp:program', args = [form_data["program_id"]]))