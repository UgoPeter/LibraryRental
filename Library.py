class Library():
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

    def get_books_list(self):
        return self.cursor.execute('''
            SELECT "id", "name" FROM "books"
        ''').fetchall()

    def create_book_rentals_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS "book_rentals" (
            "user_id" INTEGER NOT NULL,
            "book_id" INTEGER NOT NULL,
            FOREIGN KEY ("user_id") REFERENCES "users" ("id"), 
            FOREIGN KEY ("book_id") REFERENCES "books" ("id") 
        )''')

    def rent_book(self):
        books_list = dict(self.get_books_list())
        print(books_list)

        selected_book_id = int(input("Please put book id: "))
        print("Your selected book is: {}".format(books_list[selected_book_id]))

        user_exist = input("Do you have an account: Yes/No? ").lower()
        if user_exist == "yes":
            user_id = int(input("Please put your id account: "))
        else:
            user_account = input("Do you want to create an account: Yes/No? ").lower()
            if user_account == 'yes':
                user_id = self.create_new_user()
            else:
                answer_user = input(
                    "Account creation is required to borrow a book. Are you sure you do not want to create an account: Yes/No? ").lower()
                if answer_user == 'yes':
                    return
                else:
                    self.create_new_user()

        self.save_book_rent(user_id, selected_book_id)

    def search_user_by_id(self, id):
        pass

    def create_new_user(self):
        first_name = input("Please enter your name: ")
        last_name = input("Please enter your last name: ")

        self.cursor.execute('''
            INSERT INTO "users" ("first_name", "last_name")
            VALUES(?, ?)''', (first_name, last_name))

        self.connection.commit()

        return self.cursor.lastrowid

    def save_book_rent(self, user_id, book_id):
        self.cursor.execute('''
        INSERT INTO "book_rentals" ("user_id", "book_id")
        VALUES(?, ?)''', (user_id, book_id))
        self.connection.commit()
