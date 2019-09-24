# import sqlite3
# from django.urls import reverse
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from hrapp.models import Training, Employee
# from hrapp.models import model_factory
# from ..connection import Connection


# def get_book(book_id):
#     with sqlite3.connect(Connection.db_path) as conn:
#         conn.row_factory = model_factory(Training)
#         db_cursor = conn.cursor()

#         db_cursor.execute("""
#         SELECT
#             b.id,
#             b.title,
#             b.isbn,
#             b.author,
#             b.year_published,
#             b.librarian_id,
#             b.location_id
#         FROM hrapp_training t
#         WHERE b.id = ?
#         """, (book_id,))

#         return db_cursor.fetchone()

# @login_required
# def book_details(request, book_id):
#     if request.method == 'GET':
#         book = get_book(book_id)

#         template = 'books/detail.html'
#         context = {
#             'book': book
#         }

#         return render(request, template, context)

#     if request.method == 'POST':
#         form_data = request.POST

#         # Check if this POST is for deleting a book
#         #
#         # Note: You can use parenthesis to break up complex
#         #       `if` statements for higher readability
#         if (
#             "actual_method" in form_data
#             and form_data["actual_method"] == "DELETE"
#         ):
#             with sqlite3.connect(Connection.db_path) as conn:
#                 db_cursor = conn.cursor()

#                 db_cursor.execute("""
#                 DELETE FROM libraryapp_book
#                 WHERE id = ?
#                 """, (book_id,))

#             return redirect(reverse('libraryapp:books'))

#         if (
#             "actual_method" in form_data
#             and form_data["actual_method"] == "EDIT"
#         ):
#             book = get_book(book_id)

#             template = 'books/edit.html'
#             context = {
#                 'book': book
#             }

#             return render(request, template, context)

#         if (
#             "actual_method" in form_data
#             and form_data["actual_method"] == "UPDATE"
#         ):
#             with sqlite3.connect(Connection.db_path) as conn:
#                 db_cursor = conn.cursor()

#                 db_cursor.execute("""
#                 UPDATE libraryapp_book
#                 SET
#                     title = ?, author = ?, isbn = ?,
#                     year_published = ?, librarian_id = ?
#                 WHERE id = ?
#                 """, (form_data['title'], form_data['author'],
#                 form_data['isbn'], form_data['year_published'], request.user.librarian.id, book_id))

#             book = get_book(book_id)

#             template = 'books/detail.html'
#             context = {
#                 'book': book
#             }

#             return render(request, template, context)