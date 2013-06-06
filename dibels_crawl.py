import mechanize
from datetime import date
import csv
from custom_mod import Student, fetch_student, parse_grade_from_string

import json

### globals
FINAL_DATA = {}

#### CREDENTIALS

DIBELS_USER = "chavez4th"
DIBELS_PW = "dibels4th"


def printResponse(response):

	print response.geturl()
	print response.info()  # headers
	print response.read()  # body

def determine_grade(a_dictionary):
	ad = a_dictionary
	if ad["Year_K"] != "":
		return 0
	if ad["Year_1st"] != "":
		return 1
	if ad["Year_2nd"] != "":
		return 2
	if ad["Year_3rd"] != "":
		return 3
	if ad["Year_4th"] != "":
		return 4
	if ad["Year_5th"] != "":
		return 5
	if ad["Year_6th"] != "":
		return 6

#### open the browser
#### galileo login page

br = mechanize.Browser()
br.set_handle_robots( False )
br.open("https://dibels.uoregon.edu/")

response = br.response()
#printResponse(response)

br.select_form("login")

br["name"] = DIBELS_USER
br["password"] = DIBELS_PW

response = br.submit()

### get last year
d = date.today()
year = d.year - 1 

br.open("https://dibels.uoregon.edu/reports/report.php?report=DataFarming&Scope=School&district=572&School=3271&Grade=_ALL_&StartYear=%s&EndYear=%s&Assessment=10000&AssessmentPeriod=_ALL_&StudentFilter=none&Fields[]=&Fields[]=1&Fields[]=2&Delimiter=0" % (year, year))

response = br.response()
download_link = br.links(text_regex="Download Full Dataset")

csv_file = br.retrieve(download_link.next().absolute_url)[0]

print csv_file

with open(csv_file, 'rb') as csvfile:
    for row in csv.DictReader(csvfile):
    	try:
    		grade = determine_grade(row)
    		name = row["Last"] + ", " + row["First"]
    		s = Student(name=name, grade=grade)

    		for key in row.keys():
    			if key != "First" and key != "Last":
    				s.add_score(title=key, score=row[key])

    		FINAL_DATA[name] = s
    	except:
    		print "Someerror"
    		continue


print json.dumps(FINAL_DATA)

