import matplotlib.pyplot as plt
from .courses import Course
from .students import Student
import json
import re

class Professor:
    def __init__(self, id, name, email, password, phone, lms, courses = None, remember_me=False):
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
        if courses is None:
            courses = {}  # Ensure it's always a dictionary
        self.courses = courses
        self.remember_me = remember_me  # Default is False
    
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
            if isinstance(obj, Student):
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "email": obj.email,
                    "password": obj.password,
                    "phone": obj.phone,
                    "enrolled_courses": {course_id: course for course_id, course in obj.enrolled_courses.items()}
                }
            elif isinstance(obj, Course):
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "instructor_id": obj.instructor_id,
                    "capacity": obj.capacity,
                    "schedule": obj.schedule,
                    "description": obj.description,
                    "enrolled_students": {
                        student_id: {category: grade for category, grade in grades.items()}
                        for student_id, grades in obj.enrolled_students.items()
                    }, # Store as dict
                    "grading_scheme": obj.grading_scheme,
                    "students_ids": obj.students_ids
                }
            elif isinstance(obj, Professor):
                return {
                    "id": obj.id,
                    "name": obj.name,
                    "email": obj.email,
                    "password": obj.password,
                    "phone": obj.phone,
                    "courses": list(obj.courses.keys()),  # Store course IDs as list
                    "remember_me": obj.remember_me
                }
            return str(obj)

        data = {
            "students": {id: serialize(student) for id, student in self.lms.students.items()},
            "professors": {id: serialize(professor) for id, professor in self.lms.professors.items()},
            "courses": {id: serialize(course) for id, course in self.lms.courses.items()}
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Data saved successfully by Professor {self.name}.")
   
    @classmethod
    def load_data(cls, lms, filename="lms_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            # Load students
            lms.students = {int(id): Student(**info) for id, info in data["students"].items()}
            
            # Load courses
            lms.courses = {}
            for id, info in data["courses"].items():
                # Create course without the instructor first
                course = Course(**info)

                # Assign the instructor manually after the course is created
                instructor_id = int(info["instructor_id"])  # ensure integer conversion for matching
                course.instructor = lms.professors.get(instructor_id, None)  # Add instructor object reference

                # Ensure enrolled_students are initialized with grades properly
                course.enrolled_students = {
                    int(student_id): grades  # Convert student_id to int
                    for student_id, grades in info["enrolled_students"].items()
                }

                lms.courses[int(id)] = course

            # Load professors and assign courses correctly
            lms.professors = {}
            for id, info in data["professors"].items():
                professor = Professor(**info, lms=lms)

                # Restore courses as a dictionary (from list of IDs)
                professor.courses = {
                    course_id: lms.courses[course_id]
                    for course_id in info.get("courses", [])
                    if course_id in lms.courses
                }

                lms.professors[int(id)] = professor

            # Check for a remembered professor
            for professor in lms.professors.values():
                if professor.remember_me:
                    return professor  # Auto-login the remembered professor

            return None  # No remembered professor found

        except FileNotFoundError:
            print("No previous data found.")
            return None

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

        for student_id, grades in course.enrolled_students.items():
            final_score = sum(grades.get(category, 0) * (weight / 20) for category, weight in course.grading_scheme.items())
            course.enrolled_students[student_id]["Final Score"] = final_score  

        print(f"Grading scheme set successfully for course {course.name}")

    def assign_grade(self, course_id, student_id, category, grade):
        if course_id not in self.courses:
            print(f"{self.name} is not the professor of this course.")
            return
        course = self.courses[course_id]

        if not course.grading_scheme:
            print(f"Error: Grading scheme has not been set for {course.name}. Cannot assign grades.")
            return

        if student_id in course.enrolled_students:
            course.enrolled_students[student_id][category] = grade
            print(f"Grade for {category} updated to {grade} for student {student_id}.")
            
            # Calculate final score based on grading scheme
            final_score = sum(
                course.enrolled_students[student_id].get(cat, 0) * (weight / 20)
                for cat, weight in course.grading_scheme.items()
            )
            course.enrolled_students[student_id]["Final Score"] = final_score
            print(f"Updated Final Score for Student {student_id}: {final_score}")
        else:
            print("Invalid student ID or category.")

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
        print(df)
        print(f"Current average grade: {avg_grade}")

        if avg_grade < 16:
            shift = 16 - avg_grade
            df["Final Score After Shift"] = df["Final Score"] + shift
            df["Final Score After Shift"] = df["Final Score After Shift"].apply(lambda x: min(20, max(0, x)))

            for student_id in df.index:
                course.enrolled_students[student_id]["Final Score After Shift"] = df.loc[student_id, "Final Score After Shift"]

            print("Grades adjusted to maintain an average of 16.")
            avg_grade = df["Final Score After Shift"].mean()
            print(df)
            print(f"New adjusted average grade: {avg_grade}")
            

        else:
            print("No adjustment needed, average is already 16 or higher.")

