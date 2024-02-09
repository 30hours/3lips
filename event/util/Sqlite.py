"""
@file Sqlite.py
@author 30hours
"""

import sqlite3

class Sqlite:

    """
    @class Sqlite
    @brief A class for interacting with an SQLite database.
    @see https://sqlite.org/ for more information on SQLite.
    """

    def __init__(self, database_path):

        """
        @brief Constructor for the Sqlite class.
        @param database_path (str): Path to the SQLite database.
        """

        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, schema):
        """
        @brief Create a table in the database if it doesn't exist.
        @param table_name (str): Name of the table.
        @param schema (str): Table schema definition.
        @return None
        """

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema});")
        self.connection.commit()

    def table_exists(self, table_name):

        """
        @brief Check if a table if the given name exists in the database.
        @param table_name (str): Name of the table.
        @return bool: True if the table exists.
        """

        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        return self.cursor.fetchone() is not None

    def add_entry(self, table_name, api, timestamp):

        """
        @brief Add entry to table.
        @param table_name (str): Name of the table.
        @param api (str): API URL to add.
        @param timestamp (Integer): Timestamp to add.
        @return None
        """

        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        insert_entry_sql = "INSERT INTO {table_name} (api, timestamp) VALUES (?, ?);"
        cursor.execute(insert_entry_sql, (api, timestamp))
        connection.commit()

    def execute_query(self, query, parameters=None):

        """
        @brief Execute an SQL query on the database.
        @param query (str): SQL query to execute.
        @param parameters (tuple, optional): Parameters to bind to the query.
        @return None
        """

        if parameters:
            self.cursor.execute(query, parameters)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def fetch_all_rows(self, query):

        """
        @brief Fetch all rows resulting from an SQL query.
        @param query (str): SQL query to execute.
        @return list: List of tuples representing the result rows.
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):

        """
        @brief Close the SQLite database connection.
        @return None
        """

        self.connection.close()
