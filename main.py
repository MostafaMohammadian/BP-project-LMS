from lms.lms import LMS, Professor

def main():
    # Step 1: Initialize LMS System
    lms = LMS()

    print(lms.professors)
    print(lms.students)
    print(lms.courses)
    
    # Step 2: Register professors and students
    lms.register_professor(1234, "Dr. Smith", "dr.smith@email.com", "prof123", "+987654321011", remember_me= True)
    lms.register_professor(5678, "Dr. Johnson", "dr.johnson@email.com", "prof456", "+987654321111")

    print(type(lms.professors[1234].courses))
 
    lms.register_student(123456789,  "John Doe", "john.doe@email.com", "student123", "+987654301111")
    lms.register_student(987654321, "Jane Smith", "jane.smith@email.com", "student456", "+987654321011")

    print("Professor courses type:", type(lms.courses))
    # Step 3: Create courses (automatically assigns to professors)
    lms.create_course(101, "Intro to Python", 1234, 30, "MWF 10:00-11:00", "An introductory course on Python programming.")
    lms.create_course(102, "Data Structures", 5678, 30, "TTh 2:00-3:30", "Learn about data structures like lists, stacks, queues, and trees.")

    # Step 4: Enroll students in courses
    lms.enroll_student_in_course(123456789, 101)  # Enroll John Doe in "Intro to Python"
    lms.enroll_student_in_course(987654321, 101)  # Enroll Jane Smith in "Intro to Python"
    lms.enroll_student_in_course(987654321, 102)  # Enroll Jane Smith in "Data Structures"

    # Step 5: Assign grades
    professor_1 = lms.professors[1234]  # Dr. Smith
    professor_2 = lms.professors[5678]  # Dr. Johnson
    course_1 = lms.courses[101]
    course_2 = lms.courses[102]
    course_1.display_course_info()
    student_1 = lms.students[123456789]
    

    # Set grading scheme
    grading_scheme = {"Quiz 1": 5, "Midterm": 5, "Quiz 2": 5, "Final": 5}
    professor_1.set_course_grading_scheme(101, grading_scheme)

    # Assign grades for "Intro to Python"
    professor_1.assign_grade(101, 123456789, "Quiz 1", 10)
    professor_1.assign_grade(101, 123456789, "Midterm", 10)
    professor_1.assign_grade(101, 123456789, "Quiz 2", 18)
    professor_1.assign_grade(101, 123456789, "Final", 14)
    professor_1.assign_grade(101, 123456789, "Assignments", 14)
    professor_1.assign_grade(101, 987654321, "Quiz 1", 10)
    professor_1.assign_grade(101, 987654321, "Midterm", 10)
    professor_1.assign_grade(101, 987654321, "Quiz 2", 17)
    professor_1.assign_grade(101, 987654321, "Final", 19)
    professor_1.assign_grade(101, 987654321, "Assignments", 17)

    student_1.view_grades(course_1)

    # Assign grades for "Data Structures"
    professor_2.assign_grade(102, 987654321, "Quiz 1", 16)
    professor_2.assign_grade(102, 987654321, "Midterm", 12)

    # Step 6: View a student's grades over time using a plot
    professor_1.plot_student_grades(123456789, course_1)  # John Doe in "Intro to Python"
    professor_1.plot_student_grades(987654321, course_1)  # Jane Smith in "Intro to Python"
    professor_2.plot_student_grades(987654321, course_2)

    # Step 7: Adjust grades to maintain an average of 16
    professor_1.view_and_adjust_average(101)

    # Step 8: Export class list to CSV
    professor_1.export_class_list(101, "csv")

    # Step 9: Display course and student enrollment details
    for course in lms.courses.values():
        print(f"Course: {course.name}")
        print(f"Description: {course.description}")
        print(f"Instructor: {lms.professors[course.instructor_id].name}")
        print(f"Enrolled Students: {list(course.enrolled_students.keys())}\n")

    # Step 10: Save data to file
    professor_1.save_data("lms_data.json")
    print("System data saved successfully.")

    # Step 2: Load Data and Auto-login if a professor has selected "Remember Me"
    remembered_professor = Professor.load_data(lms, "lms_data.json")

    if remembered_professor:
        print(f"Auto-logged in as {remembered_professor.name} ({remembered_professor.email})")
    else:
        print("No remembered professor found. Please log in manually.")
        
        # Manual login process
        email = input("Enter Professor Email: ")
        password = input("Enter Password: ")

        for professor in lms.professors.values():
            if professor.email == email and professor.password == password:
                print(f"Welcome, {professor.name}!")
                remember_me_choice = input("Remember Me? (yes/no): ").strip().lower() == "yes"
                professor.remember_me = remember_me_choice  # Set Remember Me
                remembered_professor = professor
                professor.save_data("lms_data.json")  # Save updated Remember Me status
                break
        else:
            print("Invalid credentials. Exiting...")
            return

    # Use the logged-in professor for course management
    professor_1 = remembered_professor
    print(professor_1.name)
    print(type(professor_1.courses))  # Should be dict
    print(professor_1.courses)        # Should be {101: <Course object>}

    professor_1.plot_student_grades(123456789, course_1)
    print(f"Student 123456789 exists in the system: {123456789 in lms.students}")
    print(f"Course 101 exists in the system: {101 in lms.courses}")
    professor_1.assign_grade(102, 987654321, "Quiz 1", 16)
    professor_1.assign_grade(101, 123456789, "Quiz 1", 20)
    professor_1.export_class_list(101, "csv")

if __name__ == "__main__":
    main()
