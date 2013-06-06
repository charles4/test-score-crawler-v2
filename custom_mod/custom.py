import re

### classes

class Student(object):

	def __init__(self, name, grade=None):
		self.name = name
		self.scores = {}
		self.grade = grade

	def add_score(self, title, score):
		if title not in self.scores:
			self.scores[title] = score

	def __repr__(self):
		return "<Student %s>" % self.name




### methods

def fetch_student(array_of_student_objects, student_name, grade):

	for s in array_of_student_objects:
		if s.name == student_name and s.grade == grade:
			return s
	
	return None

def parse_grade_from_string(_string):
	grades = [ int(s) for s in re.findall(r'\d+', _string)]

	if "Algebra" in _string:
		return 9
	if len(grades) == 0 :
		return None
	else:
		return grades[0]



