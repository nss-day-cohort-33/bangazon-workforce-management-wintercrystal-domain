import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, Employee
from hrapp.models import model_factory
from datetime import date
from ..connection import Connection


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.make,
            c.model,
            c.purchase_date,
            c.decommission_date
        FROM hrapp_computer c
        WHERE c.id = ?
        """, (computer_id,))

        return db_cursor.fetchone()



def computer_details(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)
        data_set = None
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Computer)
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                t.id relationId,
                t.computer_id_id,
                t.employee_id_id,
                e.id employee_id,
                e.first_name,
                e.last_name
            from hrapp_employeecomputer t
            left join hrapp_employee e on e.id = t.employee_id_id
            where t.unassigned_date is NULL and computer_id_id is ?
            """,(computer_id,))

            data_set = db_cursor.fetchall()
            context = {
                'computer': computer,
                'employees': data_set
            }
        template_name = 'computers/computer_details.html'
        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                decommission_date = date.today().strftime("%Y/%m/%d")

                db_cursor.execute("""
                UPDATE hrapp_computer
                SET decommission_date = ?
                WHERE id = ?
                """,
                (
                    decommission_date, computer_id
                ))

            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                unassigned_date = date.today().strftime("%Y/%m/%d")

                db_cursor.execute("""
                UPDATE hrapp_employeecomputer
                SET unassigned_date = ?
                WHERE computer_id_id = ? and unassigned_date is NULL
                """,
                (
                    unassigned_date, computer_id
                ))
            return redirect(reverse('hrapp:computer_list'))

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_computer
                    WHERE id = ?
                """, (computer_id,))

            return redirect(reverse('hrapp:computer_list'))