import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from hrapp.models import Training
from hrapp.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required

# @login_required
def training_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:

            conn.row_factory = model_factory(Training)

            db_cursor = conn.cursor()
            db_cursor.execute("""
            select
                t.id,
                t.title
            from hrapp_training t
            """)

            all_training_programs = db_cursor.fetchall()

        template = 'training_programs/training_list.html'
        context = {
            'all_training_programs': all_training_programs
        }

        return render(request, template, context)
