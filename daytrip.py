import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import time
import re
import requests
import urllib.request
import urllib.parse

driver = webdriver.Chrome('chromedriver.exe')

driver.get("http://www.tripadvisor.it")

hotels = driver.find_element_by_xpath("//div[@id='component_4']/div//span[1]/div") #hotels
actions = ActionChains(driver)
actions.click(hotels) 
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()

url = driver.current_url
print (url)

calendnext = driver.find_element_by_xpath("//button[contains(@class, 'calendar__next')]").click()
#arrivo = driver.find_elements_by_xpath("//div[contains(@class, 'calendar__day')]")
dec1 = driver.find_element_by_xpath("//div[contains(@class, 'calendar__month-')][1]//div[contains(@class, 'calendar__week-')][1]/div[1]").click()
dec2 = driver.find_element_by_xpath("//div[contains(@class, 'calendar__month-')][1]//div[contains(@class, 'calendar__week-')][1]/div[2]").click()
ad1 = driver.find_element_by_xpath("//div[contains(@class, 'guest-wrapper__picker')][2]//button[contains(@class, 'number-ticker__control')][1]").click()
aggiorna = driver.find_element_by_xpath("//button(@class='ui_button primary fullwidth')")