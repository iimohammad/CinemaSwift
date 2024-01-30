import psycopg2 
from settings import local_settings





# Connect to PostgreSQL using psycopg2
conn = psycopg2.connect(
    host=local_settings.DATABASE['host'],
    port=local_settings.DATABASE['port'],
    user=local_settings.DATABASE['user'],
    password=local_settings.DATABASE['password'],
    database=local_settings.DATABASE['database']
)


# Create a cursor object to execute SQL commands
cursor = conn.cursor()


# Create a table for contacts
create_table_query = """
CREATE TABLE IF NOT EXISTS contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone_number VARCHAR(20)
);
"""


cursor.execute(create_table_query)

# with conn:
#     with conn.cursor() as cursor:
#         cursor.execute(
#             'INSERT INTO contact (name, phone_number) VALUES (%s, %s)', (name, phone))