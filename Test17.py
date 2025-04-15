import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import cv2
from PIL import Image, ImageTk

# Initialize main window
root = tk.Tk()
root.title("EV Battery Solutions")
root.geometry("800x480")  # Fit the 4-inch screen resolution
root.configure(bg="#f5f5f5")

# Create Tkinter variables
user_var = tk.StringVar()
location_var = tk.StringVar()
item_var = tk.StringVar()
action_var = tk.StringVar()
vibe_var = tk.StringVar()

# Define styles
style = ttk.Style()
style.theme_use("clam")

# Configure styles with smaller fonts and padding
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TCombobox", font=("Arial", 10))
style.configure("TRadiobutton", font=("Arial", 10))

# Custom button styles
style.configure("Primary.TButton", background="#004aad", foreground="white")
style.configure("Secondary.TButton", background="#666666", foreground="white")
style.configure("Danger.TButton", background="#ff4444", foreground="white")

style.map("Primary.TButton", background=[("active", "#003b8e")])
style.map("Secondary.TButton", background=[("active", "#555555")])
style.map("Danger.TButton", background=[("active", "#cc3333")])

# Database setup (unchanged)
def setup_database():
    conn = sqlite3.connect("evbs_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username TEXT,
                                    location TEXT,
                                    item TEXT,
                                    action TEXT,
                                    vibe TEXT,
                                    photo_path TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE)''')
    conn.commit()
    conn.close()

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

# Save function (unchanged)
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
        conn = sqlite3.connect("evbs_data.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO logs 
                        (username, location, item, action, vibe, photo_path)
                        VALUES (?, ?, ?, ?, ?, ?)''', 
                       (username, location, item, action, vibe, photo_path))
        cursor.execute('''INSERT OR IGNORE INTO users (username) VALUES (?)''', (username,))
        conn.commit()
        show_frame(frames["EndPage"])
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save data: {str(e)}")
    finally:
        if conn:
            conn.close()

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
    try:
        conn = sqlite3.connect("evbs_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username LIKE ? ORDER BY username", (f"%{typed}%",))
        matches = cursor.fetchall()
        for match in matches:
            suggestion_listbox.insert(tk.END, match[0])
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch suggestions: {str(e)}")
    finally:
        conn.close()

def select_suggestion(event):
    if suggestion_listbox.curselection():
        selected = suggestion_listbox.get(suggestion_listbox.curselection())
        user_var.set(selected)
        suggestion_listbox.delete(0, tk.END)
    return "break"

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
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)  # Reduced size for the smaller screen
        img_tk = ImageTk.PhotoImage(img)
        photo_label.config(image=img_tk)
        photo_label.image = img_tk
        photo_label.photo_path = photo_path
        photo_status.config(text="Photo captured!", fg="green")
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
    if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()

# Main container setup
container = tk.Frame(root, bg="#f5f5f5")
container.pack(fill="both", expand=True)

# Create all frames
frames = {}
for F in ("StartPage", "UserPage", "LocationPage", "ActionPage", "ItemPage", "PhotoPage", "VibePage", "EndPage"):
    frame = tk.Frame(container, bg="#f5f5f5")
    frames[F] = frame
    frame.grid(row=0, column=0, sticky="nsew")

# ====== Start Page ======
start_frame = frames["StartPage"]
header_start = tk.Frame(start_frame, bg="#e0e0e0", height=30)  # Reduced height
header_start.pack(fill="x")
tk.Label(header_start, text="SPIERS Smart System", font=("Arial", 12, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_start = tk.Frame(start_frame, bg="white", bd=1, relief="groove")
content_start.pack(pady=10, padx=10, fill="both", expand=True)
start_btn = ttk.Button(content_start, text="Start Session", style="Primary.TButton",
                       command=lambda: show_frame(frames["UserPage"]))
start_btn.pack(pady=10)

# ====== User Page ======
user_frame = frames["UserPage"]
header_user = tk.Frame(user_frame, bg="#e0e0e0", height=30)
header_user.pack(fill="x")
tk.Label(header_user, text="Step 1: Technician", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_user = tk.Frame(user_frame, bg="white", bd=1, relief="groove")
content_user.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_user, text="Who are you?", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(pady=5)
user_entry = ttk.Entry(content_user, textvariable=user_var, font=("Arial", 10))
user_entry.pack(pady=5)
suggestion_listbox = tk.Listbox(content_user, height=3, font=("Arial", 10), bg="#f0f0f0", relief="flat", bd=1, highlightthickness=0)
suggestion_listbox.pack(pady=5, padx=10, fill="x")
user_entry.bind("<KeyRelease>", update_suggestions)
suggestion_listbox.bind("<Double-Button-1>", select_suggestion)
suggestion_listbox.bind("<Return>", select_suggestion)

nav_frame_user = tk.Frame(content_user, bg="white")
nav_frame_user.pack(pady=10, side="bottom", anchor="center")
back_btn_user = ttk.Button(nav_frame_user, text="Back", style="Secondary.TButton",
                           command=lambda: go_back(user_frame))
back_btn_user.pack(side="left", padx=5)
next_btn_user = ttk.Button(nav_frame_user, text="Next", style="Primary.TButton",
                           command=lambda: go_next(user_frame, frames["LocationPage"], user_var, "Technician identification"))
next_btn_user.pack(side="left", padx=5)

# ====== Location Page ======
location_frame = frames["LocationPage"]
header_location = tk.Frame(location_frame, bg="#e0e0e0", height=30)
header_location.pack(fill="x")
tk.Label(header_location, text="Step 2: Location", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_location = tk.Frame(location_frame, bg="white", bd=1, relief="groove")
content_location.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_location, text="Where are you?", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(pady=5)
location_dropdown = ttk.Combobox(content_location, textvariable=location_var,
                                 values=["New Battery Section", "Old Battery Section"], font=("Arial", 10))
location_dropdown.pack(pady=5)

nav_frame_location = tk.Frame(content_location, bg="white")
nav_frame_location.pack(pady=10, side="bottom", anchor="center")
back_btn_location = ttk.Button(nav_frame_location, text="Back", style="Secondary.TButton",
                               command=lambda: go_back(location_frame))
back_btn_location.pack(side="left", padx=5)
next_btn_location = ttk.Button(nav_frame_location, text="Next", style="Primary.TButton",
                               command=lambda: go_next(location_frame, frames["ActionPage"], location_var, "Location selection"))
next_btn_location.pack(side="left", padx=5)

# ====== Action Page ======
action_frame = frames["ActionPage"]
header_action = tk.Frame(action_frame, bg="#e0e0e0", height=30)
header_action.pack(fill="x")
tk.Label(header_action, text="Step 3: Action", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_action = tk.Frame(action_frame, bg="white", bd=1, relief="groove")
content_action.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_action, text="What are you doing?", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(pady=5)
action_dropdown = ttk.Combobox(content_action, textvariable=action_var,
                               values=["Find", "Receive", "Ship", "Move"], font=("Arial", 10))
action_dropdown.pack(pady=5)

nav_frame_action = tk.Frame(content_action, bg="white")
nav_frame_action.pack(pady=10, side="bottom", anchor="center")
back_btn_action = ttk.Button(nav_frame_action, text="Back", style="Secondary.TButton",
                             command=lambda: go_back(action_frame))
back_btn_action.pack(side="left", padx=5)
next_btn_action = ttk.Button(nav_frame_action, text="Next", style="Primary.TButton",
                             command=lambda: go_next(action_frame, frames["ItemPage"], action_var, "Action selection"))
next_btn_action.pack(side="left", padx=5)

# ====== Item Page ======
item_frame = frames["ItemPage"]
header_item = tk.Frame(item_frame, bg="#e0e0e0", height=30)
header_item.pack(fill="x")
tk.Label(header_item, text="Step 4: Item", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_item = tk.Frame(item_frame, bg="white", bd=1, relief="groove")
content_item.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_item, text="Scan/Select Battery", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(pady=5)

barcode_label = tk.Label(content_item, text="Scan Barcode:", font=("Arial", 10), bg="white", fg="#333333")
barcode_label.pack(pady=2)
barcode_entry = ttk.Entry(content_item, textvariable=item_var, font=("Arial", 10))
barcode_entry.pack(pady=2)

item_label = tk.Label(content_item, text="Or Select:", font=("Arial", 10), bg="white", fg="#333333")
item_label.pack(pady=2)
item_dropdown = ttk.Combobox(content_item, textvariable=item_var,
                             values=["Battery 1", "Battery 2", "Custom Item"], font=("Arial", 10))
item_dropdown.pack(pady=2)

barcode_status = tk.Label(content_item, text="", font=("Arial", 8), bg="white")
barcode_status.pack(pady=2)

def process_barcode(event):
    barcode = item_var.get().strip()
    if barcode:
        barcode_status.config(text=f"Barcode scanned!", fg="green")
        item_var.set(barcode)
    else:
        barcode_status.config(text="No barcode!", fg="red")
        item_var.set("")
    return "break"

barcode_entry.bind("<Return>", process_barcode)
barcode_entry.focus_set()

nav_frame_item = tk.Frame(content_item, bg="white")
nav_frame_item.pack(pady=10, side="bottom", anchor="center")
back_btn_item = ttk.Button(nav_frame_item, text="Back", style="Secondary.TButton",
                           command=lambda: go_back(item_frame))
back_btn_item.pack(side="left", padx=5)
next_btn_item = ttk.Button(nav_frame_item, text="Next", style="Primary.TButton",
                           command=lambda: go_next(item_frame, frames["PhotoPage"], item_var, "Item identification"))
next_btn_item.pack(side="left", padx=5)

# ====== Photo Page ======
photo_frame = frames["PhotoPage"]
header_photo = tk.Frame(photo_frame, bg="#e0e0e0", height=30)
header_photo.pack(fill="x")
tk.Label(header_photo, text="Step 5: Photo", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_photo = tk.Frame(photo_frame, bg="white", bd=1, relief="groove")
content_photo.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_photo, text="Take Photo", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(pady=5)

shadow_frame = tk.Frame(content_photo, bg="#d0d0d0")
shadow_frame.pack(pady=5)
photo_container = tk.Frame(shadow_frame, bg="white", width=350, height=250)  # Scaled down for the screen
photo_container.pack(padx=2, pady=2)
photo_container.pack_propagate(False)

photo_label = tk.Label(photo_container, bg="white", relief="ridge", borderwidth=2)
photo_label.place(relx=0.5, rely=0.5, anchor="center", width=300, height=200)

photo_status = tk.Label(content_photo, text="", font=("Arial", 8), bg="white")
photo_status.pack(pady=2)
capture_btn = ttk.Button(content_photo, text="📸 Capture", style="Primary.TButton", command=take_photo)
capture_btn.pack(pady=2)
retake_btn = ttk.Button(content_photo, text="🔄 Retake", style="Danger.TButton", command=take_photo)
retake_btn.pack(pady=2)

nav_frame_photo = tk.Frame(content_photo, bg="white")
nav_frame_photo.pack(pady=10, side="bottom", anchor="center")
back_btn_photo = ttk.Button(nav_frame_photo, text="Back", style="Secondary.TButton",
                            command=lambda: go_back(photo_frame))
back_btn_photo.pack(side="left", padx=5)
next_btn_photo = ttk.Button(nav_frame_photo, text="Next", style="Primary.TButton",
                            command=lambda: go_next(photo_frame, frames["VibePage"], tk.StringVar(value=getattr(photo_label, "photo_path", "")), "Battery photo"))
next_btn_photo.pack(side="left", padx=5)

# ====== Vibe Page ======
vibe_frame = frames["VibePage"]
header_vibe = tk.Frame(vibe_frame, bg="#e0e0e0", height=30)
header_vibe.pack(fill="x")
tk.Label(header_vibe, text="Step 6: Status", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_vibe = tk.Frame(vibe_frame, bg="white", bd=1, relief="groove")
content_vibe.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_vibe, text="How are you?", font=("Arial", 10, "bold"), bg="white", fg="#333333").pack(pady=5)
tk.Label(content_vibe, text="Select status:", font=("Arial", 8), bg="white", fg="#333333").pack(pady=2)
vibe_options = [
    ("😊 Confident", "confident"),
    ("😌 Calm", "calm"),
    ("😐 Neutral", "neutral"),
    ("😟 Stressed", "stressed"),
    ("😴 Fatigued", "fatigued"),
    ("🚀 Energized", "energized")
]
for text, value in vibe_options:
    rb = ttk.Radiobutton(content_vibe, text=text, value=value, variable=vibe_var, style="TRadiobutton")
    rb.pack(anchor="w", padx=20, pady=2)

nav_frame_vibe = tk.Frame(content_vibe, bg="white")
nav_frame_vibe.pack(pady=10, side="bottom", anchor="center")
back_btn_vibe = ttk.Button(nav_frame_vibe, text="Back", style="Secondary.TButton",
                           command=lambda: go_back(vibe_frame))
back_btn_vibe.pack(side="left", padx=5)
submit_btn_vibe = ttk.Button(nav_frame_vibe, text="Submit", style="Primary.TButton",
                             command=lambda: go_next(vibe_frame, frames["EndPage"], vibe_var, "Operator status check") or save_data())
submit_btn_vibe.pack(side="left", padx=5)

# ====== End Page ======
end_frame = frames["EndPage"]
header_end = tk.Frame(end_frame, bg="#e0e0e0", height=30)
header_end.pack(fill="x")
tk.Label(header_end, text="Step 7: Done", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333333").pack(pady=5)

content_end = tk.Frame(end_frame, bg="white", bd=1, relief="groove")
content_end.pack(pady=10, padx=10, fill="both", expand=True)
tk.Label(content_end, text="SPIERS System", font=("Arial", 12, "bold"), bg="white", fg="#333333").pack(pady=5)
tk.Label(content_end, text="Thank you!\nOperation logged.", font=("Arial", 10), bg="white", fg="#333333").pack(pady=5)
tk.Label(content_end, text="Next?", font=("Arial", 10), bg="white", fg="#333333").pack(pady=5)

btn_frame = tk.Frame(content_end, bg="white")
btn_frame.pack(pady=10)
new_op_btn = ttk.Button(btn_frame, text="New Op", style="Primary.TButton", command=reset_session)
new_op_btn.pack(side="left", padx=5)
end_session_btn = ttk.Button(btn_frame, text="Exit", style="Danger.TButton", command=confirm_exit)
end_session_btn.pack(side="left", padx=5)

# Initialize database and start application
setup_database()
show_frame(frames["StartPage"])
root.mainloop()
