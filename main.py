from Library import Library
from db.def_run_seeders import seed
from db.def_run_migrations import migrate
import sqlite3

if __name__ == '__main__':

    conn = sqlite3.connect("library.db")
    seed(conn)
    migrate(conn)
    library = Library(conn).rent_book()


