import sqlite3
from datetime import date
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

    elif request.method == 'POST':
        form_data = request.POST
        last_id = None

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()
            start_date = date.today().strftime("%Y/%m/%d")
            nothing = None

            db_cursor.execute("""
            INSERT INTO hrapp_computer
            (
                make, model, purchase_date,
                decommission_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (form_data['make'], form_data['model'],
                start_date, nothing))

            db_cursor.execute("""
            select last_insert_rowid()
            """)

            last_id = db_cursor.fetchone()

        if form_data['employee'] != 'Null':
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()
                start_date = date.today().strftime("%Y/%m/%d")
                nothing = None

                db_cursor.execute("""
                INSERT INTO hrapp_employeecomputer
                (
                    assigned_date, unassigned_date, computer_id_id,
                    employee_id_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (start_date, nothing,
                    last_id[0], form_data['employee']))


        return redirect(reverse('hrapp:computer_list'))