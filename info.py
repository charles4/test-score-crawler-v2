import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver= webdriver.Firefox()

print dir(driver)

driver.quit()