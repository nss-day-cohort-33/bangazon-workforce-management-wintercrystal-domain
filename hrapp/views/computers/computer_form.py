import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import model_factory
from ..connection import Connection

def computer_form(request):
    if request.method == 'GET':
        template = 'computers/computer_form.html'

        return render(request, template, {})


@login_required
def book_edit_form(request, computer_id):

    if request.method == 'GET':
        book = get_book(book_id)
        libraries = get_libraries()

        template = 'books/form.html'
        context = {
            'book': book,
            'all_libraries': libraries
        }

        return render(request, template, context)