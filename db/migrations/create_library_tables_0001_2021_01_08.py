class Create_library_tables():
    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.create_users_table()
        self.create_book_table()
        self.create_book_rentals_table()

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "users" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "first_name" TEXT NOT NULL, 
            "last_name" TEXT NOT NULL

            )''')

    def create_book_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "books" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "name" TEXT NOT NULL
            )''')

    def create_book_rentals_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "book_rentals" (
            "user_id" INTEGER NOT NULL,
            "book_id" INTEGER NOT NULL,
            FOREIGN KEY ("user_id") REFERENCES "users" ("id"), 
            FOREIGN KEY ("book_id") REFERENCES "books" ("id") 
        )''')
