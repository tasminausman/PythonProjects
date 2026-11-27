"""
Student Management System (OOP)
Concepts: inheritance (Student -> Person), encapsulation (private marks),
properties, method overriding, exception handling, NumPy statistics, CSV export.
"""
import csv
import numpy as np


class ValidationError(Exception):
    """Raised when user input fails validation."""


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Name cannot be empty.")
        self._name = value.strip().title()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or not (15 <= value <= 60):
            raise ValidationError("Age must be a whole number between 15 and 60.")
        self._age = value

    def describe(self):
        return f"{self.name}, age {self.age}"


class Student(Person):
    SUBJECTS = ("Math", "Science", "English")

    def __init__(self, roll_no, name, age, marks):
        super().__init__(name, age)
        if not isinstance(roll_no, int) or roll_no <= 0:
            raise ValidationError("Roll number must be a positive integer.")
        self.roll_no = roll_no
        self.__marks = {}          # private (name-mangled) -> encapsulation
        self.set_marks(marks)

    # ---- encapsulated marks ----
    def set_marks(self, marks):
        if len(marks) != len(self.SUBJECTS):
            raise ValidationError(f"Provide marks for {len(self.SUBJECTS)} subjects.")
        for subject, m in zip(self.SUBJECTS, marks):
            if not isinstance(m, (int, float)) or not (0 <= m <= 100):
                raise ValidationError(f"{subject} marks must be between 0 and 100.")
        self.__marks = dict(zip(self.SUBJECTS, marks))

    def get_marks(self):
        return dict(self.__marks)   # return a copy so outside code can't modify it

    @property
    def average(self):
        return float(np.mean(list(self.__marks.values())))

    @property
    def grade(self):
        avg = self.average
        if avg >= 85: return "A"
        if avg >= 75: return "B"
        if avg >= 65: return "C"
        if avg >= 50: return "D"
        return "F"

    # ---- method overriding ----
    def describe(self):
        return f"[Roll {self.roll_no}] {super().describe()} | Avg: {self.average:.2f} | Grade: {self.grade}"

    def __str__(self):
        return self.describe()


class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self, student):
        if student.roll_no in self.students:
            raise ValidationError(f"Roll number {student.roll_no} already exists.")
        self.students[student.roll_no] = student

    def get_student(self, roll_no):
        if roll_no not in self.students:
            raise KeyError(f"No student with roll number {roll_no}.")
        return self.students[roll_no]

    def remove_student(self, roll_no):
        self.get_student(roll_no)
        del self.students[roll_no]

    def update_marks(self, roll_no, marks):
        self.get_student(roll_no).set_marks(marks)

    def rankings(self):
        return sorted(self.students.values(), key=lambda s: s.average, reverse=True)

    def statistics(self):
        if not self.students:
            raise ValidationError("No students available.")
        avgs = np.array([s.average for s in self.students.values()])
        return {
            "count": len(avgs),
            "mean": float(np.mean(avgs)),
            "median": float(np.median(avgs)),
            "std_dev": float(np.std(avgs)),
            "highest": float(np.max(avgs)),
            "lowest": float(np.min(avgs)),
        }

    def export_csv(self, filename="student_report.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank", "Roll No", "Name", "Age", *Student.SUBJECTS, "Average", "Grade"])
            for rank, s in enumerate(self.rankings(), start=1):
                m = s.get_marks()
                writer.writerow([rank, s.roll_no, s.name, s.age,
                                 *[m[x] for x in Student.SUBJECTS],
                                 round(s.average, 2), s.grade])
        return filename


# ------------------------- console menu -------------------------
def read_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        raise ValidationError("Please enter a valid whole number.")


def read_marks():
    marks = []
    for subject in Student.SUBJECTS:
        try:
            marks.append(float(input(f"  {subject} marks (0-100): ")))
        except ValueError:
            raise ValidationError("Marks must be numeric.")
    return marks


def main():
    manager = StudentManager()
    menu = """
=== Student Management System ===
1. Add student      2. View all       3. Search by roll no
4. Update marks     5. Delete student 6. Rankings
7. Class statistics 8. Export CSV     0. Exit"""
    while True:
        print(menu)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                roll = read_int("Roll no: ")
                name = input("Name: ")
                age = read_int("Age: ")
                manager.add_student(Student(roll, name, age, read_marks()))
                print("Student added.")
            elif choice == "2":
                for s in manager.students.values():
                    print(s)
                if not manager.students:
                    print("No students yet.")
            elif choice == "3":
                print(manager.get_student(read_int("Roll no: ")))
            elif choice == "4":
                roll = read_int("Roll no: ")
                manager.update_marks(roll, read_marks())
                print("Marks updated.")
            elif choice == "5":
                manager.remove_student(read_int("Roll no: "))
                print("Student deleted.")
            elif choice == "6":
                for i, s in enumerate(manager.rankings(), 1):
                    print(f"{i}. {s}")
            elif choice == "7":
                for k, v in manager.statistics().items():
                    print(f"{k:>8}: {v:.2f}" if k != "count" else f"{k:>8}: {v}")
            elif choice == "8":
                print("Saved to", manager.export_csv())
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except (ValidationError, KeyError) as e:
            print("Error:", e.args[0])


if __name__ == "__main__":
    main()
