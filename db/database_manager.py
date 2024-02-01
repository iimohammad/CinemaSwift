import mysql.connector
from settings import local_settings


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

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
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()

    def create_table(self, table_name, columns):
        # Generate the CREATE TABLE query dynamically
        create_table_query = f"CREATE TABLE IF NOT EXISTS {
            table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join(columns)})"

        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully!")

        except mysql.connector.Error as error:
            print("Error while creating table:", error)

    def insert_into_table(self, table_name, columns, values):
        # Generate the INSERT INTO query dynamically
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({
            ', '.join(['%s' for _ in values])})"

        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, values)
            self.connection.commit()
            print(f"Data inserted into '{table_name}' successfully!")

        except mysql.connector.Error as error:
            print("Error while inserting data:", error)

    def select_column_from_table(self, table_name, column_name):
        # Generate the SELECT query dynamically
        select_query = f"SELECT {column_name} FROM {table_name}"

        try:
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            rows = cursor.fetchall()

            # Print the values of the selected column
            print(f"Values in '{column_name}' column of '{table_name}':")
            for row in rows:
                print(row[0])

        except mysql.connector.Error as error:
            print("Error while selecting data:", error)


if __name__ == "__main__":
    db_manager = DatabaseManager(
        host=local_settings.DATABASE['host'],
        user=local_settings.DATABASE['user'],
        password=local_settings.DATABASE['password'],
        database=local_settings.DATABASE['database']
    )

    # Connect to MySQL
    db_manager.connect()

    # Create desired tables
    person_model_columns = [
        ("username", "VARCHAR(255) NOT NULL"),
        ("email", "VARCHAR(255) NOT NULL"),
        ("birthday", "DATE"),
        ("phone", "VARCHAR(255) NOT NULL"),
    ]

    # # Example usage: insert data into the table
    # person_values = ["JohnDoe", "john.doe@example.com", "1990-01-01", "+123456789"]
    # db_manager.insert_into_table("person_model", ["username", "email", "birthday", "phone"], person_values)

    # # Example usage: select data from the table
    # db_manager.select_column_from_table("person_model", "username")

    bank_accounts_columns = [
        ("id", "SERIAL"),
        ("user_id", "INTEGER"),
        ("balance", "DECIMAL(10, 2)"),
        ("name", "VARCHAR(255)"),
        ("cvv2", "VARCHAR(10)"),
        ("password", "VARCHAR(255)"),
    ]

    wallets_columns = [
        ("id", "SERIAL"),
        ("balance", "DECIMAL(10, 2)"),
        ("name", "VARCHAR(255)"),
        ("user_id", "INTEGER"),
    ]

    seats_showtimes_columns = [
        ("id", "SERIAL"),
        ("sans_id", "INTEGER"),
        ("status", "VARCHAR(255)"),
    ]

    sans_model_columns = [
        ("id", "SERIAL"),
        ("screen_id", "INTEGER"),
        ("start_time", "TIMESTAMP"),
        ("capacity", "INTEGER"),
    ]

    admin_model_columns = [
        ("username", "VARCHAR(255) NOT NULL"),
        ("email", "VARCHAR(255) NOT NULL"),
        ("birthday", "DATE"),
        ("phone", "VARCHAR(255) NOT NULL"),
    ]

    users_model_columns = [
        ("username", "VARCHAR(255) NOT NULL"),
        ("email", "VARCHAR(255) NOT NULL"),
        ("birthday", "DATE"),
        ("phone", "VARCHAR(255) NOT NULL"),
        ("subscription_id", "INTEGER"),
    ]

    subscription_model_columns = [
        ("id", "SERIAL"),
        ("name", "VARCHAR(255)"),
        ("descount_number", "INTEGER"),
        ("discount_value", "DECIMAL(10, 2)"),
        ("drink_number", "INTEGER"),
    ]

    comments_model_columns = [
        ("id", "SERIAL"),
        ("film_id", "INTEGER"),
        ("user_id", "INTEGER"),
        ("text", "TEXT"),
        ("date", "TIMESTAMP"),
        ("parent_comments_id", "INTEGER"),
    ]

    free_drinks_model_columns = [
        ("id", "SERIAL"),
        ("datetime", "TIMESTAMP"),
    ]

    screens_mode_columns = [
        ("id", "SERIAL"),
        ("film_id", "INTEGER"),
        ("number_of_screens", "INTEGER"),
    ]

    films_model_columns = [
        ("id", "SERIAL"),
        ("name", "VARCHAR(255)"),
        ("age_rating", "INTEGER"),
        ("duration", "INTEGER"),
        ("rate", "DECIMAL(3, 2)"),
    ]

    db_manager.create_table("person_model", person_model_columns)
    db_manager.create_table("person_model", person_model_columns)
    db_manager.create_table("bank_accounts_models", bank_accounts_columns)
    db_manager.create_table("wallets_model", wallets_columns)
    db_manager.create_table("seats_showtimes_model", seats_showtimes_columns)
    db_manager.create_table("sans_model", sans_model_columns)
    db_manager.create_table("admin_model", admin_model_columns)
    db_manager.create_table("users_model", users_model_columns)
    db_manager.create_table("subscription_model", subscription_model_columns)
    db_manager.create_table("comments_model", comments_model_columns)
    db_manager.create_table("free_drinks_model", free_drinks_model_columns)
    db_manager.create_table("screens_mode", screens_mode_columns)
    db_manager.create_table("films_model", films_model_columns)

    # Disconnect from MySQL
    db_manager.disconnect()


# Call create_table for each class
