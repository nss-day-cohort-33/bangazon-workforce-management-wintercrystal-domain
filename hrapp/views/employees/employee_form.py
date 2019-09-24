import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Department
from hrapp.models import model_factory
from ..connection import Connection

@login_required
def employee_form(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = model_factory(Department)
            db_cursor = conn.cursor()
            db_cursor.execute("""
            select
                d.id,
                d.dept_name,
                d.budget
            from hrapp_department d
            """)
        dataset = db_cursor.fetchall()
        template = "employees/form.html"
        context = {
          "departments": dataset
        }
        return render(request, template, context)