import sqlite3

def create_database():
    conn = sqlite3.connect('evbs.db')
    c = conn.cursor()

    # Create tables for warehouses, items, and operations
    c.execute('''CREATE TABLE IF NOT EXISTS warehouse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_name TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS item (
                    serial_number TEXT PRIMARY KEY,
                    part_number TEXT,
                    item_type TEXT,
                    status TEXT,
                    warehouse_location INTEGER,
                    FOREIGN KEY(warehouse_location) REFERENCES warehouse(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS operation (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT,
                    item_serial_number TEXT,
                    user_id TEXT,
                    operation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    additional_info TEXT)''')

    conn.commit()
    conn.close()

create_database()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QLineEdit, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
import sqlite3

class EVBSApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cox EVBS Prototype')
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_layout = QVBoxLayout()

        # Warehouse location dropdown
        self.warehouse_dropdown = QComboBox()
        self.load_warehouse_locations()
        main_layout.addWidget(QLabel('Select Warehouse Location'))
        main_layout.addWidget(self.warehouse_dropdown)

        # Operation type dropdown
        self.operation_dropdown = QComboBox()
        self.operation_dropdown.addItems(['Receive', 'Ship', 'Move', 'Take Picture', 'Inspect'])
        main_layout.addWidget(QLabel('Select Operation'))
        main_layout.addWidget(self.operation_dropdown)

        # Item Serial Number input
        self.item_serial_input = QLineEdit()
        self.item_serial_input.setPlaceholderText('Scan or Enter Serial Number')
        main_layout.addWidget(self.item_serial_input)

        # Button for executing the operation
        self.execute_button = QPushButton('Execute Operation')
        self.execute_button.clicked.connect(self.execute_operation)
        main_layout.addWidget(self.execute_button)

        # Setting layout
        self.setLayout(main_layout)

    def load_warehouse_locations(self):
        conn = sqlite3.connect('evbs.db')
        c = conn.cursor()
        c.execute('SELECT location_name FROM warehouse')
        locations = c.fetchall()
        for location in locations:
            self.warehouse_dropdown.addItem(location[0])
        conn.close()

    def execute_operation(self):
        serial_number = self.item_serial_input.text()
        operation = self.operation_dropdown.currentText()
        warehouse_location = self.warehouse_dropdown.currentText()

        # Check if item exists in the database
        conn = sqlite3.connect('evbs.db')
        c = conn.cursor()
        c.execute('SELECT * FROM item WHERE serial_number = ?', (serial_number,))
        item = c.fetchone()

        if not item:
            print(f"Item {serial_number} not found in the system!")
            return

        # Record the operation
        user_id = "device_001"  # Ideally, get from the device or user login
        c.execute('''INSERT INTO operation (operation_type, item_serial_number, user_id, additional_info)
                    VALUES (?, ?, ?, ?)''',
                  (operation, serial_number, user_id, warehouse_location))

        conn.commit()
        conn.close()

        print(f"Operation {operation} for item {serial_number} recorded.")

def main():
    app = QApplication(sys.argv)
    window = EVBSApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import cv2
import numpy as np


def take_picture():
    # Open the first camera (typically the default camera on the device)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture one frame
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('item_picture.jpg', frame)
        print("Picture taken successfully!")

    cap.release()

# Bind this to the 'Take Picture' button in the PyQt interface
