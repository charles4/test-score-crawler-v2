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
	if "Bechtold" in _string:
		return None
	if "KG" in _string:
		return 0 # kindergarden
	if len(grades) == 0 :
		return None
	else:
		return grades[0]

def read_user_info_file():
	user_info = {}
	f = open('user.info', 'r')
	for line in f.readlines():
		line = line.strip("\n")
		parts = line.split(" ")
		key = parts[0]
		value = parts[1]

		user_info[key] = value

	return user_info

