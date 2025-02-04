import pandas as pd

class Course:
    def __init__(self, id, name, instructor_id, capacity, schedule, description="", enrolled_students=None, grading_scheme = None, students_ids = None):
        self.id = id
        self.name = name
        self.instructor_id = instructor_id
        self.capacity = capacity
        self.schedule = schedule
        self.description = description
        self.enrolled_students = enrolled_students if enrolled_students is not None else {}  # Ensure it's a dictionary
        self.grading_scheme = grading_scheme if grading_scheme is not None else {}
        self.students_ids = students_ids if students_ids is not None else []
    
    def enroll_student(self, student_id):
        if len(self.enrolled_students) < self.capacity:
            self.enrolled_students[student_id] = {"Quiz 1": 0, "Midterm": 0, "Quiz 2": 0, "Final": 0, "Assignments": 0, "Final Score": 0}
            self.students_ids.append(student_id)
            print(f"Student {student_id} enrolled in {self.name}.")
        else:
            print("Course is full")

    def generate_class_list(self):
        if not self.grading_scheme:
            print("Grading scheme not set. Cannot calculate final scores.")
            return None
        
        df = pd.DataFrame.from_dict(self.enrolled_students, orient='index')
        df.index.name = "Student ID"
        return df

    def display_course_info(self):
        print(f"Course ID: {self.id}")
        print(f"Course Name: {self.name}")
        print(f"Instructor ID: {self.instructor_id}")
        print(f"Schedule: {self.schedule}")
        print(f"Description: {self.description}")
        print(f"Enrolled Students: {len(self.enrolled_students)} / {self.capacity}")
        print(f"Students Enrolled (IDs): {self.students_ids}")
