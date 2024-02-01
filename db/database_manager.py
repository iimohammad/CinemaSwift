from settings import local_settings

import psycopg2
from psycopg2 import sql
from pymongo import MongoClient


class dabaseManagerwithORM:

def create_table(table_name, columns):
    # Connect to DBMS
    dbname = local_settings.DATABASE['database'],
    user = local_settings.DATABASE['user'],
    password = local_settings.DATABASE['password'],
    host = local_settings.DATABASE['host'],
    port = local_settings.DATABASE['port']

        # Generate the CREATE TABLE query dynamically
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                {}
            );
        """).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join([
                sql.SQL("{} {}").format(sql.Identifier(column_name), sql.SQL(column_type))
                for column_name, column_type in columns
            ])
        )

        try:
            connection = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            cursor = connection.cursor()
            cursor.execute(create_table_query)
            connection.commit()

            print(f"Table '{table_name}' created successfully!")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        finally:
            # Close the cursor and connection
            if connection:
                cursor.close()
                connection.close()



    def get_user_by_username(username):
        pass

    def insert_into_table(table_name, columns, values):
        """
        How to use this fucntions :
        table_name = "person_model"
        columns = ["username", "email", "birthday", "phone"]
        values = ["JohnDoe", "john.doe@example.com", "1990-01-01", "+123456789"]
        insert_into_table(table_name, columns, values)
        """
        # Connect to DBMS
        dbname = local_settings.DATABASE['database'],
        user = local_settings.DATABASE['user'],
        password = local_settings.DATABASE['password'],
        host = local_settings.DATABASE['host'],
        port = local_settings.DATABASE['port']

        # Generate the INSERT INTO query dynamically
        insert_query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({});
        """).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(map(sql.Literal, values))
        )

        try:
            # Establish a connection to the PostgreSQL database
            connection = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )

            cursor = connection.cursor()
            cursor.execute(insert_query)
            connection.commit()
            print(f"Data inserted into '{table_name}' successfully!")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        finally:
            if connection:
                cursor.close()
                connection.close()



    # table_name = "person_model"
    # columns = ["username", "email", "birthday", "phone"]
    # values = ["JohnDoe", "john.doe@example.com", "1990-01-01", "+123456789"]

    # insert_into_table(table_name, columns, values)

    def select_column_from_table(table_name, column_name):
        """
        # Example usage:
        table_name = "person_model"
        column_name = "username"

        select_column_from_table(table_name, column_name)
        """
        # Connect to DBMS
        dbname = local_settings.DATABASE['database'],
        user = local_settings.DATABASE['user'],
        password = local_settings.DATABASE['password'],
        host = local_settings.DATABASE['host'],
        port = local_settings.DATABASE['port']

        # Generate the SELECT query dynamically
        select_query = sql.SQL("""
            SELECT {} FROM {};
        """).format(
            sql.Identifier(column_name),
            sql.Identifier(table_name)
        )

        try:
            # Establish a connection to the PostgreSQL database
            connection = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the SQL query to select the column
            cursor.execute(select_query)

            # Fetch all rows from the result set
            rows = cursor.fetchall()

            # Print the values of the selected column
            print(f"Values in '{column_name}' column of '{table_name}':")
            for row in rows:
                print(row[0])

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        finally:
            # Close the cursor and connection
            if connection:
                cursor.close()
                connection.close()



    person_model_columns = [
        ("username", "VARCHAR(255) NOT NULL"),
        ("email", "VARCHAR(255) NOT NULL"),
        ("birthday", "DATE"),
        ("phone", "VARCHAR(255) NOT NULL"),
    ]

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
    # Call create_table for each class
    create_table("person_model", person_model_columns)
    create_table("bank_accounts_models", bank_accounts_columns)
    create_table("wallets_model", wallets_columns)
    create_table("seats_showtimes_model", seats_showtimes_columns)
    create_table("sans_model", sans_model_columns)
    create_table("admin_model", admin_model_columns)
    create_table("users_model", users_model_columns)
    create_table("subscription_model", subscription_model_columns)
    create_table("comments_model", comments_model_columns)
    create_table("free_drinks_model", free_drinks_model_columns)
    create_table("screens_mode", screens_mode_columns)
    create_table("films_model", films_model_columns)

