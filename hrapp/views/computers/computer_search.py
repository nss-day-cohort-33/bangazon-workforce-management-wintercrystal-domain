import sqlite3
from django.shortcuts import render
from ..connection import Connection
from hrapp.models import model_factory
from hrapp.models import Computer


def computer_search(request):

    if request.method == 'POST':
        form_data = request.POST
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
            computer_results = []

            for computer in all_computers:
                if form_data["search"].lower() in computer.make.lower() or form_data["search"].lower() in computer.model.lower():
                    computer_results.append(computer)

            template = 'computers/computer_list.html'
            context = {
                'all_computers': computer_results
            }
            return render(request, template, context)


