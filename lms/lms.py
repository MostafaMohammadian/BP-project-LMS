from .students import Student
from .professors import Professor
from .courses import Course

class LMS:
    def __init__(self):
        self.students = {}
        self.professors = {}
        self.courses = {}
    
    def register_student(self, student_id, name, email, password, phone, courses= None, remember_me=False):
        if student_id in self.students:
            print(f"Student id {student_id} already exists.")
            return
        self.students[student_id] = Student(student_id, name, email, password, phone, courses, remember_me)
        print(f"Student {student_id} registered successfully.")
    
    def register_professor(self, professor_id, name, email, password, phone, courses= None, remember_me=False):
        if professor_id in self.professors:
            print(f"Professor id {professor_id} already exists.")
            return
        self.professors[professor_id] = Professor(professor_id, name, email, password, phone, self, courses, remember_me)
        print(f"Professor {professor_id} registered successfully.")
    
    def create_course(self, course_id, name, instructor_id, capacity, schedule, description=""):
        if course_id in self.courses:
            print("Course ID already exists")
            return
        if instructor_id not in self.professors:
            print("Invalid professor ID")
            return
        # Create a new course and store the professor's ID instead of the professor object
        created_course = Course(course_id, name, instructor_id, capacity, schedule, description)
        self.courses[course_id] = created_course
        self.professors[instructor_id].add_course(created_course)
        print(f"Course {course_id} created successfully.")
 
    def enroll_student_in_course(self, student_id, course_id):
        if student_id not in self.students:
            print("Invalid student ID")
            return
        if course_id not in self.courses:
            print("Invalid course ID")
            return
        self.courses[course_id].enroll_student(student_id)
        self.students[student_id].enroll(course_id)
    
