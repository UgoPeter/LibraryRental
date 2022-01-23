import sqlite3
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest

from Library import Library


class TestLibrary(unittest.TestCase):
    db_mock = None

    def setUp(self):
        magic_mock = MagicMock(autospec=sqlite3.connect)
        self.db_mock = magic_mock

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_validation_create_new_user(self):
        lib = Library(self.db_mock).validation_create_new_user(('Jakub', 'Nowak'))

        assert lib == ('Jakub', 'Nowak')

    @patch.object(Library, 'retry_validation')
    @patch.object(Library, 'input_selected_book_id')
    @patch.object(Library, 'get_books_list')
    def test_validation_selected_book_id_correct_value(self, get_books_list_mock, input_selected_book_id_mock, retry_validation):
        get_books_list_mock.return_value = [(1, 'Harry Potter'), (2, 'Malowany Czlowiek'), (3, 'Folwark Zwierzecy')]
        input_selected_book_id_mock.return_value = 1
        retry_validation = None

        lib = Library(self.db_mock)

        assert lib.validation_selected_book_id(1) == 1

    @patch.object(Library, 'retry_validation')
    @patch.object(Library, 'input_selected_book_id')
    @patch.object(Library, 'get_books_list')
    def test_validation_selected_book_id_less_zero(self, get_books_list_mock, input_selected_book_id_mock,
                                                         retry_validation_mock):
        get_books_list_mock.return_value = [(1, 'Harry Potter'), (2, 'Malowany Czlowiek'), (3, 'Folwark Zwierzecy')]
        input_selected_book_id_mock.return_value = -1
        retry_validation_mock.return_value = None

        lib = Library(self.db_mock)

        with self.captured_output() as (out, err):
            lib.validation_selected_book_id(input_selected_book_id_mock())
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()

        assert output == "Wrong value. Try again."

    @patch.object(Library, 'retry_validation')
    @patch.object(Library, 'input_selected_book_id')
    @patch.object(Library, 'get_books_list')
    def test_validation_selected_book_id_zero(self, get_books_list_mock, input_selected_book_id_mock,
                                                         retry_validation_mock):
        get_books_list_mock.return_value = [(1, 'Harry Potter'), (2, 'Malowany Czlowiek'), (3, 'Folwark Zwierzecy')]
        input_selected_book_id_mock.return_value = 0
        retry_validation_mock.return_value = None

        lib = Library(self.db_mock)

        with self.captured_output() as (out, err):
            lib.validation_selected_book_id(input_selected_book_id_mock())
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()

        assert output == "Wrong value. Try again."

    # @patch.object(Library, 'retry_validation')
    # @patch.object(Library, 'input_selected_book_id')
    # @patch.object(Library, 'get_books_list')
    # def test_validation_selected_book_id_value(self, get_books_list_mock, input_selected_book_id_mock,
    #                                                      retry_validation_mock):
    #     get_books_list_mock.return_value = [(1, 'Harry Potter'), (2, 'Malowany Czlowiek'), (3, 'Folwark Zwierzecy')]
    #     input_selected_book_id_mock.side_effect = ValueError
    #     retry_validation_mock.return_value = None
    #
    #     lib = Library(self.db_mock)
    #
    #     with self.captured_output() as (out, err):
    #         lib.validation_selected_book_id(input_selected_book_id_mock())
    #     # This can go inside or outside the `with` block
    #     output = out.getvalue().strip()
    #
    #     assert output == "Id must be a number."

    @patch.object(Library, 'retry_validation')
    @patch.object(Library, 'input_selected_book_id')
    @patch.object(Library, 'get_books_list')
    def test_validation_selected_book_id_zero(self, get_books_list_mock, input_selected_book_id_mock,
                                                         retry_validation_mock):
        get_books_list_mock.return_value = [(1, 'Harry Potter'), (2, 'Malowany Czlowiek'), (3, 'Folwark Zwierzecy')]
        input_selected_book_id_mock.return_value = 4
        retry_validation_mock.return_value = None

        lib = Library(self.db_mock)

        with self.captured_output() as (out, err):
            lib.validation_selected_book_id(input_selected_book_id_mock())
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()

        assert output == "Select the correct value from the list."

    @patch.object(Library, 'input_user_exist')
    def test_validation_user_exist_yes_answer(self, input_user_exist_mock):
        input_user_exist_mock.return_value = 'yes'

        lib = Library(self.db_mock)

        assert  lib.validation_user_exist(input_user_exist_mock()) == 'yes'

    @patch.object(Library, 'input_user_exist')
    def test_validation_user_exist_no_answer(self, input_user_exist_mock):
        input_user_exist_mock.return_value = 'no'

        lib = Library(self.db_mock)

        assert lib.validation_user_exist(input_user_exist_mock()) == 'no'

    @patch.object(Library, 'retry_validation')
    @patch.object(Library, 'input_user_exist')
    def test_validation_user_exist_wrong_answer(self, input_user_exist_mock, retry_validation_mock):
        input_user_exist_mock.return_value = 'test'
        retry_validation_mock = None

        lib = Library(self.db_mock)

        with self.captured_output() as (out, err):
            lib.validation_user_exist(input_user_exist_mock)
        # This can go inside or outside the `with` block
        output = out.getvalue().strip()


        assert output == 'Please enter a correct value. Try again'