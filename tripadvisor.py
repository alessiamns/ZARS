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


hotels = driver.find_element_by_xpath("//*[@id='component_4']/div/div/div/span[1]/div/div/div/a") #hotels
actions = ActionChains(driver)
actions.click(hotels) 
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()

url = driver.current_url
print (url)



for i in range(0,400):

    hotelname = driver.find_elements_by_xpath("//*[@class='listing_title']") #nomi hotel
    #hotelprice = driver.find_elements_by_xpath("//*[@class='price-wrap ']") #prezzi

    listname = []
    #listprice = []

    for i in range(0,len(hotelname)):
        listname.append(hotelname[i].text)

    #for j in hotelprice:
    #    listprice.append(hotelprice[j].text)

    driver.find_element_by_xpath("//a[@class='nav next taLnk ui_button primary']").click()
    time.sleep(5)

    print(listname)


    







