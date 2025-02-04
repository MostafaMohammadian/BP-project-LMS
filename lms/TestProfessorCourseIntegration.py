import unittest
from unittest.mock import patch
from lms.courses import Course
from lms.students import Student
from lms.professors import Professor
from lms.lms import LMS 


class TestProfessorCourseIntegration(unittest.TestCase):
    def setUp(self):
        self.lms = LMS()
        self.professor = Professor(
            id=1001, 
            name="Prof. John", 
            email="prof.john@example.com", 
            password="password123", 
            phone="+989123456789", 
            lms=self.lms
        )
        
        self.course = Course(
            id=101,
            name="Introduction to Python",
            instructor_id=self.professor.id,
            capacity=2,
            schedule="Mon-Wed 10:00 - 12:00",
            description="Learn the basics of Python programming."
        )
        
        self.professor.add_course(self.course)  # Assign the course to the professor
        
        self.student1 = Student(123456789, "Alice", "alice@example.com", "password", "+989123456989")
        self.student2 = Student(987654321, "Bob", "bob@example.com", "password", "+989123456977")
        
        # Enroll students in the course
        self.course.enroll_student(123456789)
        self.course.enroll_student(987654321)
        
        self.course.grading_scheme = {
            "Quiz 1": 2.5,
            "Midterm": 5,
            "Quiz 2": 2.5,
            "Final": 10
        }

    def test_course_creation_and_enrollment(self):
        self.assertIn(self.course.id, self.professor.courses)

        self.assertIn(123456789, self.course.enrolled_students)
        self.assertIn(123456789, self.course.enrolled_students)
        
    def test_assign_grades_to_students(self):
        self.professor.assign_grade(101, 123456789, "Quiz 1", 18)
        self.professor.assign_grade(101, 123456789, "Midterm", 17)
        self.professor.assign_grade(101, 987654321, "Quiz 1", 15)
        self.professor.assign_grade(101, 987654321, "Midterm", 14)
        
        self.assertEqual(self.course.enrolled_students[123456789]["Quiz 1"], 18)
        self.assertEqual(self.course.enrolled_students[123456789]["Midterm"], 17)
        self.assertEqual(self.course.enrolled_students[987654321]["Quiz 1"], 15)
        self.assertEqual(self.course.enrolled_students[987654321]["Midterm"], 14)
        
    def test_adjust_grades_if_average_is_below_16(self):
        self.professor.assign_grade(101, 123456789, "Quiz 1", 5)
        self.professor.assign_grade(101, 123456789, "Midterm", 6)
        self.professor.assign_grade(101, 987654321, "Quiz 1", 10)
        self.professor.assign_grade(101, 987654321, "Midterm", 8)
        
        df_before = self.course.generate_class_list()
        avg_before = df_before["Final Score"].mean()
        
        self.professor.view_and_adjust_average(101)
        
        df_after = self.course.generate_class_list()
        avg_after = df_after["Final Score After Shift"].mean()

        self.assertGreaterEqual(avg_after, 16)
        self.assertNotEqual(avg_before, avg_after)
        
    @patch("pandas.DataFrame.to_csv")
    def test_export_class_list_csv(self, mock_to_csv):
        """Test exporting class list to CSV"""
        self.professor.export_class_list(101, "csv")
        filename = "class_list_101.csv"
        mock_to_csv.assert_called_once_with(filename)

    @patch("pandas.DataFrame.to_excel")
    def test_export_class_list_xlsx(self, mock_to_excel):
        """Test exporting class list to Excel"""
        self.professor.export_class_list(101, "xlsx")
        filename = "class_list_101.xlsx"
        mock_to_excel.assert_called_once_with(filename)

if __name__ == '__main__':
    unittest.main()
