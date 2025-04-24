import mysql.connector
import hashlib

class DatabaseManager:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "spiers_user"
        self.password = "spiers_pass"
        self.database = "spiers_system"
        self.auth_plugin = "mysql_native_password"
        self.init_db()

    def init_db(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin=self.auth_plugin
            )
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            raise

    def authenticate_user(self, user_id, password):
        entered_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin=self.auth_plugin
            )
            cursor = conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result and entered_password_hash == result[0]:
                return True
            return False
        except mysql.connector.Error as err:
            raise Exception(f"Error accessing database: {str(err)}")

    def log_operation(self, data):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin=self.auth_plugin
            )
            cursor = conn.cursor()
            query = """
                INSERT INTO operations (technician_id, location, action, barcode, new_location, source, destination, battery_condition, photo_path, reaction)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                data["technician_id"],
                data["location"],
                data["action"],
                data["barcode"],
                data["new_location"] or None,
                data["source"] or None,
                data["destination"] or None,
                data["battery_condition"] or None,
                data["photo_path"],
                data["reaction"]
            ))
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            operation_id = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return operation_id
        except mysql.connector.Error as err:
            raise Exception(f"Error logging operation: {str(err)}")

    def generate_operation_summary(self, operation_id):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                auth_plugin=self.auth_plugin
            )
            cursor = conn.cursor()
            query = "SELECT * FROM operations WHERE operation_id = %s"
            cursor.execute(query, (operation_id,))
            operation = cursor.fetchone()
            if not operation:
                cursor.close()
                conn.close()
                return "Operation not found."
            
            (op_id, tech_id, loc, action, barcode, new_loc, src, dest, batt_cond, photo_path, reaction, timestamp) = operation
            summary = f"Operation Summary (ID: {op_id})\n"
            summary += f"Timestamp: {timestamp}\n"
            summary += f"Technician ID: {tech_id}\n"
            summary += f"Location: {loc}\n"
            summary += f"Action: {action}\n"
            summary += f"Barcode: {barcode}\n"
            
            if action == "Move" and new_loc:
                summary += f"New Location: {new_loc}\n"
            elif action == "Receive":
                summary += f"Source: {src}\n"
                if src == "Customer" and batt_cond:
                    summary += f"Battery Condition: {batt_cond}\n"
                if new_loc:
                    summary += f"Stored in Location: {new_loc}\n"
            elif action == "Ship" and dest:
                summary += f"Destination: {dest}\n"
            elif action == "Find":
                try:
                    cursor.execute("""
                        SELECT action, new_location, destination, source, battery_condition
                        FROM operations
                        WHERE barcode = %s AND operation_id != %s
                        ORDER BY timestamp DESC
                        LIMIT 1
                    """, (barcode, op_id))
                    result = cursor.fetchone()
                    if result:
                        prev_action, prev_new_location, prev_destination, prev_source, prev_battery_condition = result
                        if prev_new_location:
                            summary += f"Battery Location: {prev_new_location}\n"
                        elif prev_action == "Ship":
                            summary += f"Battery Location: Shipped to {prev_destination}\n"
                        elif prev_action == "Receive" and prev_source == "Customer":
                            summary += f"Battery Location: Received from Customer, Condition: {prev_battery_condition}\n"
                        elif prev_action == "Receive" and prev_source == "Supplier":
                            summary += f"Battery Location: Received from Supplier\n"
                        else:
                            summary += f"Battery Location: Location not specified\n"
                    else:
                        summary += f"Battery Location: Item does not exist or has no recorded operations.\n"
                except mysql.connector.Error as err:
                    summary += f"Battery Location: Database error: {str(err)}\n"

            summary += f"Photo Path: {photo_path if photo_path else 'N/A'}\n"
            summary += f"Reaction: {reaction if reaction else 'N/A'}\n"
            cursor.close()
            conn.close()
            return summary
        except mysql.connector.Error as err:
            return f"Error generating summary: {str(err)}"
