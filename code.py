import datetime
import json
import os

class Student:
    def __init__(self, student_id, name, course):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.attendance = {}  # {date: present/absent}

    def mark_attendance(self, date, status):
        self.attendance[date.strftime("%Y-%m-%d")] = status

    def get_attendance(self):
        return self.attendance

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "course": self.course,
            "attendance": self.attendance,
        }

    @staticmethod
    def from_dict(data):
        student = Student(data["student_id"], data["name"], data["course"])
        student.attendance = data["attendance"]
        return student

class AttendanceManager:
    def __init__(self, filename="attendance.json"):
        self.students = {}
        self.filename = filename
        self.load_data()

    def add_student(self, student):
        if student.student_id not in self.students:
            self.students[student.student_id] = student
            self.save_data()
        else:
            print("Student ID already exists.")

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()
        else:
            print("Student ID not found.")

    def mark_attendance(self, student_id, date, status):
        if student_id in self.students:
            self.students[student_id].mark_attendance(date, status)
            self.save_data()
        else:
            print("Student ID not found.")

    def get_student_attendance(self, student_id):
        if student_id in self.students:
            return self.students[student_id].get_attendance()
        else:
            print("Student ID not found.")
            return None

    def get_all_students(self):
        return list(self.students.values())

    def save_data(self):
        data = [student.to_dict() for student in self.students.values()]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.students = {student["student_id"]: Student.from_dict(student) for student in data}
            except FileNotFoundError:
                pass #first time running.
            except json.JSONDecodeError:
                print("Error: Corrupted JSON file. Attendance data may be lost.")
                self.students = {} #reset to empty dict.

def main():
    manager = AttendanceManager()

    while True:
        print("\nStudent Attendance Management System")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Mark Attendance")
        print("4. View Student Attendance")
        print("5. View All Students")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            course = input("Enter Student Course: ")
            student = Student(student_id, name, course)
            manager.add_student(student)

        elif choice == "2":
            student_id = input("Enter Student ID to remove: ")
            manager.remove_student(student_id)

        elif choice == "3":
            student_id = input("Enter Student ID: ")
            date_str = input("Enter date (YYYY-MM-DD): ")
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue
            status = input("Enter attendance status (present/absent): ").lower()
            if status in ("present", "absent"):
                manager.mark_attendance(student_id, date, status)
            else:
                print("Invalid attendance status.")

        elif choice == "4":
            student_id = input("Enter Student ID to view attendance: ")
            attendance = manager.get_student_attendance(student_id)
            if attendance:
                print(attendance)

        elif choice == "5":
            students = manager.get_all_students()
            for student in students:
                print(f"ID: {student.student_id}, Name: {student.name}, Course: {student.course}")

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
