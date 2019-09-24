import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..connection import Connection


def department_form(request):
    if request.method == 'GET':

        template = 'departments/form.html'

        return render(request, template, {})