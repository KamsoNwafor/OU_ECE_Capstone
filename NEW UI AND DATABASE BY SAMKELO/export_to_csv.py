import mysql.connector
from mysql.connector import Error
import csv
import os

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="spiers_user",
            password="spiers_pass",
            database="spiers_system",
            auth_plugin="mysql_native_password"
        )
        return conn
    except Error as err:
        print(f"Error connecting to database: {err}")
        return None

def export_users_to_csv():
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        headers = ["user_id", "password_hash"]
        
        # Export to CSV in C:/Temp with proper quoting
        file_path = "C:/Temp/users.csv"
        try:
            os.makedirs("C:/Temp", exist_ok=True)  # Ensure the directory exists
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # Quote all fields
                writer.writerow(headers)  # Write the header
                writer.writerows(users)   # Write the data
            print(f"Users table exported to {file_path}")
        except Exception as e:
            print(f"Failed to write users.csv to {file_path}: {str(e)}")
        
        cursor.close()
    except Error as err:
        print(f"Error exporting users table: {err}")
    finally:
        conn.close()

def export_operations_to_csv():
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operations")
        operations = cursor.fetchall()
        headers = ["operation_id", "technician_id", "location", "action", "barcode", "new_location", 
                   "source", "destination", "battery_condition", "photo_path", "reaction", "timestamp"]
        
        # Export to CSV in C:/Temp with proper quoting
        file_path = "C:/Temp/operations.csv"
        try:
            os.makedirs("C:/Temp", exist_ok=True)  # Ensure the directory exists
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # Quote all fields
                writer.writerows([headers])  # Write the header
                # Replace None with empty string for cleaner output
                cleaned_operations = [[str(item) if item is not None else "" for item in row] for row in operations]
                writer.writerows(cleaned_operations)  # Write the data
            print(f"Operations table exported to {file_path}")
        except Exception as e:
            print(f"Failed to write operations.csv to {file_path}: {str(e)}")
        
        cursor.close()
    except Error as err:
        print(f"Error exporting operations table: {err}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_users_to_csv()
    export_operations_to_csv()
