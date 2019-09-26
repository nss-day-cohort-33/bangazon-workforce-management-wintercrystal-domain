import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from hrapp.models import Training
from hrapp.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required
import datetime


def training_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            today = datetime.datetime.today()
            conn.row_factory = model_factory(Training)

            db_cursor = conn.cursor()
            db_cursor.execute("""
            SELECT
                t.id,
                t.title,
                t.start_date
            FROM hrapp_training t
            """)

            all_training_programs = db_cursor.fetchall()

            upcoming = list()

            for program in all_training_programs:
                if today < datetime.datetime.strptime(program.start_date, '%Y/%m/%d'):
                    upcoming.append(program)

        template = 'training_programs/training_list.html'
        context = {
            'all_training_programs': upcoming
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_training
            (
                title, start_date, end_date, capacity
            )
            VALUES (?, ?, ?, ?)
            """,
            (form_data['title'], datetime.datetime.strptime(form_data['start_date'], '%Y-%m-%d').strftime('%Y/%m/%d'), datetime.datetime.strptime(form_data['end_date'], '%Y-%m-%d').strftime('%Y/%m/%d'), form_data['capacity'] ))

        return redirect(reverse('hrapp:training_list'))