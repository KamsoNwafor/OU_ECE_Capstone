CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    warehouse_desc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS battery_state (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_desc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS works (
    work_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_type_name TEXT NOT NULL,
	parent_work_type_id int,
	foreign KEY (parent_work_type_id) REFERENCES works (work_type_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS employees (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL,
    warehouse_id INTEGER,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_shorthand TEXT,
    location_description TEXT NOT NULL,
    warehouse_id INTEGER,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS batteries (
    battery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number TEXT NOT NULL UNIQUE,
    part_number INTEGER,
    item_type INTEGER,
    part_description TEXT NOT NULL,
    quantity_total INTEGER,
    quantity_new Integer,
    quantity_old Integer,
    quantity_death_row Integer,
    location_new integer,
    location_old integer,
    location_death_row integer,
    picture BLOB,
    FOREIGN KEY (location_new) REFERENCES locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (location_old) REFERENCES locations(location_id) ON DELETE CASCADE,
    FOREIGN KEY (location_death_row) REFERENCES locations(location_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_time TIMESTAMP UNIQUE,
    serial_number TEXT,
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

CREATE TABLE IF NOT EXISTS reports (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_desc TEXT NOT NULL,
    FOREIGN KEY (request_id) REFERENCES requests(request_id) ON DELETE CASCADE
);

/*
drop table if exists batteries;
drop table if exists battery_state;
drop table if exists employees;
drop table if exists locations;
drop table if exists reports;
drop table if exists requests;
drop table if exists warehouses;
drop table if exists works;
*/