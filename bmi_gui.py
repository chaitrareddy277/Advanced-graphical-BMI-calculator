import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt
conn = sqlite3.connect("bmi_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
def calculate():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        if weight <= 0 or height <= 0:
            raise ValueError
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        date = datetime.date.today().isoformat()
        result_label.config(text=f"BMI: {bmi} ({category})")
        cursor.execute(
            "INSERT INTO bmi_records VALUES (NULL,?,?,?,?,?,?)",
            (name, weight, height, bmi, category, date)
        )
        conn.commit()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid weight and height")
def show_history():
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE name=?", (name_entry.get(),))
    records = cursor.fetchall()
    if not records:
        messagebox.showinfo("No Data", "No BMI records found")
        return
    dates = [r[0] for r in records]
    bmis = [r[1] for r in records]
    plt.plot(dates, bmis, marker='o')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x400")
tk.Label(root, text="BMI Calculator", font=("Arial", 16)).pack(pady=10)
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()
tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()
tk.Label(root, text="Height (m)").pack()
height_entry = tk.Entry(root)
height_entry.pack()
tk.Button(root, text="Calculate BMI", command=calculate).pack(pady=10)
tk.Button(root, text="View BMI History", command=show_history).pack(pady=5)
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)
root.mainloop()