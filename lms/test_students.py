import unittest
from lms.students import Student

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(123456789, "Alice", "AliceInWonderLand@gmail.com", "Never Say Never", "+989123456789")

    def test_student_creation(self):
        self.assertEqual(self.student.name, "Alice")
        self.assertEqual(self.student.id, 123456789)
        self.assertEqual(self.student.email, "AliceInWonderLand@gmail.com")
        self.assertEqual(self.student.phone, "+989123456789")
        self.assertEqual(self.student.enrolled_courses, {})

    def test_enrollment(self):
        self.student.enroll(123456789)
        self.assertIn(123456789, self.student.enrolled_courses)

    def test_view_grades(self):
        self.student.enroll(123456789)
        grades = self.student.view_grades(123456789)
        self.assertIsInstance(grades, dict)
        self.assertEqual(grades, {})

if __name__ == '__main__':
    unittest.main()
