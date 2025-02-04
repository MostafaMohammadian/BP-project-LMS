import tkinter as tk
from tkinter import ttk

class StudentGUI:
    def __init__(self, student, lms):
        self.student = student
        self.lms = lms
        self.root = tk.Tk()
        self.root.title(f"Student {student.name} - Dashboard")
        self.root.geometry("500x300")

        # Label
        tk.Label(self.root, text=f"Welcome {student.name}", font=("Arial", 14)).pack(pady=10)

        # Table to show enrolled courses & grades
        columns = ["Course", "Quiz 1", "Midterm", "Quiz 2", "Final", "Assignments", "Final Score"]
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.load_grades()

        self.tree.pack(expand=True, fill="both")
        self.root.mainloop()

    def load_grades(self):
        for course_id in self.student.enrolled_courses:
            course = self.lms.courses.get(course_id)
            if course:
                grades = course.enrolled_students.get(self.student.id, {})
                self.tree.insert("", "end", values=[course.name] + [grades.get(col, 0) for col in self.tree["columns"][1:]])

# Example usage
# student = lms.students[123456789]  # Example student ID
# gui = StudentGUI(student, lms)
