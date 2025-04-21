import mariadb
import sys

# create a class that stores the data
class DatabaseManager:
    # AWS RDS Database Connection Parameters

    rds_db_user = "spiersGroup1"
    rds_db_password = "spiersGroup1DB"  # I'll replace with less personal password
    rds_db_host = "spiersgroup1.cxg20au4crax.us-east-2.rds.amazonaws.com"  # Replace with your RDS endpoint
    rds_db_port = 3306  # Default port for MariaDB
    rds_db_name = "spiersGroup1DB"
    rds_conn = None
    rds_cursor = None

    """
    # Local MariaDB Database Connection Parameters
    local_db_user = "root"
    local_db_password = ""  # Replace with system MariaDB password
    local_db_host = "localhost"  # Assuming local MariaDB is on your machine
    local_db_port = 3306  # Default port for MariaDB
    local_db_name = "mariadb_data"
    local_conn = None
    local_cursor = None
    """

    # the following are dummy data since I haven't connected to the database yet
    tasks = ("Find", "Receive", "Ship", "Move", "Update Battery Status", "Intake New Item", "Take Picture")
    serial_num = "battery_1_serial"

    @classmethod
    def get_tasks(cls):
        return cls.tasks

    @classmethod
    def establish_connection(cls, db_user, db_password, db_host, db_port, db_name):
        try:
            conn = mariadb.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
                database=db_name)
            # Disable Auto-Commit so we only commit when changes are ready
            conn.autocommit = False

            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    @classmethod
    # Local Database setup
    def setup_mock_database(cls, db_conn):
        try:
            conn = db_conn
            cursor = conn.cursor()

            create_tables_sql = [
                """
                CREATE TABLE IF NOT EXISTS warehouses (
                    warehouse_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    warehouse_desc TEXT NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS battery_state (
                    state_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    state_desc TEXT NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS works (
                    work_type_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    work_type_name TEXT NOT NULL,
                    parent_work_type_id INT,
                    FOREIGN KEY (parent_work_type_id) REFERENCES works (work_type_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS employees (
                    user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_admin INTEGER NOT NULL,
                    warehouse_id INTEGER,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS locations (
                    location_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    location_shorthand TEXT,
                    location_description TEXT NOT NULL,
                    warehouse_id INTEGER,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS batteries (
                    serial_number VARCHAR(30) PRIMARY KEY,
                    part_number INTEGER,
                    item_type INTEGER,
                    part_description TEXT NOT NULL,
                    quantity_total INTEGER,
                    quantity_new INTEGER,
                    quantity_old INTEGER,
                    quantity_death_row INTEGER,
                    location_new INTEGER,
                    location_old INTEGER,
                    location_death_row INTEGER,
                    picture BLOB,
                    FOREIGN KEY (location_new) REFERENCES locations(location_id) ON DELETE CASCADE,
                    FOREIGN KEY (location_old) REFERENCES locations(location_id) ON DELETE CASCADE,
                    FOREIGN KEY (location_death_row) REFERENCES locations(location_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS requests (
                    request_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    request_time TIMESTAMP UNIQUE,
                    serial_number VARCHAR(30),
                    work_type_id INTEGER,
                    user_id INTEGER,
                    warehouse_id INTEGER,
                    state_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY (serial_number) REFERENCES batteries(serial_number) ON DELETE CASCADE,
                    FOREIGN KEY (work_type_id) REFERENCES works(work_type_id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES employees(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE CASCADE,
                    FOREIGN KEY (state_id) REFERENCES battery_state(state_id) ON DELETE CASCADE
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS reports (
                    request_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    report_desc TEXT NOT NULL,
                    FOREIGN KEY (request_id) REFERENCES requests(request_id) ON DELETE CASCADE
                );
                """
            ]
            # Execute each SQL statement to create the tables
            for statement in create_tables_sql:
                cursor.execute(statement)
                conn.commit()

        except mariadb.Error as e:
            print(f"Error: {e}")

    @classmethod
    def add_mock_data (cls, db_conn):

        try:
            # Establish connection to Mariadb database
            conn = db_conn

            # Link cursor
            cursor = conn.cursor()

            # Insert each warehouse into the warehouse table
            warehouses = [
                (1, "Warehouse 1"),
                (2, "Warehouse 2"),
                (3, "Warehouse 3"),
                (4, "Warehouse 1"),
                (5, "Warehouse 2"),
                (6, "Warehouse 3")
            ]

            for warehouse_id, warehouse_desc in warehouses:
                cursor.execute('''
                    INSERT INTO warehouses (warehouse_id, warehouse_desc)
                    VALUES (?, ?)
                ''', (warehouse_id, warehouse_desc))

            cls.save_changes(conn)

            # Insert each battery state into the battery state table
            battery_state = [
                (1, "New"),
                (2, "Old"),
                (3, "Death Row")
            ]

            for state_id, state_desc in battery_state:
                cursor.execute("""
                    INSERT INTO battery_state (state_id, state_desc)
                    VALUES (?, ?)
                """, (state_id, state_desc))

            cls.save_changes(conn)

            works = [
                (1, "Find", None),
                (2, "Receive", 1),
                (3, "Ship", 1),
                (4, "Move", 1),
                (5, "Update Battery Status", 1),
                (6, "Intake New Item", 2),
                (7, "New Battery Work", 5),
                (8, "Old Battery Work", 5),
                (9, "Death Row Battery Work", 5),
                (10, "Store", 6),
                (11, "Diagnostic Analysis", 7),
                (12, "Disassembly", 7),
                (13, "Repair", 7),
                (14, "Re-assembly", 7),
                (15, "Testing", 7),
                (16, "Re-certification", 7),
                (17, "Take Apart", 8),
                (18, "Shred (pieces)", 8),
                (19, "Shred (powder)", 8),
                (20, "Make new battery", 8),
                (21, "Take Picture", None)
            ]

            for work_type_id, work_type_name, parent_work_type_id in works:
                cursor.execute("""
                            INSERT INTO works (work_type_id, work_type_name, parent_work_type_id)
                            VALUES (?, ?, ?)
                        """, (work_type_id, work_type_name, parent_work_type_id))

            cls.save_changes(conn)

            # Insert each employee into the employees table
            employees = [
                (1, "John", "Smith", "123password", 1, 1),
                (2, "Emily", "Johnson", "p123assword", 0, 1),
                (3, "Michael", "Williams", "pa123ssword", 0, 1),
                (4, "Sarah", "Brown", "pas123sword", 1, 2),
                (5, "James", "Davis", "pass123word", 0, 2),
                (6, "Jessica", "Wilson", "passw123ord", 0, 2),
                (7, "David", "Moore", "passwo123rd", 1, 3),
                (8, "Olivia", "Taylor", "passwor123d", 0, 3),
                (9, "Daniel", "Anderson", "password123", 0, 3),
                (10, "John", "Smith", "123password", 1, 4),
                (11, "Emily", "Johnson", "p123assword", 0, 4),
                (12, "Michael", "Williams", "pa123ssword", 0, 4),
                (13, "Sarah", "Brown", "pas123sword", 1, 5),
                (14, "James", "Davis", "pass123word", 0, 5),
                (15, "Jessica", "Wilson", "passw123ord", 0, 5),
                (16, "David", "Moore", "passwo123rd", 1, 6),
                (17, "Olivia", "Taylor", "passwor123d", 0, 6),
                (18, "Daniel", "Anderson", "password123", 0, 6)
            ]

            for user_id, first_name, last_name, password, is_admin, warehouse_id in employees:
                cursor.execute('''
                    INSERT INTO employees (user_id, first_name, last_name, password, is_admin, warehouse_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, first_name, last_name, password, is_admin, warehouse_id))

            cls.save_changes(conn)

            # Insert each location into the location table
            locations = [
                ("FS1, W1", "floor space 1, warehouse 1", 1),
                ("FS2, W1", "floor space 2, warehouse 1", 1),
                ("FS3, W1", "floor space 3, warehouse 1", 1),
                ("SS1, W1", "shelf space 1, warehouse 1", 1),
                ("SS2, W1", "shelf space 2, warehouse 1", 1),
                ("SS3, W1", "shelf space 3, warehouse 1", 1),
                ("FS1, W2", "floor space 1, warehouse 2", 2),
                ("FS2, W2", "floor space 2, warehouse 2", 2),
                ("FS3, W2", "floor space 3, warehouse 2", 2),
                ("SS1, W1", "shelf space 1, warehouse 1", 2),
                ("SS2, W1", "shelf space 2, warehouse 1", 2),
                ("SS3, W1", "shelf space 3, warehouse 1", 2)
            ]

            for location_shorthand, location_description, warehouse_id in locations:
                cursor.execute("""
                    INSERT INTO locations (location_shorthand, location_description, warehouse_id)
                    VALUES (?, ?, ?)
                """, (location_shorthand, location_description, warehouse_id))

            cls.save_changes(conn)

            batteries = [
                ("battery_1_serial", 1, 1, "battery 1", 20, 10, 5, 5, 1, 2, 3),
                ("battery_2_serial", 1, 1, "battery 2", 20, 10, 5, 5, 4, 5, 6),
                ("battery_3_serial", 1, 1, "battery 3", 20, 10, 5, 5, 7, 8, 9)
            ]

            for serial_number, part_number, item_type, part_description, quantity_total, quantity_new, quantity_old, quantity_death_row, location_new, location_old, location_death_row in batteries:
                cursor.execute("""
                    INSERT INTO batteries (serial_number, part_number, item_type, part_description, quantity_total, quantity_new, quantity_old, quantity_death_row, location_new, location_old, location_death_row)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (serial_number, part_number, item_type, part_description, quantity_total, quantity_new, quantity_old,
                      quantity_death_row, location_new, location_old, location_death_row))

            cls.save_changes(conn)

        except mariadb.Error as e:
            print(f"Error: {e}")

    """
    @classmethod
    def setup_local_database(cls):
        cls.local_conn =  cls.establish_connection(cls.local_db_user, cls.local_db_password, cls.local_db_host, cls.local_db_port, cls.local_db_name)
        cls.local_cursor = cls.local_conn.cursor()
        cls.setup_mock_database(cls.local_conn)
        cls.add_mock_data(cls.local_conn)

    @classmethod
    def get_local_conn (cls):
        return cls.local_conn
    """

    @classmethod
    def setup_aws_database(cls):
        cls.rds_conn = cls.establish_connection(cls.rds_db_user, cls.rds_db_password, cls.rds_db_host, cls.rds_db_port, cls.rds_db_name)
        cls.rds_cursor = cls.rds_conn.cursor()
        cls.setup_mock_database(cls.rds_conn)
        cls.add_mock_data(cls.rds_conn)

    @classmethod
    def clear_everything(cls):
        commands = [
            """drop table if exists reports;""",
            """drop table if exists requests;""",
            """drop table if exists batteries;""",
            """drop table if exists locations;""",
            """drop table if exists employees;""",
            """drop table if exists works;""",
            """drop table if exists battery_state;""",
            """drop table if exists warehouses;"""
        ]

        cls.conn = cls.establish_connection(cls.rds_db_user, cls.rds_db_password, cls.rds_db_host, cls.rds_db_port,
                                            cls.rds_db_name)
        cls.cursor = cls.conn.cursor()

        for instruction in commands:
            cls.cursor.execute(instruction)

        cls.conn.commit()
        cls.conn.close()

    @classmethod
    def get_aws_conn (cls):
        return cls.rds_conn

    @classmethod
    def save_changes(cls, db_conn):
        db_conn.commit()

    @classmethod
    def close_connection(cls, db_conn):
        db_conn.close()