import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv

# -------------------- Main Window Setup --------------------
root = tk.Tk()
root.title("GPA Calculator")
root.geometry("600x500")
root.configure(bg="#f0f0f0")  # Light gray background

# List to store course data
courses = []

# -------------------- Input Frame --------------------
frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.pack(pady=10)

# Course Name
tk.Label(frame_inputs, text="Course Name:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(frame_inputs, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=5, pady=5)

# Grade
tk.Label(frame_inputs, text="Grade:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
grade_entry = tk.Entry(frame_inputs, font=("Arial", 12))
grade_entry.grid(row=1, column=1, padx=5, pady=5)

# Units
tk.Label(frame_inputs, text="Units:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
unit_entry = tk.Entry(frame_inputs, font=("Arial", 12))
unit_entry.grid(row=2, column=1, padx=5, pady=5)

# -------------------- Courses Table Frame --------------------
frame_table = tk.Frame(root)
frame_table.pack(pady=10, fill=tk.BOTH, expand=True)

# Scrollbar for the table
scrollbar = tk.Scrollbar(frame_table)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview setup (columns: Course, Grade, Units)
columns = ("Course", "Grade", "Units")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", yscrollcommand=scrollbar.set, height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

# -------------------- Functions --------------------
# Add a course
def add_course():
    name = name_entry.get()
    try:
        grade = float(grade_entry.get())
        unit = float(unit_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Grade and Units must be numbers")
        return

    courses.append({"name": name, "grade": grade, "unit": unit})
    tree.insert("", tk.END, values=(name, grade, unit))

    # Clear input fields
    name_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)
    unit_entry.delete(0, tk.END)

# Delete selected course(s)
def delete_course():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a course to delete")
        return
    for item in selected_item:
        tree.delete(item)
        # Also remove from courses list
        values = tree.item(item, "values")
        courses[:] = [c for c in courses if not (c["name"] == values[0] and str(c["grade"]) == str(values[1]) and str(c["unit"]) == str(values[2]))]

# Calculate weighted GPA
def calculate_gpa():
    if not courses:
        messagebox.showerror("Error", "No courses added")
        return

    total = sum(c["grade"] * c["unit"] for c in courses)
    total_units = sum(c["unit"] for c in courses)
    gpa = total / total_units

    messagebox.showinfo("GPA Result", f"Your weighted GPA is: {gpa:.2f}")

# Save courses to CSV
def save_courses():
    if not courses:
        messagebox.showwarning("Warning", "No courses to save")
        return
    with open("courses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Course", "Grade", "Units"])
        for c in courses:
            writer.writerow([c["name"], c["grade"], c["unit"]])
    messagebox.showinfo("Saved", "Courses saved to courses.csv")

# Load courses from CSV
def load_courses():
    try:
        with open("courses.csv", "r") as file:
            reader = csv.DictReader(file)
            courses.clear()
            for row in reader:
                courses.append({"name": row["Course"], "grade": float(row["Grade"]), "unit": float(row["Units"])})
        # Update the table
        tree.delete(*tree.get_children())
        for c in courses:
            tree.insert("", tk.END, values=(c["name"], c["grade"], c["unit"]))
        messagebox.showinfo("Loaded", "Courses loaded from courses.csv")
    except FileNotFoundError:
        messagebox.showwarning("Warning", "courses.csv not found")

# -------------------- Buttons --------------------
frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=10)

# Add course button
add_btn = tk.Button(frame_buttons, text="Add Course", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=15, height=2, command=add_course)
add_btn.grid(row=0, column=0, padx=10)

# Calculate GPA button
calc_btn = tk.Button(frame_buttons, text="Calculate GPA", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=15, height=2, command=calculate_gpa)
calc_btn.grid(row=0, column=1, padx=10)

# Delete selected button
delete_btn = tk.Button(frame_buttons, text="Delete Selected", bg="#f44336", fg="white", font=("Arial", 12, "bold"), width=15, height=2, command=delete_course)
delete_btn.grid(row=0, column=2, padx=10)

# Save button
save_btn = tk.Button(frame_buttons, text="Save", bg="#FFC107", fg="white", font=("Arial", 12, "bold"), width=10, height=2, command=save_courses)
save_btn.grid(row=1, column=0, padx=5, pady=5)

# Load button
load_btn = tk.Button(frame_buttons, text="Load", bg="#9C27B0", fg="white", font=("Arial", 12, "bold"), width=10, height=2, command=load_courses)
load_btn.grid(row=1, column=1, padx=5, pady=5)

# -------------------- Run the main window --------------------
root.mainloop()
