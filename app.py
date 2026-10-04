import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ==========================================
# DATABASE
# ==========================================

def connect_database():
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            course TEXT,
            marks REAL
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# ADD STUDENT
# ==========================================

def add_student():

    roll_no = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()

    if roll_no == "" or name == "":
        messagebox.showerror(
            "Error",
            "Roll Number and Name are required!"
        )
        return

    try:
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students
            (roll_no, name, age, course, marks)
            VALUES (?, ?, ?, ?, ?)
        """, (roll_no, name, age, course, marks))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Roll Number already exists!"
        )


# ==========================================
# VIEW STUDENTS
# ==========================================

def view_students():

    for row in student_table.get_children():
        student_table.delete(row)

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, roll_no, name, age, course, marks
        FROM students
    """)

    students = cursor.fetchall()

    connection.close()

    for student in students:
        student_table.insert(
            "",
            tk.END,
            values=student
        )


# ==========================================
# SELECT STUDENT
# ==========================================

def select_student(event):

    selected = student_table.focus()

    if selected == "":
        return

    values = student_table.item(
        selected,
        "values"
    )

    clear_fields()

    roll_entry.insert(0, values[1])
    name_entry.insert(0, values[2])
    age_entry.insert(0, values[3])
    course_entry.insert(0, values[4])
    marks_entry.insert(0, values[5])


# ==========================================
# UPDATE STUDENT
# ==========================================

def update_student():

    selected = student_table.focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Please select a student first!"
        )
        return

    values = student_table.item(
        selected,
        "values"
    )

    student_id = values[0]

    roll_no = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()
    marks = marks_entry.get()

    if roll_no == "" or name == "":
        messagebox.showerror(
            "Error",
            "Roll Number and Name are required!"
        )
        return

    try:
        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE students
            SET roll_no = ?,
                name = ?,
                age = ?,
                course = ?,
                marks = ?
            WHERE id = ?
        """, (
            roll_no,
            name,
            age,
            course,
            marks,
            student_id
        ))

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Roll Number already exists!"
        )


# ==========================================
# DELETE STUDENT
# ==========================================

def delete_student():

    selected = student_table.focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Please select a student first!"
        )
        return

    values = student_table.item(
        selected,
        "values"
    )

    student_id = values[0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:

        connection = sqlite3.connect("student.db")
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        connection.commit()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

        clear_fields()
        view_students()


# ==========================================
# SEARCH STUDENT
# ==========================================

def search_student():

    search_text = search_entry.get()

    for row in student_table.get_children():
        student_table.delete(row)

    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, roll_no, name, age, course, marks
        FROM students
        WHERE roll_no LIKE ?
        OR name LIKE ?
        OR course LIKE ?
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    students = cursor.fetchall()

    connection.close()

    for student in students:
        student_table.insert(
            "",
            tk.END,
            values=student
        )


# ==========================================
# CLEAR FIELDS
# ==========================================

def clear_fields():

    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


# ==========================================
# MAIN WINDOW
# ==========================================

connect_database()

root = tk.Tk()

root.title("Student Management System")

root.geometry("1000x650")

root.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold")
)

title.pack(pady=20)


# ==========================================
# INPUT FRAME
# ==========================================

input_frame = tk.Frame(root)

input_frame.pack(pady=10)


# Roll Number

tk.Label(
    input_frame,
    text="Roll Number",
    font=("Arial", 12)
).grid(row=0, column=0, padx=10, pady=8)

roll_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

roll_entry.grid(row=0, column=1)


# Name

tk.Label(
    input_frame,
    text="Name",
    font=("Arial", 12)
).grid(row=1, column=0, padx=10, pady=8)

name_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

name_entry.grid(row=1, column=1)


# Age

tk.Label(
    input_frame,
    text="Age",
    font=("Arial", 12)
).grid(row=2, column=0, padx=10, pady=8)

age_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

age_entry.grid(row=2, column=1)


# Course

tk.Label(
    input_frame,
    text="Course",
    font=("Arial", 12)
).grid(row=3, column=0, padx=10, pady=8)

course_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

course_entry.grid(row=3, column=1)


# Marks

tk.Label(
    input_frame,
    text="Marks",
    font=("Arial", 12)
).grid(row=4, column=0, padx=10, pady=8)

marks_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

marks_entry.grid(row=4, column=1)


# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(root)

button_frame.pack(pady=15)


tk.Button(
    button_frame,
    text="ADD",
    width=12,
    command=add_student
).grid(row=0, column=0, padx=5)


tk.Button(
    button_frame,
    text="UPDATE",
    width=12,
    command=update_student
).grid(row=0, column=1, padx=5)


tk.Button(
    button_frame,
    text="DELETE",
    width=12,
    command=delete_student
).grid(row=0, column=2, padx=5)


tk.Button(
    button_frame,
    text="CLEAR",
    width=12,
    command=clear_fields
).grid(row=0, column=3, padx=5)


# ==========================================
# SEARCH
# ==========================================

search_frame = tk.Frame(root)

search_frame.pack(pady=10)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 12)
).pack(side=tk.LEFT, padx=5)


search_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 12)
)

search_entry.pack(side=tk.LEFT, padx=5)


tk.Button(
    search_frame,
    text="SEARCH",
    width=12,
    command=search_student
).pack(side=tk.LEFT, padx=5)


tk.Button(
    search_frame,
    text="SHOW ALL",
    width=12,
    command=view_students
).pack(side=tk.LEFT, padx=5)


# ==========================================
# TABLE
# ==========================================

table_frame = tk.Frame(root)

table_frame.pack(pady=15)


columns = (
    "ID",
    "Roll No",
    "Name",
    "Age",
    "Course",
    "Marks"
)


student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:

    student_table.heading(
        column,
        text=column
    )

    student_table.column(
        column,
        width=130
    )


student_table.pack()

student_table.bind(
    "<ButtonRelease-1>",
    select_student
)


# ==========================================
# START APPLICATION
# ==========================================

view_students()

root.mainloop()