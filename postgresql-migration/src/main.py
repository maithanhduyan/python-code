import os
import datetime
import psycopg2
import configparser

# Lấy đường dẫn thư mục hiện tại
current_directory = os.getcwd()
# print("Thư mục hiện tại:", current_directory)

# Tạo đối tượng ConfigParser
config = configparser.ConfigParser()

# Đọc cấu hình từ file system.conf
config.read(os.path.join(current_directory, 'system.conf'))
# print("Database_1 name:", config.get('Database_1', 'dbname'))

def connect_to_database(db_name, user, password, host, port):
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return connection
    except Exception as e:
        print(f"Error: Unable to connect to the database\n{str(e)}")
        return None

def get_table_names(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        table_names = [record[0] for record in cursor.fetchall()]
        cursor.close()
        return table_names
    except Exception as e:
        print(f"Error: Unable to fetch table names\n{str(e)}")
        return []

def compare_databases(database1, database2):
    tables_db1 = get_table_names(database1)
    tables_db2 = get_table_names(database2)

    common_tables = set(tables_db1).intersection(tables_db2)

    for table in common_tables:
        # Compare data in the tables
        compare_table_data(table, database1, database2)

def compare_table_data(table_name, database1, database2):
    try:
        cursor_db1 = database1.cursor()
        cursor_db2 = database2.cursor()

        # Fetch all rows from the table in database1
        cursor_db1.execute(f"SELECT * FROM {table_name};")
        rows_db1 = cursor_db1.fetchall()

        # Fetch all rows from the table in database2
        cursor_db2.execute(f"SELECT * FROM {table_name};")
        rows_db2 = cursor_db2.fetchall()

        # Compare the rows
        if rows_db1 == rows_db2:
            print(f"Data in table {table_name} is identical.")
        else:
            print(f"Data in table {table_name} is different.")

        cursor_db1.close()
        cursor_db2.close()

    except Exception as e:
        print(f"Error: Unable to compare data in table {table_name}\n{str(e)}")

if __name__ == "__main__":
    # Database connection parameters
    db1_params = {
        'db_name': config.get('Database_1', 'dbname'),
        'user': config.get('Database_1', 'user'),
        'password': config.get('Database_1', 'password'),
        'host': config.get('Database_1', 'host'),
        'port': config.get('Database_1', 'port')
    }

    db2_params = {
        'db_name': config.get('Database_2', 'dbname'),
        'user': config.get('Database_2', 'user'),
        'password': config.get('Database_2', 'password'),
        'host': config.get('Database_2', 'host'),
        'port': config.get('Database_2', 'port')
    }

    # Connect to the databases
    db1_connection = connect_to_database(**db1_params)
    db2_connection = connect_to_database(**db2_params)

    if db1_connection and db2_connection:
        # Compare the databases
        compare_databases(db1_connection, db2_connection)

        # Close the connections
        db1_connection.close()
        db2_connection.close()
