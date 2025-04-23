import mysql.connector
from mysql.connector import Error

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

def fetch_users():
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        print("\n=== Users Table ===")
        if not users:
            print("No users found.")
        else:
            print("user_id | password_hash")
            print("-" * 50)
            for user in users:
                print(f"{user[0]} | {user[1]}")
        
        cursor.close()
    except Error as err:
        print(f"Error querying users table: {err}")
    finally:
        conn.close()

def fetch_operations():
    conn = connect_to_database()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operations")
        operations = cursor.fetchall()
        
        print("\n=== Operations Table ===")
        if not operations:
            print("No operations found.")
        else:
            print("operation_id | technician_id | location | action | barcode | new_location | source | destination | battery_condition | photo_path | reaction | timestamp")
            print("-" * 120)
            for op in operations:
                print(f"{op[0]} | {op[1]} | {op[2]} | {op[3]} | {op[4]} | {op[5]} | {op[6]} | {op[7]} | {op[8]} | {op[9]} | {op[10]} | {op[11]}")
        
        cursor.close()
    except Error as err:
        print(f"Error querying operations table: {err}")
    finally:
        conn.close()

if __name__ == "__main__":
    fetch_users()
    fetch_operations()
