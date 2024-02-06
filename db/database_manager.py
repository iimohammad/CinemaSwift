import inspect
from settings import local_settings
import mysql.connector
# from db import models
import sys
sys.path.append('../')


class DatabaseManager:
    """
    A class for managing database connections and operations.

    Attributes:
        host (str): The host address of the database.
        user (str): The username used to connect to the database.
        password (str): The password used to connect to the database.
        database (str): The name of the database.
        connection: The connection object to the database.
        dict (dict): A dictionary mapping Python data types to corresponding MySQL data types.
    """
    _instance = None

    def __new__(cls):
        """
        Singleton implementation to ensure only one instance of DatabaseManager exists.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes DatabaseManager with connection details and default column types.
        """
        self.host = local_settings.DATABASE['host']
        self.user = local_settings.DATABASE['user']
        self.password = local_settings.DATABASE['password']
        self.database = local_settings.DATABASE['name']
        self.connection = None

        self.dict = {
            'str': 'VARCHAR(255) NOT NULL',
            'int': 'Integer',
            'datetime': 'DATE'
        }

    def connect(self):
        """
        Establishes a connection to the database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL Database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def disconnect(self):
        """
        Closes the connection to the database.
        """
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
        """
        Executes a SQL query that does not return results (e.g., INSERT, UPDATE, DELETE).

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to be substituted into the query.

        Returns:
            int or None: The last inserted ID if applicable, None otherwise.
        """
        try:
            self.connect()

            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.lastrowid  # Return the last inserted ID
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.disconnect()

    def execute_query_select(self, query, params=None):
        """
        Executes a SQL query that returns results (e.g., SELECT).

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to be substituted into the query.

        Returns:
            list or None: A list of tuples representing the query results, or None if an error occurs.
        """
        try:
            self.connect()

            cursor = self.connection.cursor(buffered=True)
            cursor.execute(query, params)

            # For SELECT queries, fetch the results
            result = cursor.fetchall()

            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            self.disconnect()

    def create_table(self, table_name, columns):
        """
        Creates a new table in the database.

        Args:
            table_name (str): The name of the table to create.
            columns (list): A list of tuples representing column names and data types.
        """
        columns_str = ', '.join(
            [f"{name} {column_type}" for name, column_type in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {
            table_name} ({columns_str})"

        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully!")

        except mysql.connector.Error as error:
            print("Error while creating table:", error)

    def insert_into_table(self, table_name, columns, values):
        """
        Inserts data into an existing table.

        Args:
            table_name (str): The name of the table to insert data into.
            columns (list): A list of column names.
            values (list): A list of values to be inserted into the table.
        """
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({
            ', '.join(['%s' for _ in values])}"

        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(insert_query, values)
            self.connection.commit()
            print(f"Data inserted into '{table_name}' successfully!")

        except mysql.connector.Error as error:
            print("Error while inserting data:", error)

    def select_column_from_table(self, table_name, column_name):
        """
        Selects a specific column from a table and prints its values.

        Args:
            table_name (str): The name of the table to select from.
            column_name (str): The name of the column to select.
        """
        select_query = f"SELECT {column_name} FROM {table_name}"

        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(select_query)
            rows = cursor.fetchall()

            # Print the values of the selected column
            print(f"Values in '{column_name}' column of '{table_name}':")
            for row in rows:
                print(row[0])

        except mysql.connector.Error as error:
            print("Error while selecting data:", error)

    def create_columns(self, model_name):
        """
        Generates column definitions based on the attributes of a model class.

        Args:
            model_name (class): The model class to extract attributes from.

        Returns:
            list: A list of tuples representing column names and data types.
        """
        init_signature = inspect.signature(model_name.__init__)
        init_params = {param.name: param.annotation for param in init_signature.parameters.values(
        ) if param.name != 'self'}
        model_columns = [
            (name,
             self.dict.get(
                 param_type.__name__,
                 'VARCHAR(255)')) for name,
            param_type in init_params.items()]
        return model_columns

# if __name__ == "__main__":
    # Connect to MySQL
    # db_manager.connect()

    # db_manager.create_table("person_model", db_manager.create_columns(models.person_model))
    # db_manager.create_table("bank_accounts_models", db_manager.create_columns(models.bank_account_model))
    # db_manager.create_table("wallets_model", db_manager.create_columns(models.wallet_model))
    # db_manager.create_table("seats_showtimes_model", db_manager.create_columns(models.seats_showtimes_model))
    # db_manager.create_table("sans_model", db_manager.create_columns(models.sans_model))
    # db_manager.create_table("admin_model", db_manager.create_columns(models.admin_model))
    # db_manager.create_table("users_model", db_manager.create_columns(models.user_model))
    # db_manager.create_table("subscription_model", db_manager.create_columns(models.subscription_model))
    # db_manager.create_table("comments_model", db_manager.create_columns(models.comments_model))
    # db_manager.create_table("free_drinks_model", db_manager.create_columns(models.free_drinks_model))
    # db_manager.create_table("screens_mode", db_manager.create_columns(models.screens_mode))
    # db_manager.create_table("films_model", db_manager.create_columns(models.films_model))

    # Disconnect from MySQL
    # db_manager.disconnect()
    # db_manager.connect()
# insert_query = """
#     INSERT INTO users
#     (id, user_name, email, birthday, phone, subscription_type, password)
#     VALUES (%s, %s, %s, %s, %s, %s, %s)
#     """

# user_data = (
#         1,
#         'JohnDoe',
#         'john.doe@example.com',
#         '1990-01-01',
#         '1234567890',
#         'basic',
#         'hashed_password'
# )
#     # Execute the query
# db = DatabaseManager()
# db.execute_query(insert_query, user_data)
