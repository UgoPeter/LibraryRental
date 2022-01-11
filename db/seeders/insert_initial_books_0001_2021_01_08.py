class Insert_initial_books():
    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.add_books()

    def add_books(self):
        list_of_books = ["Harry Potter", "chuj"]

        self.cursor.execute('''
            DELETE FROM "books"    
        ''')

        self.cursor.execute('''
            DELETE FROM sqlite_sequence WHERE name = "books"
        ''')

        for book in list_of_books:
            self.cursor.execute('''
                INSERT INTO "books" ("name")      
                VALUES(?)''', (book,))


