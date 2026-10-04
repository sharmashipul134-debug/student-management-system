import json
from pathlib import Path

FILE = "students.json"


# Load students from JSON file
def load_students():
    if Path(FILE).exists():
        with open(FILE, "r") as file:
            return json.load(file)

    return []


# Save students to JSON file
def save_students(students):
    with open(FILE, "w") as file:
        json.dump(students, file, indent=4)


# CREATE
def add_student():

    students = load_students()

    roll_no = input("Enter Roll Number: ")

    # Check duplicate roll number
    for student in students:
        if student["roll_no"] == roll_no:
            print("Roll number already exists!")
            return

    name = input("Enter Name: ")
    age = input("Enter Age: ")
    course = input("Enter Course: ")
    marks = input("Enter Marks: ")

    student = {
        "roll_no": roll_no,
        "name": name,
        "age": age,
        "course": course,
        "marks": marks
    }

    students.append(student)

    save_students(students)

    print("Student added successfully!")


# READ
def view_students():

    print("VIEW FUNCTION STARTED")

    students = load_students()

    print("Students data:", students)

    if not students:
        print("No students found.")
        return

    print("\n===== STUDENT DETAILS =====")

    for student in students:
        print("Roll No :", student["roll_no"])
        print("Name    :", student["name"])
        print("Age     :", student["age"])
        print("Course  :", student["course"])
        print("Marks   :", student["marks"])
        print("----------------------------")


# UPDATE
def update_student():

    students = load_students()

    roll_no = input("Enter Roll Number to update: ")

    for student in students:

        if student["roll_no"] == roll_no:

            student["name"] = input("Enter new name: ")
            student["age"] = input("Enter new age: ")
            student["course"] = input("Enter new course: ")
            student["marks"] = input("Enter new marks: ")

            save_students(students)

            print("Student updated successfully!")

            return

    print("Student not found!")


# DELETE
def delete_student():

    students = load_students()

    roll_no = input("Enter Roll Number to delete: ")

    for student in students:

        if student["roll_no"] == roll_no:

            students.remove(student)

            save_students(students)

            print("Student deleted successfully!")

            return

    print("Student not found!")


# MAIN MENU
while True:

    print("\n================================")
    print("    STUDENT MANAGEMENT SYSTEM")
    print("================================")

    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")