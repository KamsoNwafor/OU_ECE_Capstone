import sqlite3

# Establish connection to SQLite3 database
conn = sqlite3.connect('spiers_database.db')

# Enable foreign key support
conn.execute('PRAGMA foreign_keys = ON;')

# Link cursor
cursor = conn.cursor()

# create a class that stores the data
class DatabaseData:
    def __init__(self):
        # the following are dummy data since I haven't connected to the database yet
        self.warehouses = ("Warehouse 1", "Warehouse 2", "Warehouse 3")
        self.tasks = ("Find", "Receive", "Ship", "Move", "Update Battery Status", "Intake New Item", "Take Picture")
        self.users = ("Joe Johnson", "Tim Duncan", "Kobe Bryant", "Lebron James", "Michael Jordan", "Shaquille O'Neal'",
                      "Kyrie Irving", "Stephen Curry")

    def get_warehouses(self):
        return self.warehouses

    def get_tasks(self):
        return self.tasks

    def get_users(self):
        return self.users

conn.commit()
conn.close()