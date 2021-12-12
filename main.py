from Library import Library
import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect("library.db")
    library = Library(conn).rent_book()

