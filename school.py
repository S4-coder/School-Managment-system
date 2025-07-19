import tkinter as tk
from tkinter import messagebox, ttk
import os

DATA_FILE = "school.txt"

def save_student():
    roll = roll_entry.get().strip()
    name = name_entry.get().strip()
    clas = class_entry.get().strip()
    section = section_entry.get().strip()

    if not all([roll, name, clas, section]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    with open(DATA_FILE, "a") as f:
        f.write(f"{roll},{name},{clas},{section}\n")

    messagebox.showinfo("Success", "Student Registered Successfully")
    clear_fields()
    load_students()

def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    section_entry.delete(0, tk.END)

def load_students():
    for row in student_table.get_children():
        student_table.delete(row)

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as f:
        for line in f:
            try:
                roll, name, clas, section = line.strip().split(",")
                student_table.insert("", tk.END, values=(roll, name, clas, section))
            except:
                continue

def search_student():
    roll_search = search_entry.get().strip()
    if not roll_search:
        messagebox.showwarning("Input Error", "Enter Roll Number to Search")
        return

    for row in student_table.get_children():
        student_table.delete(row)

    found = False
    with open(DATA_FILE, "r") as f:
        for line in f:
            try:
                roll, name, clas, section = line.strip().split(",")
                if roll == roll_search:
                    student_table.insert("", tk.END, values=(roll, name, clas, section))
                    found = True
                    break
            except:
                continue

    if not found:
        messagebox.showinfo("Not Found", "No student with this Roll Number")

def delete_student():
    roll_delete = search_entry.get().strip()
    if not roll_delete:
        messagebox.showwarning("Input Error", "Enter Roll Number to Delete")
        return

    if not os.path.exists(DATA_FILE):
        messagebox.showerror("Error", "No student file found")
        return

    lines = []
    deleted = False
    with open(DATA_FILE, "r") as f:
        for line in f:
            try:
                roll, name, clas, section = line.strip().split(",")
                if roll != roll_delete:
                    lines.append(line)
                else:
                    deleted = True
            except:
                continue

    with open(DATA_FILE, "w") as f:
        f.writelines(lines)

    if deleted:
        messagebox.showinfo("Deleted", "Student Deleted Successfully")
    else:
        messagebox.showinfo("Not Found", "Roll Number Not Found")

    load_students()

# ========== GUI Setup ==========
root = tk.Tk()
root.title("📘 School Management System")
root.geometry("750x500")
root.configure(bg="#f0f4f7")

# ========== Register Frame ==========
register_frame = tk.LabelFrame(root, text="Register Student", padx=10, pady=10, bg="#e6f2ff")
register_frame.pack(padx=10, pady=10, fill="x")

tk.Label(register_frame, text="Roll No:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
roll_entry = tk.Entry(register_frame)
roll_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(register_frame, text="Name:", bg="#e6f2ff").grid(row=0, column=2, padx=5, pady=5)
name_entry = tk.Entry(register_frame)
name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(register_frame, text="Class:", bg="#e6f2ff").grid(row=1, column=0, padx=5, pady=5)
class_entry = tk.Entry(register_frame)
class_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(register_frame, text="Section:", bg="#e6f2ff").grid(row=1, column=2, padx=5, pady=5)
section_entry = tk.Entry(register_frame)
section_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Button(register_frame, text="Register", command=save_student, bg="#3399ff", fg="white", width=15).grid(row=2, column=0, columnspan=4, pady=10)

# ========== Search/Delete Frame ==========
search_frame = tk.LabelFrame(root, text="Search / Delete Student", padx=10, pady=10, bg="#e6f2ff")
search_frame.pack(padx=10, pady=5, fill="x")

tk.Label(search_frame, text="Enter Roll No:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(search_frame, text="Search", command=search_student, width=12).grid(row=0, column=2, padx=5)
tk.Button(search_frame, text="Delete", command=delete_student, width=12).grid(row=0, column=3, padx=5)
tk.Button(search_frame, text="Show All", command=load_students, width=12).grid(row=0, column=4, padx=5)

# ========== Table View ==========
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

student_table = ttk.Treeview(table_frame, columns=("roll", "name", "class", "section"), show="headings")
student_table.heading("roll", text="Roll No")
student_table.heading("name", text="Name")
student_table.heading("class", text="Class")
student_table.heading("section", text="Section")

student_table.column("roll", width=80)
student_table.column("name", width=180)
student_table.column("class", width=100)
student_table.column("section", width=100)

student_table.pack(fill="both", expand=True)

load_students()
root.mainloop()
