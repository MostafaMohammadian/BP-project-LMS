import matplotlib.pyplot as plt
from .courses import Course
from .students import Student
import json
import re

class Professor:
    def __init__(self, id, name, email, password, phone, lms):
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address.")
        
        if not self.is_valid_phone(phone):
            raise ValueError("Invalid phone number.")
        
        if not self.is_valid_id(id):
            raise ValueError("Invalid ID. Professor ID must be exactly 4 digits.")
        
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.lms = lms  # Link to LMS instance
        self.courses = {}
    
    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))
    
    def is_valid_phone(self, phone):
        phone_regex = r'^\+98\d{10}$|^09\d{9}$'
        return bool(re.match(phone_regex, phone))
    
    @staticmethod
    def is_valid_id(professor_id):
        return isinstance(professor_id, int) and len(str(professor_id)) == 4
    
    def add_course(self, course):
        if course.instructor_id == self.id:
            self.courses[course.id] = course
        else:
            print(f"Cannot add course {course.id}. Instructor ID does not match professor ID.")

    def save_data(self, filename="lms_data.json"):
        def serialize(obj):
            """Helper function to convert objects to serializable dicts."""
            if isinstance(obj, Student):
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "email": obj.email,
                    "password": obj.password,
                    "phone": obj.phone,
                    "enrolled_courses": obj.enrolled_courses  # Already a dictionary
                }
            elif isinstance(obj, Course):
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "instructor_id": obj.instructor_id,  # Store only the ID
                    "capacity": obj.capacity,
                    "schedule": obj.schedule,
                    "description": obj.description,
                    "enrolled_students": obj.enrolled_students,  # Dictionary of student IDs and grades
                    "grading_scheme": obj.grading_scheme,  # Already a dictionary
                    "students_ids": obj.students_ids  # List of student IDs
                }
            elif isinstance(obj, Professor):
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "email": obj.email,
                    "password": obj.password,
                    "phone": obj.phone,
                    "courses": list(obj.courses.keys())  # Store only course IDs
                }
            return str(obj)  # Convert any other object types to string

        data = {
            "students": {id: serialize(student) for id, student in self.lms.students.items()},
            "professors": {id: serialize(professor) for id, professor in self.lms.professors.items()},
            "courses": {id: serialize(course) for id, course in self.lms.courses.items()}
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Data saved successfully by Professor {self.name}.")

    def load_data(self, filename="lms_data.json"):
        """Load LMS data from a JSON file (accessed through Professor)."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.lms.students = {id: Student(**info) for id, info in data["students"].items()}
            self.lms.professors = {id: Professor(**info, lms=self.lms) for id, info in data["professors"].items()}
            self.lms.courses = {id: Course(**info) for id, info in data["courses"].items()}
            print(f"Data loaded successfully by Professor {self.name}.")
        except FileNotFoundError:
            print("No previous data found.")   

    def plot_student_grades(self, student_id, course):
        if student_id not in course.enrolled_students:
            print("Student not enrolled in this course.")
            return
        
        student_grades = course.enrolled_students[student_id]
        
        categories = ["Quiz 1", "Midterm", "Quiz 2", "Final", "Assignments"]
        grades = [student_grades.get(category, 0) for category in categories]
        time_points = ["Quiz 1", "Midterm", "Quiz 2", "Final", "Assignments"]

        # Plotting the grades over time
        plt.figure(figsize=(10, 6))
        plt.plot(time_points, grades, marker='o', linestyle='-', color='b', label='Grades')
        plt.title(f"Student {student_id} Grades Over Time in Course: {course.name}")
        plt.xlabel("Assessment Type")
        plt.ylabel("Grade")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.show()

    def set_course_grading_scheme(self, course_id, scheme):
        if course_id not in self.courses:
            print("You are not the professor of this course.")
            return
        course = self.courses[course_id]
        if sum(scheme.values()) != 20:
            print("Invalid grading scheme. Total must be 20.")
            return
        course.grading_scheme = scheme

        for student_id, grades in self.enrolled_students.items():
            final_score = sum(grades.get(category, 0) * (weight / 20) for category, weight in self.grading_scheme.items())
            self.enrolled_students[student_id]["Final Score"] = final_score  

        print("Grading scheme set successfully")

    def assign_grade(self, course_id, student_id, category, grade):
        if course_id not in self.courses:
            print("You are not the professor of this course.")
            return
        course = self.courses[course_id]

        if not course.grading_scheme:
            print("Error: Grading scheme has not been set for this course. Cannot assign grades.")
            return

        if student_id in course.enrolled_students and category in course.enrolled_students[student_id]:
            # Update the grade for the specified category
            course.enrolled_students[student_id][category] = grade
            print(f"{category}", course.enrolled_students[student_id][category])
            print(f"Sutdent {student_id}'s, {category} grade updated successfully")

            # course.enrolled_students[student_id]["Final Score"] = self.calculate_final_score(course, student_id)
            # print(f"Final Score for Student {student_id} updated to: {course.enrolled_students[student_id]['Final Score']}")

        else:
            print("Invalid student ID or category")
    
    def calculate_final_score(self, course, student_id):
        final_score = 0
        for category, weight in course.grading_scheme.items():
            grade = course.enrolled_students[student_id].get(category, 0)  # Default to 0 if no grade is found
            final_score += grade * (weight / 20)
        return final_score

    def export_class_list(self, course_id, file_format="csv"):
        if course_id not in self.courses:
            print("You are not the professor of this course.")
            return
        course = self.courses[course_id]
        df = course.generate_class_list()
        if df is None:
            return
        filename = f"class_list_{course.id}.{file_format}"
        if file_format == "csv":
            df.to_csv(filename)
        elif file_format == "xlsx":
            df.to_excel(filename)
        else:
            print("Invalid file format")
            return
        print(f"Class list exported as {filename}")

    def view_and_adjust_average(self, course_id):
        if course_id not in self.courses:
            print("You are not the professor of this course.")
            return

        course = self.courses[course_id]
        df = course.generate_class_list()
        
        if df is None:
            return

        avg_grade = df["Final Score"].mean()
        print(f"Current average grade: {avg_grade}")

        if avg_grade < 16:
            shift = 16 - avg_grade
            df["Final Score"] = df["Final Score"] + shift
            df["Final Score"] = df["Final Score"].apply(lambda x: min(20, max(0, x)))

            for student_id in df.index:
                course.enrolled_students[student_id]["Final Score"] = df.loc[student_id, "Final Score"]

            print("Grades adjusted to maintain an average of 16.")
            avg_grade = df["Final Score"].mean()
            print(f"New average grade: {avg_grade}")

        else:
            print("No adjustment needed, average is already 16 or higher.")

