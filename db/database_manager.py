from settings import local_settings

import psycopg2
from psycopg2 import sql
# database
# This function create our desire tables 
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
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Execute the SQL query to create the table
        cursor.execute(create_table_query)

        # Commit the changes
        connection.commit()

        print(f"Table '{table_name}' created successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()


# Example usage:
table_name = "desire_table"
columns = [
    ("column1", "VARCHAR(255)"),
    ("column2", "INTEGER"),
    ("column3", "DATE"),
    # Add more columns as needed
]

create_table(table_name, columns)
