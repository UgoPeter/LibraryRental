from .migrations.create_library_tables_0001_2021_01_08 import Create_library_tables

def migrate(connection):
    Create_library_tables(connection)