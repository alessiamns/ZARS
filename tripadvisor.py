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

def listnames():
    hotelnames = driver.find_elements_by_xpath("//*[@class='listing_title']") #nomi hotel
    for i in range(0,(len(hotelnames))):
        print((hotelnames[i].text))

def listprices():
    hotelprice = driver.find_elements_by_xpath("//*[@class='price-wrap ']") #prezzi
    for i in range(0,(len(hotelprice))):
        print((hotelprice[i].text))


def cambiopag():
    num_pages = driver.find_elements_by_xpath("//div[@class='pageNumbers']/a")
    last = len(num_pages)-1
    count = int(num_pages[last].get_attribute("data-page-number"))
    page = driver.find_element_by_xpath("//a[@class='nav next taLnk ui_button primary']")
    for i in range(0,(count-1)):
        listnames()
        listprices()
        actions.click(page).perform()
        time.sleep(4)

cambiopag()

