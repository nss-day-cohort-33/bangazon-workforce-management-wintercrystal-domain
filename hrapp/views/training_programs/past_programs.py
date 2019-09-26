import sqlite3
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from hrapp.models import Training
from hrapp.models import model_factory
from ..connection import Connection
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def past_programs(request):
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

            past = list()

            for program in all_training_programs:
                if today >= datetime.datetime.strptime(program.start_date, '%Y/%m/%d'):
                    past.append(program)

        template = 'training_programs/past_list.html'
        context = {
            'all_training_programs': past
        }

        return render(request, template, context)