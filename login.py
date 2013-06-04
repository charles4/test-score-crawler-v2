import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

### globals
FINAL_DATA = []

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

print benchmark_link.text

benchmark_link.click()

#this opens a new window for some stupid reason
dashboard_window = driver.window_handles[0]
benchmark_window = driver.window_handles[1]

driver.switch_to_window(benchmark_window)
print driver.title

### iterate through classes, libraries and subjects to find all tests
class_dropdown = driver.find_element_by_id("ClassPicker_cboClass")
class_dropdown_options = class_dropdown.find_elements_by_tag_name("option")

num_of_classes = len(class_dropdown_options)
i = 0

while i < num_of_classes:
	### page refreshes after every select
	### so have to continuously reselct class_dropdown
	print driver.title
	try : 
		class_dropdown = driver.find_element_by_id("ClassPicker_cboClass")
		class_dropdown_options = class_dropdown.find_elements_by_tag_name("option")
		option = class_dropdown_options[i]
		print option.text
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
				skip_words = ["reading", "writing", "Reading", "Writing", "Science", "science"]
				for word in skip_words:
					if word in option.text:
						print "Skipping %s." % option.text
						j += 1
						skip = True

				if not skip:
					print option.text
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
							k += 1
							print option.text
							option.click()

							### now we have to scrape student data
							try:
								result_table = driver.find_element_by_id("tableResults")
								result_table_rows = result_table.find_elements_by_tag_name("tr")
								### use first row to deduce data structure
								row = result_table_rows[0]
								cols = row.find_elements_by_tag_name("td")

								### if only two cols, then no data
								if len(cols) != 2:
									column_names = []
									for col in cols:
										column_names.append(col.text)

									skipped_first = False
									for row in result_table_rows:
										if not skipped_first:
											skipped_first = True
										else:
											_dict = {}
											cols = row.find_elements_by_tag_name("td")
											for z in range(len(column_names)):
												_dict[column_names[z]] = cols[z].text

											FINAL_DATA.append(_dict)

								else:
									print "There is no data in table."


							except NoSuchElementException:
								print "There doesn't seem to be a results table on this page."
								continue


						except NoSuchElementException:
							continue
						except IndexError:
							print "I hit an index error in subjects. Continuing. k is %d" % k
							continue

			except NoSuchElementException:
				continue
			except IndexError:
				print "I hit an index error in libraries. Continuing. j is %d" % j
				continue

	except NoSuchElementException:
		### try again, sometimes the page doesn't seem to finish loading or something
		### aka the driver.title shows up blank and it can't find elements
		continue
	except IndexError:
		print "I hit an index error in classes. Continuing."
		continue

### glob student data
ALL_STUDENTS = []
for row in FINAL_DATA:
	### row["Students"] is the name of the student
	if row["Students"] not in ALL_STUDENTS:
		ALL_STUDENTS.append(row["Students"])

print ALL_STUDENTS

driver.quit()




