from .seeders.insert_initial_books_0001_2021_01_08 import Insert_initial_books

def seed(connection):
    Insert_initial_books(connection)