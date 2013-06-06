import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

from custom_mod import Student, fetch_student, parse_grade_from_string

import cProfile

import json

import mechanize
from datetime import date
import csv

### globals
FINAL_DATA = {}
SKIPPED_FIRST = False
COLUMN_NAMES = []
GRADE = None

TESTING = False

## methods

def handle_row(row):

	global SKIPPED_FIRST
	global FINAL_DATA
	global COLUMN_NAMES
	global GRADE

	# skip first row (column titles)
	if not SKIPPED_FIRST:
		SKIPPED_FIRST = True
	else:
		cols = row.find_elements_by_tag_name("td")
		name = cols[0].text
		#check if student exists already
		# returns the student object if it exists, or None
		try:
			s = FINAL_DATA[name]
			for z in range(len(COLUMN_NAMES)):
				s.add_score(title=COLUMN_NAMES[z], score=cols[z].text)
		except KeyError:
			# declare new student
			s = Student(name=name, grade=GRADE)
			for z in range(len(COLUMN_NAMES)):
				s.add_score(title=COLUMN_NAMES[z], score=cols[z].text)

			FINAL_DATA[name] = s
			pass

def galileo_crawl():

	global SKIPPED_FIRST
	global FINAL_DATA
	global COLUMN_NAMES
	global GRADE

	### sign in
	driver= webdriver.Firefox()
	driver.get("https://www.assessmenttechnology.com/GalileoASP/ASPX/K12Login.aspx")

	emailid=driver.find_element_by_id("txtUsername")
	emailid.send_keys("mcosta@scstucson.org")


	passw=driver.find_element_by_id("txtPassword")
	passw.send_keys("galileo")

	signin=driver.find_element_by_id("btnLogin")
	signin.click()

	## go to dashboard

	python_link = driver.find_elements_by_xpath(".//a[@href='/GalileoASP/ASPX/Dashboard/AdminDashboard.aspx']")[0]
	python_link.click()

	### go to benchmarks
	python_link = driver.find_elements_by_xpath(".//a")
	benchmark_link = None
	for link in python_link:
		if link.text == "Benchmark Results":
			benchmark_link = link

	benchmark_link.click()

	#this opens a new window for some stupid reason
	dashboard_window = driver.window_handles[0]
	benchmark_window = driver.window_handles[1]

	driver.switch_to_window(benchmark_window)

	### iterate through classes, libraries and subjects to find all tests
	try:
		class_dropdown = driver.find_element_by_id("ClassPicker_cboClass")
		class_dropdown_options = class_dropdown.find_elements_by_tag_name("option")

		num_of_classes = len(class_dropdown_options)
		i = 0
	except NoSuchElementException:
		driver.quit()

	#while i < num_of_classes:
	while i < 2:
		### page refreshes after every select
		### so have to continuously reselct class_dropdown
		try : 
			class_dropdown = driver.find_element_by_id("ClassPicker_cboClass")
			class_dropdown_options = class_dropdown.find_elements_by_tag_name("option")
			option = class_dropdown_options[i]

			### find grade of the current class
			GRADE = parse_grade_from_string(option.text)

			### click (refreshes Page)
			i += 1
			option.click()

			### now iterate through each library for that class
			library_dropdown = driver.find_element_by_id("cboLibraries")
			library_dropdown_options = library_dropdown.find_elements_by_tag_name("option")

			num_of_libs = len(library_dropdown_options)
			j = 0

			while j < num_of_libs and num_of_libs != 0:
				try: 
					library_dropdown = driver.find_element_by_id("cboLibraries")
					library_dropdown_options = library_dropdown.find_elements_by_tag_name("option")
					option = library_dropdown_options[j]

					skip = False
					## list of words to skip
					skip_words = ["reading", "writing", "Reading", "Writing", "Science", "science", "Select", "select"]
					for word in skip_words:
						if word in option.text:
							j += 1
							skip = True

					if not skip:
						j += 1
						option.click()

						### now iterate through each subject for that library
						subject_dropdown = driver.find_element_by_id("ddlSubjects")
						subject_dropdown_options = subject_dropdown.find_elements_by_tag_name("option")

						num_of_subjects = len(subject_dropdown_options)
						k = 0

						while k < num_of_subjects and num_of_subjects != 0:
							try: 
								subject_dropdown = driver.find_element_by_id("ddlSubjects")
								subject_dropdown_options = subject_dropdown.find_elements_by_tag_name("option")
								option = subject_dropdown_options[k]

								## check if GRADE is set
								if GRADE == None:
									GRADE = parse_grade_from_string(option.text)

								skip_words = ["Science", "science", "Biology", "biology", "Chemistry", "chemistry", "Physics", "physics", "Select", "select"]
								skip = False
								for word in skip_words:
									if word in option.text:
										k += 1
										skip = True

								if not skip:
									k += 1
									option.click()

									### now we have to scrape student data
									try:
										result_table = driver.find_element_by_id("tableResults")
										result_table_rows = result_table.find_elements_by_tag_name("tr")
										### use first row to deduce data structure
										row = result_table_rows[0]
										cols = row.find_elements_by_tag_name("td")

										### if only two cols, then no data
										if len(cols) > 2:
											COLUMN_NAMES = []
											for col in cols:
												COLUMN_NAMES.append(col.text)

											# map compiles to C for performance
											# or so i've been told
											map(handle_row, result_table_rows)
											## reset skipped first
											SKIPPED_FIRST = False


									except NoSuchElementException:
										continue


							except NoSuchElementException:
								continue
							except IndexError:
								continue

				except NoSuchElementException:
					continue
				except IndexError:
					continue

		except NoSuchElementException:
			### try again, sometimes the page doesn't seem to finish loading or something
			### aka the driver.title shows up blank and it can't find elements
			continue
		except IndexError:
			continue

	driver.quit()

def dibels_crawl():
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

	br.select_form("login")

	br["name"] = DIBELS_USER
	br["password"] = DIBELS_PW

	response = br.submit()

	### get last year
	d = date.today()
	year = d.year - 1 

	br.open("https://dibels.uoregon.edu/reports/report.php?report=DataFarming&Scope=School&district=572&School=3271&Grade=_ALL_&StartYear=%s&EndYear=%s&Assessment=10000&AssessmentPeriod=_ALL_&StudentFilter=none&Fields[]=&Fields[]=1&Fields[]=2&Fields[]=22&Fields[]=25&Fields[]=41&Delimiter=0" % (year, year))

	response = br.response()
	download_link = br.links(text_regex="Download Full Dataset")

	csv_file = br.retrieve(download_link.next().absolute_url)[0]

	with open(csv_file, 'rb') as csvfile:
	    for row in csv.DictReader(csvfile):
	    	grade = determine_grade(row)
	    	name = row["Last"] + ", " + row["First"]

	    	try:
	    		### try to udpate existing student object 
	    		s = FINAL_DATA[name]
	    		for key in row.keys():
	    			if key != "First" and key != "Last":
	    				s.add_score(title=key, score=row[key])
	    	except KeyError:
	    		## student does not exist, create new student object
	    		s = Student(name=name, grade=grade)
	    		for key in row.keys():
	    			if key != "First" and key != "Last":
	    				s.add_score(title=key, score=row[key])
	    		FINAL_DATA[name] = s
	    		pass 		


def crawl():
	galileo_crawl()
	dibels_crawl()

	count = 0
	score_count = 0
	for name in FINAL_DATA.keys():
		count += 1
		print ""
		print ""
		print FINAL_DATA[name].grade, name
		for key in FINAL_DATA[name].scores.keys():
			score_count += 1
			print key + " = " + FINAL_DATA[name].scores[key]

	print "There were %d students." % count
	print "There were %d scores." % score_count


if __name__ == "__main__":
	crawl()



