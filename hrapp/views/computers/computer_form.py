import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models.employee import Employee
from hrapp.models import model_factory
from ..connection import Connection

def get_employee():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            e.id,
            e.first_name,
            e.last_name
        from hrapp_employee e
        """)

        return db_cursor.fetchall()
@login_required
def computer_form(request):
    if request.method == 'GET':
        employees = get_employee()
        template = 'computers/computer_form.html'
        context = {
            'all_employees': employees
        }

        return render(request, template, context)


# def computer_edit_form(request, computer_id):

#     if request.method == 'GET':
#         book = get_computer(computer_id)
#         libraries = get_libraries()

#         template = 'books/form.html'
#         context = {
#             'book': book,
#             'all_libraries': libraries
#         }

#         return render(request, template, context)