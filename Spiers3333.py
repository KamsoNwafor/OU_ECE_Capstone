import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import cv2
from PIL import Image, ImageTk

# Initialize main window
root = tk.Tk()
root.title("EV Battery Solutions")
root.geometry("500x600")
root.configure(bg="white")

# Create Tkinter variables
user_var = tk.StringVar()
location_var = tk.StringVar()
item_var = tk.StringVar()
action_var = tk.StringVar()
vibe_var = tk.StringVar()

# Database setup
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

# Validation function for each step
def validate_step(field_value, field_name, current_frame, next_frame):
    if not field_value.strip():
        messagebox.showerror("Missing Information", f"Please complete: {field_name}", parent=root)
        show_frame(current_frame)
        return False
    return True

# Save function with detailed validation
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
        conn.commit()
        show_frame(frames["EndPage"])
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to save data: {str(e)}")
    finally:
        if conn:
            conn.close()

# Predictive text functions
def update_suggestions(event):
    typed = user_var.get().strip()
    suggestion_listbox.delete(0, tk.END)
    if len(typed) < 1:
        return
    conn = sqlite3.connect("evbs_data.db")
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
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
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

# Start Page
start_frame = frames["StartPage"]
tk.Label(start_frame, text="SPIERS Technologies Smart System", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
tk.Button(start_frame, text="Start Session", font=("Arial", 14), bg="#004aad", fg="white",
          command=lambda: show_frame(frames["UserPage"])).pack(pady=10)

# User Page
user_frame = frames["UserPage"]
tk.Label(user_frame, text="Who are you", font=("Arial", 14), bg="white").pack(pady=20)
user_entry = ttk.Entry(user_frame, textvariable=user_var, font=("Arial", 12))
user_entry.pack(pady=5)
suggestion_listbox = tk.Listbox(user_frame, height=4, font=("Arial", 12), bg="white", relief="flat")
suggestion_listbox.pack()
user_entry.bind("<KeyRelease>", update_suggestions)
suggestion_listbox.bind("<Double-Button-1>", select_suggestion)
suggestion_listbox.bind("<Return>", select_suggestion)
tk.Button(user_frame, text="Next →", 
          command=lambda: validate_step(user_var.get(), "Technician identification", frames["UserPage"], frames["LocationPage"]) and show_frame(frames["LocationPage"]),
          bg="#004aad", fg="white").pack(pady=10)

# Location Page
location_frame = frames["LocationPage"]
tk.Label(location_frame, text="Where are you?", font=("Arial", 14), bg="white").pack(pady=20)
location_dropdown = ttk.Combobox(location_frame, textvariable=location_var,
                                 values=["New Battery Section", "Old Battery Section"], font=("Arial", 12))
location_dropdown.pack()
tk.Button(location_frame, text="Next →", 
          command=lambda: validate_step(location_var.get(), "Location selection", frames["LocationPage"], frames["ActionPage"]) and show_frame(frames["ActionPage"]),
          bg="#004aad", fg="white").pack(pady=10)

# Action Page
action_frame = frames["ActionPage"]
tk.Label(action_frame, text="What are you trying to do?", font=("Arial", 14), bg="white").pack(pady=20)
action_dropdown = ttk.Combobox(action_frame, textvariable=action_var,
                               values=["Find", "Receive", "Ship", "Move"], font=("Arial", 12))
action_dropdown.pack()
tk.Button(action_frame, text="Next →", 
          command=lambda: validate_step(action_var.get(), "Action selection", frames["ActionPage"], frames["ItemPage"]) and show_frame(frames["ItemPage"]),
          bg="#004aad", fg="white").pack(pady=10)

# Item Page
item_frame = frames["ItemPage"]
tk.Label(item_frame, text="Input the Item you are working on", font=("Arial", 14), bg="white").pack(pady=20)
item_dropdown = ttk.Combobox(item_frame, textvariable=item_var,
                             values=["Battery 1", "Battery 2", "Custom Item Entry"], font=("Arial", 12))
item_dropdown.pack()
tk.Button(item_frame, text="Scan Battery →", 
          command=lambda: validate_step(item_var.get(), "Item identification", frames["ItemPage"], frames["PhotoPage"]) and show_frame(frames["PhotoPage"]),
          bg="#004aad", fg="white").pack(pady=10)

# Photo Page
photo_frame = frames["PhotoPage"]
tk.Label(photo_frame, text="Take the photo of the item", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
photo_label = tk.Label(photo_frame, bg="white", height=15, width=30, relief="sunken")
photo_label.pack(pady=10)
photo_status = tk.Label(photo_frame, text="", bg="white")
photo_status.pack()
tk.Button(photo_frame, text="📸 Capture Image", command=take_photo,
          bg="#004aad", fg="white").pack(pady=5)
tk.Button(photo_frame, text="Quality Check →", 
          command=lambda: validate_step(getattr(photo_label, "photo_path", ""), "Battery photo", frames["PhotoPage"], frames["VibePage"]) and show_frame(frames["VibePage"]),
          bg="#004aad", fg="white").pack(pady=10)

# Vibe Page
vibe_frame = frames["VibePage"]
tk.Label(vibe_frame, text="How are you feeling about this activity?", font=("Arial", 14, "bold"), bg="white").pack(pady=20)
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
tk.Button(vibe_frame, text="Submit Report", 
          command=lambda: validate_step(vibe_var.get(), "Operator status check", frames["VibePage"], frames["EndPage"]) and save_data(),
          bg="#004aad", fg="white", font=("Arial", 12)).pack(pady=20)

# End Page
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
          bg="#ff4444", fg="white", width=15).pack(side="right", padx=10)

# Initialize database and start application
setup_database()
show_frame(frames["StartPage"])
root.mainloop()
