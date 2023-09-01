from tkinter import messagebox
import sqlite3
from tkinter import *
from datetime import datetime
import style
from ask import main
def edit_profile(user,root):
    edit_window = Toplevel(root)
    edit_window.title("Edit Profile")
    
    password_label = Label(edit_window, text="Password:")
    password_label.pack()
    password_entry = Entry(edit_window)
    password_entry.insert(0, user["password"])  # Populate with user's current password
    password_entry.pack()
    
    current_weight_label = Label(edit_window, text="Current Weight:")
    current_weight_label.pack()
    current_weight_entry = Entry(edit_window)
    current_weight_entry.insert(0, user["current_weight"])  # Populate with user's current weight
    current_weight_entry.pack()
    
    target_weight_label = Label(edit_window, text="Target Weight:")
    target_weight_label.pack()
    target_weight_entry = Entry(edit_window)
    target_weight_entry.insert(0, user["target_weight"])  # Populate with user's target weight
    target_weight_entry.pack()
    
    height_label = Label(edit_window, text="Height:")
    height_label.pack()
    height_entry = Entry(edit_window)
    height_entry.insert(0, user["height"])  
    height_entry.pack()
    
    def save_changes():
        new_password = password_entry.get()
        new_current_weight = current_weight_entry.get()
        new_target_weight = target_weight_entry.get()
        new_height = height_entry.get()
        if not new_password or not new_current_weight or not new_target_weight or not new_height:
            messagebox.showinfo(text="Please fill in all fields.")
            return
        if (new_target_weight-1) > new_current_weight:
            messagebox.showinfo(text="Target weight should be at least 1 kg less than current weight!")
        try:
            new_current_weight = float(new_current_weight)
            new_target_weight = float(new_target_weight)
            new_height = float(new_height)
        except ValueError:
            messagebox.showinfo(text="Please enter valid numeric values.")
            return
        
        if(len(new_password) < 8):
            messagebox.showinfo("Warning", "Password length less than 8 can be easy to guess your.")
            return
        
    save_button = Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack()

def calculate_sum_kcal():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT calory FROM records WHERE user_id=?", (userid,))
        records = cursor.fetchall()
        total_calories = sum(record[0] for record in records)
        conn.close()
        return total_calories

def get_bmi_status(bmi):
        if bmi < 16:
            return "Severe Thinness"
        elif bmi < 17:
            return "Moderate Thinness"
        elif bmi < 18.5:
            return "Mild Thinness"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        elif bmi < 35:
            return "Obese Class I"
        elif bmi < 40:
            return "Obese Class II"
        else:
            return "Obese Class III"
def add_calories_burned():
        print("dsa")
        calories_burned = calories_gained_entry.get()
        if calories_burned == "":
            messagebox.showinfo("Error", "Calories burned value is empty.")
            return
        try:
            calories_burned = float(calories_burned)
        except ValueError:
            messagebox.showinfo("Error", "Please enter a valid numeric value.")
            return 
    
        if calories_burned <= 0:
            messagebox.showinfo("Error", "Please enter a positive calorie value.")
            return
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (user_id, date_time, calory)
            VALUES (?, ?, ?)
        """, (userid, datetime.now(), -calories_burned))
        conn.commit()
        calories_message_label.config(text="Calories burned added successfully.")
        kcal_to_burn_label.config(text=str(kcal_to_burn+calculate_sum_kcal())+" kcal left 🔥")
        conn.close()

def add_calories_gained():
        calories_gained = calories_gained_entry.get()
        if calories_gained == "":
            messagebox.showinfo("Error", "Calories gained value is empty.")
            return
        try:
            calories_gained = float(calories_gained)
        except ValueError:
            messagebox.showinfo("Error", "Please enter a valid numeric value.")
            return
        if calories_gained <= 0:
            messagebox.showinfo("Error", "Please enter a positive calorie value.")
            return
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (user_id, date_time, calory)
            VALUES (?, ?, ?)
        """, (userid, datetime.now(), calories_gained))
        conn.commit()
        conn.close()
        calories_message_label.config(text="Calories gained added successfully.")
        kcal_to_burn_label.config(text=str(kcal_to_burn+calculate_sum_kcal())+" kcal left 🔥")

def create_dashboard_page(user):
    global kcal_to_burn,calories_message_label,kcal_to_burn_label,userid,calories_gained_entry,calories_burned_entry
    userid = user["id"]
    if(user["target_weight"] == None):
        main(user)
    quotes = [
    "The only bad workout is the one that didn't happen.",
    "Don't wish for it, work for it.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "The only way to achieve your goals is to start, and the only way to start is to stop talking and begin doing.",
    "The future depends on what you do today.",
    "Believe you can and you're halfway there.",
    "It's not about being the best; it's about being better than you were yesterday."
        ]
    root = Tk()
    root.title("Dashboard")
    root.configure(bg=style.WINDOW_BACKGROUND)


    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (style.WINDOW_WIDTH/2)
    y = (screen_height/2) - (style.WINDOW_HEIGHT/2)
    root.geometry('%dx%d+%d+%d' % (style.WINDOW_WIDTH, style.WINDOW_HEIGHT, x, y))
    root.configure(bg=style.WINDOW_BACKGROUND)

    user_info_frame = Frame(root, bg=style.USER_INFO_BACKGROUND)
    user_info_frame.pack(side="top", fill="x", padx=20, pady=20)

    user_icon = PhotoImage(file="user.png")

    user_icon_label = Label(user_info_frame, image=user_icon, bg=style.USER_INFO_BACKGROUND)
    user_icon_label.image = user_icon
    user_icon_label.pack(side="left", padx=(0, 20))

    user_info_label = Label(
        user_info_frame, 
        text=f"{user['name']} {user['surname']}",
        bg=style.USER_INFO_BACKGROUND,
        fg=style.USER_INFO_TEXT,
        font=style.LARGE_FONT,
        anchor="w"
    )
    user_info_label.pack(side="left")
    exit_button = Button(user_info_frame, text="Exit", command=root.destroy)
    exit_button.pack(side="right", padx=10)

    edit_profile_button = Button(
        user_info_frame,
        text="Edit Profile",
        command=lambda: edit_profile(user,root)  
    )
    edit_profile_button.pack(side="right", padx=10)

    quote_frame = Frame(root, bg=style.QUOTE_BACKGROUND)
    quote_frame.pack(side="top", fill="x", padx=20, pady=10)
    current_day = datetime.today().weekday()
    quote_of_the_day = quotes[current_day] 

    quote_label = Label(
        quote_frame,
        text=f"Quote of the day: {quote_of_the_day}",
        bg=style.QUOTE_BACKGROUND,
        fg=style.QUOTE_TEXT,
        font=style.NORMAL_FONT,
        anchor="w"
    )
    quote_label.pack(side="left", padx=(20, 0))

        
    bmi_frame = Frame(root)
    bmi_frame.pack(padx=20, pady=20)

    height_m = user["height"]  
    bmi = user["current_weight"] / ((height_m/100) ** 2)
    bmi_label = Label(bmi_frame, text=f"Your BMI: {bmi:.2f} ({get_bmi_status(bmi)})")
    bmi_label.pack(pady=10)

    kcal_frame = Frame(root)
    kcal_frame.pack(padx=20, pady=20)

    kcal_to_burn = (float(user["current_weight"]) - float(user["target_weight"])) * 7700

    kcal_to_burn_label = Label(kcal_frame, text=str(kcal_to_burn + calculate_sum_kcal()) + " kcal left 🔥")
    kcal_to_burn_label.grid(row=0, columnspan=2, padx=5, pady=5)

    calories_burned_label = Label(kcal_frame, text="Calories Burned:")
    calories_burned_label.grid(row=1, column=0, padx=5, pady=5)
    
    calories_burned_entry = Entry(kcal_frame)
    calories_burned_entry.grid(row=1, column=1, padx=5, pady=5)

    calories_gained_label = Label(kcal_frame, text="Calories Gained:")
    calories_gained_label.grid(row=2, column=0, padx=5, pady=5)
    
    calories_gained_entry = Entry(kcal_frame)
    calories_gained_entry.grid(row=2, column=1, padx=5, pady=5)

    add_calories_burned_button = Button(kcal_frame, text="Add Calories Burned", command=add_calories_burned)
    add_calories_burned_button.grid(row=3, column=0, padx=5, pady=10)

    add_calories_gained_button = Button(kcal_frame, text="Add Calories Gained", command=add_calories_gained)
    add_calories_gained_button.grid(row=3, column=1, padx=5, pady=10)

    calories_message_label = Label(kcal_frame, text="")
    calories_message_label.grid(row=4, columnspan=2, padx=5, pady=5)

    root.mainloop()