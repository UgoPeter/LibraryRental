class Library():
    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.rent_book()
        self.get_books_list()
        self.search_user_by_id()
        self.save_book_rent()

    def rent_book(self):
        books_list = dict(self.get_books_list())
        print(books_list)

        selected_book_id = int(input("Please put book id: "))
        print("Your selected book is: {}".format(books_list[selected_book_id]))

        user_exist = input("Do you have an account: Yes/No? ").lower()
        if user_exist == 'yes':
            user_id = int(input("Please put your id account: "))
        else:
            user_account = input("Do you want to create an account: Yes/No? ").lower()
            if user_account == 'yes':
                user_id = self.create_new_user()
            else:
                answer_user = input("Account creation is required to borrow a book. Are you sure you do not want to create an account: Yes/No? ").lower()
                if answer_user == 'yes':
                    return
                else:
                    self.create_new_user()

        self.save_book_rent(user_id, selected_book_id)

    def get_books_list(self):
        return self.cursor.execute('''
            SELECT "id", "name" FROM "books"
        ''').fetchall()

    def search_user_by_id(self, user_id):
        return self.cursor.execute('''
            SELECT "id" FROM "users"
        ''').fetchone()[user_id]

    def save_book_rent(self, user_id, book_id):
        self.cursor.execute('''
        INSERT INTO "book_rentals" ("user_id", "book_id")
        VALUES(?, ?)''', (user_id, book_id))
        self.connection.commit()

