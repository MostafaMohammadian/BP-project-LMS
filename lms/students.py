import re

class Student:
    def __init__(self, id, name, email, password, phone, enrolled_courses = None, remember_me=False):
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address.")
        
        if not self.is_valid_phone(phone):
            raise ValueError("Invalid phone number.")
        
        if not self.is_valid_id(id):
            raise ValueError("Invalid ID. Student ID must be exactly 9 digits.")
        
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.enrolled_courses = enrolled_courses if enrolled_courses is not None else {}
        self.remember_me = remember_me
        
    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))
    
    def is_valid_phone(self, phone):
        phone_regex = r'^\+98\d{10}$|^09\d{9}$'
        return bool(re.match(phone_regex, phone))

    def is_valid_id(self, student_id):
        return isinstance(student_id, int) and len(str(student_id)) == 9
    
    def enroll(self, course_id):
        self.enrolled_courses[course_id] = {}
        #print(f"Enrolled in course {course_id}")
    
    def view_grades(self, course):
        if course.id in self.enrolled_courses:
            student_grades = course.enrolled_students[self.id]
            print(f"Student {self.id} grades are {student_grades}")
        else:
            print(f"{self.id} is not enrolled in the course {course.id}.")
            return None
    
   
