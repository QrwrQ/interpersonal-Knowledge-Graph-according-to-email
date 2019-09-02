from selenium import webdriver
from selenium.webdriver.support.select import Select

browser = webdriver.Chrome()

browser.get("http://192.168.1.171:2480/studio/index.html#/")
s=Select(browser.find_element_by_id("database-selection"))
s.select_by_value("string:person")
input_str1 = browser.find_element_by_id('user')
input_str1.send_keys("root")
input_str2 = browser.find_element_by_id('password')
input_str2.send_keys("123")
button = browser.find_element_by_id('database-connect')
button.click()
browser.get("http://192.168.1.171:2480/studio/index.html#/database/person/graph")
input_str3 = browser.find_element_by_class_name('cm-keyword')
#input_str3.click()
input_str3.send_keys("as")

