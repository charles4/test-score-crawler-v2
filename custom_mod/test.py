import unittest
from custom import *

class TestSequence(unittest.TestCase):

	def setUp(self):
		self.students = []
		self.students.append(Student("Bob"))
		self.students.append(Student("Mary"))
		self.students.append(Student("Jesus"))
		self.students.append(Student("Rachel"))
		self.students.append(Student("Jose"))
		self.students.append(Student("Michael"))
		self.students.append(Student("Randy"))

	def test_does_student_exist(self):

		result = fetch_student(self.students, "Bob", None)
		self.assertTrue(result != None)
		self.assertTrue(result.name == "Bob")

		result = fetch_student(self.students, "Michael", None)
		self.assertTrue(result != None)
		self.assertTrue(result.name == "Michael")

	def test_Student_add_score(self):
		self.students[0].add_score("AIMS", 33)

		self.assertTrue(self.students[0].scores["AIMS"] == 33)

	def test_parse_grade_from_string(self):
		grade_string = "Homeroom 4: edmunson"
		grade = parse_grade_from_string(grade_string)
		self.assertEqual(grade, 4)

		grade_string = "Art: Phillips: 6th"
		grade = parse_grade_from_string(grade_string)
		self.assertEqual(grade, 6)	

		grade_string = "World History: Maes: A"
		grade = parse_grade_from_string(grade_string)
		self.assertEqual(grade, None)

		grade_string = "AZ: GR06 AIMS MATH"
		grade = parse_grade_from_string(grade_string)
		self.assertEqual(grade, 6)



if __name__ == "__main__":
	unittest.main()