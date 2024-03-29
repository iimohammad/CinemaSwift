import inspect
import mysql.connector
from settings import local_settings

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
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
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
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
        # Generate the CREATE TABLE query dynamically
        columns_str = ', '.join(
            [f"{name} {column_type}" for name, column_type in columns])
        create_table_query = f"""CREATE TABLE IF NOT EXISTS {
            table_name} ({columns_str})"""

        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully!")

        except mysql.connector.Error as error:
            print("Error while creating table:", error)

    def insert_into_table(self, table_name, columns, values):
        # Generate the INSERT INTO query dynamically
        insert_query = f"""INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({
            ', '.join(['%s' for _ in values])}"""

        try:
            cursor = self.connection.cursor(buffered=True)
            cursor.execute(insert_query, values)
            self.connection.commit()
            print(f"Data inserted into '{table_name}' successfully!")

        except mysql.connector.Error as error:
            print("Error while inserting data:", error)

    def select_column_from_table(self, table_name, column_name):
        # Generate the SELECT query dynamically
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

