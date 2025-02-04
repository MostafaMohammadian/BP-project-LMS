import tkinter as tk
from tkinter import ttk, messagebox

class ProfessorGUI:
    def __init__(self, professor, lms):
        self.professor = professor
        self.lms = lms
        self.root = tk.Tk()
        self.root.title(f"Professor {professor.name} - Dashboard")
        self.root.geometry("600x400")

        # Dropdown to select a course
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(self.root, textvariable=self.course_var)
        self.course_dropdown["values"] = [course.name for course in professor.courses.values()]
        self.course_dropdown.pack(pady=10)

        # Button to view enrolled students
        self.view_students_button = tk.Button(self.root, text="View Students", command=self.view_students)
        self.view_students_button.pack(pady=10)

        self.root.mainloop()

    def view_students(self):
        selected_course = self.course_var.get()
        if not selected_course:
            messagebox.showwarning("Warning", "Select a course first!")
            return

        course = next(c for c in self.professor.courses.values() if c.name == selected_course)
        
        # Create a new window for students list
        student_window = tk.Toplevel(self.root)
        student_window.title(f"Students in {course.name}")
        student_window.geometry("500x300")

        # Table to show student grades
        columns = ["Student ID", "Quiz 1", "Midterm", "Quiz 2", "Final", "Assignments", "Final Score"]
        tree = ttk.Treeview(student_window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for student_id, grades in course.enrolled_students.items():
            tree.insert("", "end", values=[student_id] + [grades.get(col, 0) for col in columns[1:]])

        tree.pack(expand=True, fill="both")

# Example usage (you would get `professor` from LMS)
# prof = lms.professors[1234]  # Example professor ID
# gui = ProfessorGUI(prof, lms)
