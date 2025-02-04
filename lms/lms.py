from .students import Student
from .professors import Professor
from .courses import Course

class LMS:
    def __init__(self):
        self.students = {}
        self.professors = {}
        self.courses = {}
    
    def register_student(self, id, name, email, password, phone):
        if id in self.students or len(str(id)) != 9:
            print("Invalid or duplicate student ID")
            return
        self.students[id] = Student(id, name, email, password, phone)
        print("Student registered successfully")
    
    def register_professor(self, professor_id, name, email, password, phone):
            """Registers a professor and links them to the LMS system."""
            if professor_id in self.professors:
                print("Professor already exists.")
                return
            self.professors[professor_id] = Professor(professor_id, name, email, password, phone, self)
    
    def create_course(self, id, name, instructor_id, capacity, schedule, description=""):
        if id in self.courses:
            print("Course ID already exists")
            return
        if instructor_id not in self.professors:
            print("Invalid professor ID")
            return
        # Create a new course and store the professor's ID instead of the professor object
        created_course = Course(id, name, instructor_id, capacity, schedule, description)
        self.courses[id] = created_course
        self.professors[instructor_id].add_course(created_course)
        print("Course created successfully")
 
    def enroll_student_in_course(self, student_id, course_id):
        if student_id not in self.students:
            print("Invalid student ID")
            return
        if course_id not in self.courses:
            print("Invalid course ID")
            return
        self.courses[course_id].enroll_student(student_id)
        self.students[student_id].enroll(course_id)
    
    def login(self, id, password):
        if id in self.students and self.students[id].password == password:
            print("Student logged in successfully")
        elif id in self.professors and self.professors[id].password == password:
            print("Professor logged in successfully")
        else:
            print("Invalid credentials")
