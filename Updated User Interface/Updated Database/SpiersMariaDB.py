import tkinter as tk
from tkinter import ttk, messagebox
import mariadb
import sys
import cv2
from PIL import Image, ImageTk

# AWS RDS Database Connection Parameters
rds_db_user = "root"
rds_db_password = "" # I'll replace with less personal password
rds_db_host = "spiers.cxg20au4crax.us-east-2.rds.amazonaws.com"  # Replace with your RDS endpoint
rds_db_port = 3306  # Default port for MariaDB
rds_db_name = "spiersnt"

# Local MariaDB Database Connection Parameters
local_db_user = "root"
local_db_password = "" # I'll replace with less personal password
local_db_host = "localhost"  # Assuming local MariaDB is on your machine
local_db_port = 3306  # Default port for MariaDB
local_db_name = "mariadb_data"

# Initialize main window
root = tk.Tk()
root.title("EV Battery Solutions")
root.geometry("700x800")
root.configure(bg="white")

# Create Tkinter variables
user_var = tk.StringVar()
location_var = tk.StringVar()
item_var = tk.StringVar()
action_var = tk.StringVar()
vibe_var = tk.StringVar()


# Local Database setup
def setup_local_database():
    try:
        conn = mariadb.connect(
            user=local_db_user,
            password=local_db_password,
            host=local_db_host,
            port=local_db_port,
            database=local_db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                        username TEXT,
                                        location TEXT,
                                        item TEXT,
                                        action TEXT,
                                        vibe TEXT,
                                        photo_path TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                         username TEXT UNIQUE)''')
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

# Local Database setup
def setup_AWS_database():
    try:
        conn = mariadb.connect(
            user=rds_db_user,
            password=rds_db_password,
            host=rds_db_host,
            port=rds_db_port,
            database=rds_db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                        username TEXT,
                                        location TEXT,
                                        item TEXT,
                                        action TEXT,
                                        vibe TEXT,
                                        photo_path TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                         username TEXT UNIQUE)''')
        conn.commit()
        conn.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)


# Move between pages
def show_frame(frame):
    frame.tkraise()


# Validation function
def validate_step(field_value, field_name, current_frame, next_frame):
    if not field_value.strip():
        messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=root)
        show_frame(current_frame)
        return False
    return True


# Save function
def save_data():
    username = user_var.get().strip()
    location = location_var.get().strip()
    item = item_var.get().strip()
    action = action_var.get().strip()
    vibe = vibe_var.get().strip()
    photo_path = getattr(photo_label, "photo_path", "")

    validation_errors = []
    if not username:
        validation_errors.append(("Technician identification", "UserPage"))
    if not location:
        validation_errors.append(("Location selection", "LocationPage"))
    if not item:
        validation_errors.append(("Item identification", "ItemPage"))
    if not action:
        validation_errors.append(("Action selection", "ActionPage"))
    if not vibe:
        validation_errors.append(("Operator status check", "VibePage"))
    if not photo_path:
        validation_errors.append(("Battery photo", "PhotoPage"))

    if validation_errors:
        field_name, page_name = validation_errors[0]
        messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=root)
        show_frame(frames[page_name])
        if page_name == "PhotoPage":
            photo_status.config(text="Photo capture required!", fg="red")
        return

    try:
        local_conn = mariadb.connect(
            user=local_db_user,
            password=local_db_password,
            host=local_db_host,
            port=local_db_port,
            database=local_db_name)
        cursor = local_conn.cursor()
        cursor.execute('''INSERT INTO logs 
                        (username, location, item, action, vibe, photo_path)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (username, location, item, action, vibe, photo_path))
        local_conn.commit()
        show_frame(frames["EndPage"])
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save data: {str(e)}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
    finally:
        if local_conn:
            local_conn.close()
            
    try:
        rds_conn = mariadb.connect(
            user=rds_db_user,
            password=rds_db_password,
            host=rds_db_host,
            port=rds_db_port,
            database=rds_db_name)
        cursor = rds_conn.cursor()
        cursor.execute('''INSERT INTO logs 
                        (username, location, item, action, vibe, photo_path)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                       (username, location, item, action, vibe, photo_path))
        rds_conn.commit()
        show_frame(frames["EndPage"])
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save data: {str(e)}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
    finally:
        if rds_conn:
            rds_conn.close()


# Navigation functions
def go_back(current_frame):
    if current_frame == frames["UserPage"]:
        show_frame(frames["StartPage"])
    elif current_frame == frames["LocationPage"]:
        show_frame(frames["UserPage"])
    elif current_frame == frames["ActionPage"]:
        show_frame(frames["LocationPage"])
    elif current_frame == frames["ItemPage"]:
        show_frame(frames["ActionPage"])
    elif current_frame == frames["PhotoPage"]:
        show_frame(frames["ItemPage"])
    elif current_frame == frames["VibePage"]:
        show_frame(frames["PhotoPage"])


def go_next(current_frame, next_frame, validation_field, field_name):
    if validate_step(validation_field.get(), field_name, current_frame, next_frame):
        show_frame(next_frame)


# Predictive text functions
def update_suggestions(event):
    typed = user_var.get().strip()
    suggestion_listbox.delete(0, tk.END)
    if len(typed) < 1:
        return
    conn = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="mariadb_data")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username LIKE ?", (f"%{typed}%",))
    matches = cursor.fetchall()
    conn.close()
    for match in matches:
        suggestion_listbox.insert(tk.END, match[0])


def select_suggestion(event):
    if suggestion_listbox.curselection():
        selected = suggestion_listbox.get(suggestion_listbox.curselection())
        user_var.set(selected)
    suggestion_listbox.delete(0, tk.END)


# Photo functions
def take_photo():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        messagebox.showerror("Error", "Failed to open webcam.")
        return

    cv2.namedWindow("Battery Scanner - SPACE to capture, ESC to cancel")
    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture video.")
            break
        cv2.imshow("Battery Scanner - SPACE to capture, ESC to cancel", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Spacebar
            photo_path = f"battery_{item_var.get().replace(' ', '_')}_{user_var.get()}.jpg"
            cv2.imwrite(photo_path, frame)
            cam.release()
            cv2.destroyAllWindows()
            display_photo(photo_path)
            return
        elif key == 27:  # ESC
            cam.release()
            cv2.destroyAllWindows()
            return


def display_photo(photo_path):
    try:
        img = Image.open(photo_path)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        photo_label.config(image=img_tk)
        photo_label.image = img_tk
        photo_label.photo_path = photo_path
        photo_status.config(text="Photo captured successfully!", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load photo: {e}")
        photo_status.config(text="Photo capture failed", fg="red")


def reset_session():
    user_var.set("")
    location_var.set("")
    item_var.set("")
    action_var.set("")
    vibe_var.set("")
    photo_label.config(image="")
    photo_label.photo_path = ""
    photo_status.config(text="")
    show_frame(frames["StartPage"])


def confirm_exit():
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to end the session and close the application?"):
        root.destroy()


# Main container setup
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create all frames
frames = {}
for F in ("StartPage", "UserPage", "LocationPage", "ActionPage", "ItemPage", "PhotoPage", "VibePage", "EndPage"):
    frame = tk.Frame(container, bg="white")
    frames[F] = frame
    frame.grid(row=0, column=0, sticky="nsew")

# ====== Start Page ======
start_frame = frames["StartPage"]
tk.Label(start_frame, text="SPIERS Technology Smart System", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
tk.Button(start_frame, text="Start Session", font=("Arial", 14), bg="#004aad", fg="white",
          command=lambda: show_frame(frames["UserPage"])).pack(pady=10)

# ====== User Page ======
user_frame = frames["UserPage"]
tk.Label(user_frame, text="Who are you", font=("Arial", 14), bg="white").pack(pady=20)
user_entry = ttk.Entry(user_frame, textvariable=user_var, font=("Arial", 12))
user_entry.pack(pady=5)
suggestion_listbox = tk.Listbox(user_frame, height=4, font=("Arial", 12), bg="white", relief="flat")
suggestion_listbox.pack()
user_entry.bind("<KeyRelease>", update_suggestions)
suggestion_listbox.bind("<Double-Button-1>", select_suggestion)
suggestion_listbox.bind("<Return>", select_suggestion)

# Centered navigation buttons
nav_frame_user = tk.Frame(user_frame, bg="white")
nav_frame_user.pack(pady=20, side="bottom", anchor="center")
tk.Button(nav_frame_user, text="Back",
          command=lambda: go_back(user_frame),
          bg="#666666", fg="white", width=10).pack(side="left", padx=10)
tk.Button(nav_frame_user, text="Next →",
          command=lambda: go_next(user_frame, frames["LocationPage"], user_var, "Technician identification"),
          bg="#004aad", fg="white", width=10).pack(side="left", padx=10)

# ====== Location Page ======
location_frame = frames["LocationPage"]
tk.Label(location_frame, text="Where are you?", font=("Arial", 14), bg="white").pack(pady=20)
location_dropdown = ttk.Combobox(location_frame, textvariable=location_var,
                                 values=["New Battery Section", "Old Battery Section"], font=("Arial", 12))
location_dropdown.pack()

# Centered navigation buttons
nav_frame_location = tk.Frame(location_frame, bg="white")
nav_frame_location.pack(pady=20, side="bottom", anchor="center")
tk.Button(nav_frame_location, text="Back",
          command=lambda: go_back(location_frame),
          bg="#666666", fg="white", width=10).pack(side="left", padx=10)
tk.Button(nav_frame_location, text="Next →",
          command=lambda: go_next(location_frame, frames["ActionPage"], location_var, "Location selection"),
          bg="#004aad", fg="white", width=10).pack(side="left", padx=10)

# ====== Action Page ======
action_frame = frames["ActionPage"]
tk.Label(action_frame, text="What are you trying to do?", font=("Arial", 14), bg="white").pack(pady=20)
action_dropdown = ttk.Combobox(action_frame, textvariable=action_var,
                               values=["Find", "Receive", "Ship", "Move"], font=("Arial", 12))
action_dropdown.pack()

# Centered navigation buttons
nav_frame_action = tk.Frame(action_frame, bg="white")
nav_frame_action.pack(pady=20, side="bottom", anchor="center")
tk.Button(nav_frame_action, text="Back",
          command=lambda: go_back(action_frame),
          bg="#666666", fg="white", width=10).pack(side="left", padx=10)
tk.Button(nav_frame_action, text="Next →",
          command=lambda: go_next(action_frame, frames["ItemPage"], action_var, "Action selection"),
          bg="#004aad", fg="white", width=10).pack(side="left", padx=10)

# ====== Item Page ======
item_frame = frames["ItemPage"]
tk.Label(item_frame, text="Scan or Select the Battery", font=("Arial", 14), bg="white").pack(pady=20)

# Barcode Entry
barcode_label = tk.Label(item_frame, text="Scan Barcode:", font=("Arial", 12), bg="white")
barcode_label.pack()
barcode_entry = ttk.Entry(item_frame, textvariable=item_var, font=("Arial", 12))
barcode_entry.pack(pady=5)

# Dropdown for manual selection
item_label = tk.Label(item_frame, text="Or Select Item:", font=("Arial", 12), bg="white")
item_label.pack()
item_dropdown = ttk.Combobox(item_frame, textvariable=item_var,
                             values=["Battery 1", "Battery 2", "Custom Item Entry"], font=("Arial", 12))
item_dropdown.pack(pady=5)

# Status label for feedback
barcode_status = tk.Label(item_frame, text="", font=("Arial", 10), bg="white")
barcode_status.pack(pady=5)


def process_barcode(event):
    barcode = item_var.get().strip()
    if barcode:
        barcode_status.config(text=f"Barcode {barcode} scanned successfully!", fg="green")
        item_var.set(barcode)
    else:
        barcode_status.config(text="No barcode scanned!", fg="red")
        item_var.set("")
    return "break"


barcode_entry.bind("<Return>", process_barcode)
barcode_entry.focus_set()

# Centered navigation buttons
nav_frame_item = tk.Frame(item_frame, bg="white")
nav_frame_item.pack(pady=20, side="bottom", anchor="center")
tk.Button(nav_frame_item, text="Back",
          command=lambda: go_back(item_frame),
          bg="#666666", fg="white", width=10).pack(side="left", padx=10)
tk.Button(nav_frame_item, text="Next →",
          command=lambda: go_next(item_frame, frames["PhotoPage"], item_var, "Item identification"),
          bg="#004aad", fg="white", width=10).pack(side="left", padx=10)

# ====== Photo Page ======
photo_frame = frames["PhotoPage"]
tk.Label(photo_frame, text="Take the photo of the item", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

photo_container = tk.Frame(photo_frame, bg="white", width=450, height=450)
photo_container.pack(pady=10)
photo_container.pack_propagate(False)

photo_label = tk.Label(photo_container, bg="white", relief="ridge", borderwidth=2)
photo_label.place(relx=0.5, rely=0.5, anchor="center", width=400, height=400)

photo_status = tk.Label(photo_frame, text="", bg="white")
photo_status.pack()
tk.Button(photo_frame, text="📸 Capture Image", command=take_photo,
          bg="#004aad", fg="white").pack(pady=5)

# Centered navigation buttons
nav_frame_photo = tk.Frame(photo_frame, bg="white")
nav_frame_photo.pack(pady=20, side="bottom", anchor="center")
tk.Button(nav_frame_photo, text="Back",
          command=lambda: go_back(photo_frame),
          bg="#666666", fg="white", width=10).pack(side="left", padx=10)
tk.Button(nav_frame_photo, text="Next →",
          command=lambda: go_next(photo_frame, frames["VibePage"],
                                  tk.StringVar(value=getattr(photo_label, "photo_path", "")), "Battery photo"),
          bg="#004aad", fg="white", width=10).pack(side="left", padx=10)

# ====== Vibe Page ======
vibe_frame = frames["VibePage"]
tk.Label(vibe_frame, text="How are you feeling about this activity?", font=("Arial", 14, "bold"), bg="white").pack(
    pady=20)
tk.Label(vibe_frame, text="Please confirm your current status:", font=("Arial", 12), bg="white").pack()
vibe_options = [
    ("😊 Confident", "confident"),
    ("😌 Calm", "calm"),
    ("😐 Neutral", "neutral"),
    ("😟 Stressed", "stressed"),
    ("😴 Fatigued", "fatigued"),
    ("🚀 Energized", "energized")
]
for text, value in vibe_options:
    rb = ttk.Radiobutton(vibe_frame, text=text, value=value, variable=vibe_var,
                         style="TRadiobutton", width=20)
    rb.pack(anchor="w", padx=50)

# Centered navigation buttons
nav_frame_vibe = tk.Frame(vibe_frame, bg="white")
nav_frame_vibe.pack(pady=20, side="bottom", anchor="center")
tk.Button(nav_frame_vibe, text="Back",
          command=lambda: go_back(vibe_frame),
          bg="#666666", fg="white", width=10).pack(side="left", padx=10)
tk.Button(nav_frame_vibe, text="Submit Report",
          command=lambda: go_next(vibe_frame, frames["EndPage"], vibe_var, "Operator status check") or save_data(),
          bg="#004aad", fg="white", width=15).pack(side="left", padx=10)

# ====== End Page ======
end_frame = frames["EndPage"]
tk.Label(end_frame, text="SPIERS Smart System", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
tk.Label(end_frame, text="Thank you for using the SPIERS system!\nYour operation has been securely logged.",
         font=("Arial", 12), bg="white").pack(pady=20)
tk.Label(end_frame, text="What would you like to do next?", font=("Arial", 12), bg="white").pack()
btn_frame = tk.Frame(end_frame, bg="white")
btn_frame.pack(pady=20)
tk.Button(btn_frame, text="New Battery Operation", command=reset_session,
          bg="#004aad", fg="white", width=20).pack(side="left", padx=10)
tk.Button(btn_frame, text="End Session", command=confirm_exit,
          bg="#ff4444", fg="white", width=15).pack(side="left", padx=10)

# Initialize database and start application
setup_local_database()
setup_AWS_database()
show_frame(frames["StartPage"])
root.mainloop()