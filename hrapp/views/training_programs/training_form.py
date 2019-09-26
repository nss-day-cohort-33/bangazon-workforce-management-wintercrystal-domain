import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Training
from hrapp.models import model_factory
from ..connection import Connection

@login_required
def training_form(request):
    if request.method == 'GET':
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

            all_training_programs = db_cursor.fetchall()

        template = 'training_programs/training_form.html'
        context = {
            'all_training_programs': all_training_programs
        }

        return render(request, template, context)