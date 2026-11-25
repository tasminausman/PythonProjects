"""
Student Management System (Pandas + NumPy version)
Concepts: Python basics + pandas DataFrame (store and filter data)
          + numpy (mean, median, std, min, max).
"""

import numpy as np
import pandas as pd

SUBJECTS = ("Math", "English", "Science")      # tuple: fixed data
COLUMNS = ["roll", "name", "city", "Math", "English", "Science"]

# DataFrame = a table. Each row is one student.
students = pd.DataFrame(columns=COLUMNS)


# ---------- Helper functions ----------

def get_grade(avg):
    if avg >= 80:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 40:
        return "C"
    else:
        return "Fail"


def build_report():
    # Copy the table and add two new columns: Average and Grade
    report = students.copy()
    marks = report[list(SUBJECTS)].to_numpy(dtype=float)   # numpy array
    report["Average"] = np.round(np.mean(marks, axis=1), 1)  # mean of each row
    report["Grade"] = report["Average"].apply(get_grade)
    return report


def roll_exists(roll):
    return roll in students["roll"].values


def ask_marks(subject):
    # Keep asking until the user types a valid number from 0 to 100
    while True:
        value = input(f"  {subject} marks (0-100): ")
        if value.isdigit() and 0 <= int(value) <= 100:
            return int(value)
        print("  Invalid input. Enter a whole number between 0 and 100.")


# ---------- Menu actions ----------

def add_student():
    roll = input("Roll number: ").strip()
    if roll_exists(roll):
        print("A student with this roll number already exists.")
        return
    name = input("Name: ").strip().title()
    city = input("City: ").strip().title()

    marks = []
    for subject in SUBJECTS:
        marks.append(ask_marks(subject))

    # add a new row at the end of the table
    students.loc[len(students)] = [roll, name, city] + marks
    print(f"Student {name} added successfully!")


def view_all():
    if len(students) == 0:
        print("No students yet.")
        return
    report = build_report()
    print()
    print(report[["roll", "name", "city", "Average", "Grade"]].to_string(index=False))


def search_student():
    roll = input("Enter roll number to search: ").strip()
    if not roll_exists(roll):
        print("Student not found.")
        return
    report = build_report()
    row = report[report["roll"] == roll].iloc[0]       # filter rows, take the first
    print(f"\nRoll: {row['roll']}  |  Name: {row['name']}  |  City: {row['city']}")
    for subject in SUBJECTS:
        print(f"  {subject}: {row[subject]}")
    print(f"  Average: {row['Average']}  |  Grade: {row['Grade']}")


def update_marks():
    roll = input("Enter roll number to update: ").strip()
    if not roll_exists(roll):
        print("Student not found.")
        return
    for subject in SUBJECTS:
        students.loc[students["roll"] == roll, subject] = ask_marks(subject)
    print("Marks updated!")


def delete_student():
    roll = input("Enter roll number to delete: ").strip()
    if not roll_exists(roll):
        print("Student not found.")
        return
    row_index = students.index[students["roll"] == roll]
    students.drop(row_index, inplace=True)
    students.reset_index(drop=True, inplace=True)
    print("Student deleted.")


def show_statistics():
    if len(students) == 0:
        print("No students yet.")
        return
    report = build_report()
    averages = report["Average"].to_numpy()
    topper = report.loc[report["Average"].idxmax(), "name"]

    print("\n----- Class Statistics -----")
    print(f"Total students  : {len(report)}")
    print(f"Class average   : {np.mean(averages):.1f}")
    print(f"Median average  : {np.median(averages):.1f}")
    print(f"Std deviation   : {np.std(averages):.1f}")
    print(f"Highest average : {np.max(averages):.1f} ({topper})")
    print(f"Lowest average  : {np.min(averages):.1f}")
    print(f"Cities          : {', '.join(sorted(report['city'].unique()))}")
    print("\nSubject-wise average:")
    for subject in SUBJECTS:
        print(f"  {subject}: {np.mean(report[subject].to_numpy(dtype=float)):.1f}")
    print("\nStudents per grade:")
    print(report["Grade"].value_counts().to_string())


def show_ranking():
    if len(students) == 0:
        print("No students yet.")
        return
    report = build_report().sort_values("Average", ascending=False)
    print("\n----- Ranking -----")
    position = 1
    for _, row in report.iterrows():
        print(f"{position}. {row['name']} - {row['Average']}")
        position += 1


def export_csv():
    if len(students) == 0:
        print("No students yet.")
        return
    build_report().to_csv("students_report.csv", index=False)
    print("Saved as students_report.csv")


# ---------- Main program ----------

def main():
    print("=== Student Management System ===")
    while True:
        print("\n1) Add student")
        print("2) View all students")
        print("3) Search student")
        print("4) Update marks")
        print("5) Delete student")
        print("6) Class statistics")
        print("7) Ranking")
        print("8) Export report to CSV")
        print("9) Exit")

        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_marks()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            show_statistics()
        elif choice == "7":
            show_ranking()
        elif choice == "8":
            export_csv()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")


if __name__ == "__main__":
    main()
