import mariadb

# Establish connection to Mariadb database
conn = mariadb.connect('spiers_database.db')

# Enable foreign key support
conn.execute('PRAGMA foreign_keys = ON;')

# Link cursor
cursor = conn.cursor()

# Insert each warehouse into the warehouse table
warehouses = [
    ("Warehouse 1",),
    ("Warehouse 2",),
    ("Warehouse 3",)
]

for warehouse_desc in warehouses:
    cursor.execute('''
        INSERT INTO warehouses (warehouse_desc)
        VALUES (?)
    ''', (warehouse_desc[0],))

# Insert each employee into the employees table
employees = [
    ("John", "Smith", "123password", 1, 1),
    ("Emily", "Johnson", "p123assword", 0, 1),
    ("Michael", "Williams", "pa123ssword", 0, 1),
    ("Sarah", "Brown", "pas123sword", 1, 2),
    ("James", "Davis", "pass123word", 0, 2),
    ("Jessica", "Wilson", "passw123ord", 0, 2),
    ("David", "Moore", "passwo123rd", 1, 3),
    ("Olivia", "Taylor", "passwor123d", 0, 3),
    ("Daniel", "Anderson", "password123", 0, 3)
]

for first_name, last_name, password, is_admin, warehouse_id in employees:
    cursor.execute('''
        INSERT INTO employees (first_name, last_name, password, is_admin, warehouse_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, password, is_admin, warehouse_id))

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

# Insert each battery state into the location table
battery_state = [
    ("New",),
    ("Old",),
    ("Death Row",)
]

# Insert each employee into the employees table
for state_desc in battery_state:
    cursor.execute("""
        INSERT INTO battery_state (state_desc)
        VALUES (?)
    """, (state_desc[0],))

batteries = [
    ("battery_1_serial", 1, 1, "battery 1", 20, 10, 5, 5, 1, 2, 3),
    ("battery_2_serial", 1, 1, "battery 2", 20, 10, 5, 5, 4, 5, 6),
    ("battery_3_serial", 1, 1, "battery 3", 20, 10, 5, 5, 7, 8, 9)
]

for serial_number, part_number, item_type, part_description, quantity_total, quantity_new, quantity_old, quantity_death_row, location_new, location_old, location_death_row in batteries:
    cursor.execute("""
        INSERT INTO batteries (serial_number, part_number, item_type, part_description, quantity_total, quantity_new, quantity_old, quantity_death_row, location_new, location_old, location_death_row)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (serial_number, part_number, item_type, part_description, quantity_total, quantity_new, quantity_old, quantity_death_row, location_new, location_old, location_death_row))

values = [
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

for work_type_id, work_type_name, parent_work_type_id in values:
    cursor.execute("""
        INSERT INTO WORKS (work_type_id, work_type_name, parent_work_type_id)
        VALUES (?, ?, ?)
    """, (work_type_id, work_type_name, parent_work_type_id))

# Commit changes and close connection
conn.commit()

# Close the connection
conn.close()