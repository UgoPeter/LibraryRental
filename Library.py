class Library():
    connection = None
    cursor = None

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def rent_book(self):
        books_list = dict(self.get_books_list())
        print(books_list)

        selected_book_id = self.validation_selected_book_id()

        user_exist = self.validation_user_exist()

        if user_exist == "yes":
            user_id = self.validation_user_id()
            self.search_user_by_id(user_id)
        else:
            user_account = self.validation_user_account()
            if user_account == "yes":
                user_id = self.create_new_user()
                print("Your account id: {}.".format(user_id))
            else:
                answer_user = self.validation_answer_user()
                if answer_user == "yes":
                    print("The program is ending its work.")
                    exit()
                else:
                    print("If you want to create an account, restart the program.")
                    print("The program is ending its work.")
                    exit()

        self.save_book_rent(user_id, selected_book_id)
        print("You borrowed a book {}.".format(books_list[selected_book_id]))

    def get_books_list(self):
        return self.cursor.execute('''
            SELECT "id", "name" FROM "books"
        ''').fetchall()

    def search_user_by_id(self, user_id):
        return self.cursor.execute('''
            SELECT "id" FROM "users"
        ''').fetchone()

    def save_book_rent(self, user_id, book_id):

        self.cursor.execute('''
        INSERT INTO "book_rentals" ("user_id", "book_id")
        VALUES(?, ?)''', (user_id, book_id))
        self.connection.commit()

    def create_new_user(self):
        first_name = input("Please enter your name: ")
        last_name = input("Please enter your last name: ")

        self.cursor.execute('''    
            INSERT INTO "users" ("first_name", "last_name")
            VALUES(?, ?)''', (first_name, last_name))

        self.connection.commit()

        return self.cursor.lastrowid

    def validation_selected_book_id(self):
        books_list = dict(self.get_books_list())

        try:
            selected_book_id = int(input("Please enter the book id: "))
            if selected_book_id <= 0:
                raise Exception("Id must be a greater than zero.")
            print("Your selected book is: {}".format(books_list[selected_book_id]))
            return selected_book_id
        except ValueError:
            print("Id must be a number.")
            self.validation_selected_book_id()
        except KeyError:
            print("Select the correct value from the list.")
            self.validation_selected_book_id()
        except Exception:
            print("Id must be a greater than zero.")
            self.validation_selected_book_id()

    def validation_user_exist(self):

        # Casting added to keep input from remembering the old value
        try:
            input_user_exist = str(input("Do you have an account: Yes/No? ").lower())
            if (input_user_exist == 'yes') or (input_user_exist == 'no'):
                return input_user_exist
            raise Exception
        except Exception:
            print("Please enter a correct value. Try again")
            self.validation_user_exist()

    def validation_user_id(self):
        try:
            input_user_id = int(input("Please put your id account: "))
            return input_user_id
        except Exception:
            print("Sorry, there was an error {}. Try again.".format(Exception))
            self.validation_user_id()

    def validation_user_account(self):
        try:
            input_user_account = str(input("Do you want to create an account: Yes/No? ").lower())
            if input_user_account == 'yes' or input_user_account == 'no':
                return input_user_account
            raise Exception
        except Exception:
            print("Please enter a correct value. Try again")
            self.validation_user_account()

    def validation_answer_user(self):
        try:
            input_answer_user = input(
                "Account creation is required to borrow a book. Are you sure you do not want to create an account: Yes/No? ").lower()
            if input_answer_user == 'yes' or input_answer_user == 'no':
                return input_answer_user
            raise Exception
        except Exception:
            print("Please enter a correct value. Try again")
            self.validation_answer_user()
