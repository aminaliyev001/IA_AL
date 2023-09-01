import tkinter as tk
import sqlite3
from tkinter import messagebox
import style 
from dashboard import create_dashboard_page 
import queries as queries_module
import random, string

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
queries_module.start(conn,cursor)
def generate_random_pin(length=8):
    return ''.join(random.choices(string.digits, k=length))
cursor.execute("SELECT * FROM users WHERE email=?", ('teymuraliyev@gmail.com',))
result = cursor.fetchone()
if not result:
    cursor.execute("""
        INSERT INTO users (name, surname, email, password, pin)
        VALUES (?, ?, ?, ?, ?)
    """, ("Teymur", "Aliyev", "teymuraliyev@gmail.com", "1234",generate_random_pin()))
    conn.commit()
def get_user(email, password):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            return None
        else:
            return {
                "id": user[0],
                "name": user[1],
                "surname": user[2],
                "current_weight": user[3],
                "target_weight": user[4],
                "height": user[5],
                "pin": user[6],
                "email": user[7],
                "password": user[8]
            }
def check_credentials(username_entry, password_entry):
    email = username_entry.get()
    password = password_entry.get()
    user = get_user(email, password)
    if email == "" or password == "":
        messagebox.showwarning("Fields Empty", "Please enter username and password")
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    result = cursor.fetchone()
    if result:
        conn.close()
        root.destroy()  
        create_dashboard_page(user)
    else:
        messagebox.showerror("Error", "Wrong credentials.")
def main():
    global root
    root = tk.Tk()
    root.title("Login")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (style.WINDOW_WIDTH/2)
    y = (screen_height/2) - (style.WINDOW_HEIGHT/2)

    root.geometry('%dx%d+%d+%d' % (style.WINDOW_WIDTH, style.WINDOW_HEIGHT, x, y))

    root.configure(bg=style.WINDOW_BACKGROUND)

    title_label = tk.Label(root, text="Login Page", **style.HEADER_STYLE)
    title_label.pack(pady=20)

    username_label = tk.Label(root, text="Username", **style.LABEL_STYLE)
    username_label.pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    password_label = tk.Label(root, text="Password", **style.LABEL_STYLE)
    password_label.pack()
    password_entry = tk.Entry(root, show='*')
    password_entry.pack()

    login_button = tk.Button(root, text="Send", **style.BUTTON_STYLE,
                            command=lambda: check_credentials(username_entry, password_entry))
    login_button.pack(pady=20)

    root.mainloop()

    conn.close()
if __name__ == "__main__":
    main()