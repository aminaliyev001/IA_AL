import tkinter as tk
from tkinter import ttk
import sqlite3

def main(user):
    def calculate():
        weight_text = weight_entry.get()
        height_text = height_entry.get()
        target_weight_text = target_weight_entry.get()

        if not weight_text or not height_text or not target_weight_text:
            result_label.config(text="Please fill in all fields.")
            return

        try:
            weight = float(weight_text)
            height_cm = float(height_text)
            target_weight = float(target_weight_text)

            if (target_weight-1) > weight:
                target_label.config(text="Target weight should be at least 1 kg less than current weight!")
            else:
                height_m = height_cm / 100  
                bmi = weight / (height_m ** 2)
                result_label.config(text=f"Your BMI: {bmi:.2f}")
                target_label.config(text=f"Target weight: {target_weight:.2f}")
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users
                    SET target_weight = ?, current_weight = ?, height = ?
                    WHERE email = ? AND password = ?
                """, (target_weight, weight, height_cm, user["email"], user["password"] ) )
                conn.commit()
                root.destroy()  
                conn.close()
        except ValueError:
            result_label.config(text="Please enter valid numeric values.")

    root = tk.Tk()
    root.title("Fill the form")

    weight_label = tk.Label(root, text="Weight (kg):")
    weight_label.pack()
    weight_entry = tk.Entry(root)
    weight_entry.pack()

    height_label = tk.Label(root, text="Height (cm):")
    height_label.pack()
    height_entry = tk.Entry(root)
    height_entry.pack()

    target_weight_label = tk.Label(root, text="Target Weight (kg, 1 kg less than current):")
    target_weight_label.pack()
    target_weight_entry = tk.Entry(root)
    target_weight_entry.pack()

    calculate_button = ttk.Button(root, text="Enter", command=calculate)
    calculate_button.pack()

    result_label = tk.Label(root, text="", font=("Helvetica", 14))
    result_label.pack()

    target_label = tk.Label(root, text="", font=("Helvetica", 14))
    target_label.pack()

    root.mainloop()
