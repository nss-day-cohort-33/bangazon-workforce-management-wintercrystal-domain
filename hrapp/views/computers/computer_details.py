import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer, Employee
from hrapp.models import model_factory
from ..connection import Connection


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
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
            where t.unassigned_date is NULL
            """)

            data_set = db_cursor.fetchall()
            context = {
                'computer': computer,
                'employees': data_set
            }
        template_name = 'computers/computer_details.html'
        return render(request, template_name, context)

    # elif request.method == 'POST':
    #     form_data = request.POST

    #     # Check if this POST is for editing a book
    #     if (
    #         "actual_method" in form_data
    #         and form_data["actual_method"] == "PUT"
    #     ):
    #         with sqlite3.connect(Connection.db_path) as conn:
    #             db_cursor = conn.cursor()

    #             db_cursor.execute("""
    #             UPDATE libraryapp_book
    #             SET title = ?,
    #                 auther = ?,
    #                 ISBN_number = ?,
    #                 year_published = ?,
    #                 location_id = ?
    #             WHERE id = ?
    #             """,
    #             (
    #                 form_data['title'],
    #                 form_data['auther'],
    #                 form_data['ISBN_number'],
    #                 form_data['year_published'],
    #                 form_data['location'],
    #                 book_id,
    #             ))

    #         return redirect(reverse('libraryapp:books'))

    #     # Check if this POST is for deleting a book
    #     if (
    #         "actual_method" in form_data
    #         and form_data["actual_method"] == "DELETE"
    #     ):
    #         with sqlite3.connect(Connection.db_path) as conn:
    #             db_cursor = conn.cursor()

    #             db_cursor.execute("""
    #                 DELETE FROM libraryapp_book
    #                 WHERE id = ?
    #             """, (book_id,))

    #         return redirect(reverse('libraryapp:books'))