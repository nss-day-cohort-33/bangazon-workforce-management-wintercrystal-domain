import sqlite3
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Computer
from hrapp.models import model_factory
from ..connection import Connection



def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            conn.row_factory = model_factory(Computer)

            db_cursor = conn.cursor()
            db_cursor.execute("""
            select
                c.id,
                c.make,
                c.model,
                c.purchase_date,
                c.decommission_date
            from hrapp_computer c
            """)

            all_computers = db_cursor.fetchall()

        template = 'computers/computer_list.html'
        context = {
            'all_computers': all_computers
        }

        return render(request, template, context)

    # elif request.method == 'POST':
    #     form_data = request.POST

    #     with sqlite3.connect(Connection.db_path) as conn:
    #         db_cursor = conn.cursor()

    #         db_cursor.execute("""
    #         INSERT INTO hrapp_computer
    #         (
    #             title, auther, ISBN_number,
    #             year_published, location_id, librarian_id
    #         )
    #         VALUES (?, ?, ?, ?, ?, ?)
    #         """,
    #         (form_data['title'], form_data['auther'],
    #             form_data['ISBN_number'], form_data['year_published'],
    #             request.user.librarian.id, form_data["location"]))

    #     return redirect(reverse('libraryapp:books'))