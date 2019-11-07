#!/usr/bin/env python
# coding: utf-8

# In[90]:


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


# In[91]:


driver = webdriver.Chrome('chromedriver.exe')

driver.get("http://www.tripadvisor.it")
driver.maximize_window()
hotels = driver.find_element_by_xpath("//div[@id='component_4']/div//span[1]/div") #hotels
actions = ActionChains(driver)
actions.click(hotels) 
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()

url = driver.current_url
print (url)


# In[92]:


calendnext = driver.find_element_by_xpath("//button[contains(@class, 'calendar__next')]").click()
dec1 = driver.find_element_by_xpath("//div[contains(@class, 'calendar__month-')][1]//div[contains(@class, 'calendar__week-')][1]/div[1]").click()
time.sleep(1)
dec2 = driver.find_element_by_xpath("//div[contains(@class, 'calendar__month-')][1]//div[contains(@class, 'calendar__week-')][1]/div[2]").click()
time.sleep(1)
ad1 = driver.find_element_by_xpath("//div[contains(@class, 'guest-wrapper__picker')][2]//button[contains(@class, 'number-ticker__control')][1]").click()
time.sleep(1)
aggiorna = driver.find_element_by_xpath("//button[text()='Aggiorna']").click()
time.sleep(5)


# In[ ]:


def listnames():
    hotelnames = driver.find_elements_by_xpath("//*[@class='listing_title']") #nomi hotel
    for i in range(0,(len(hotelnames))):
        print((hotelnames[i].text))

def listprices():
    hotelprice = driver.find_elements_by_xpath("//*[@class='price-wrap ']") #prezzi
    for i in range(0,(len(hotelprice))):
        if (hotelprice[i] not in hotelprice):
            print('0')
        else:
            print((hotelprice[i].text))
        


def cambiopag():
    num_pages = driver.find_elements_by_xpath("//div[@class='pageNumbers']/a")
    last = len(num_pages)-1
    count = int(num_pages[last].get_attribute("data-page-number"))
    for i in range(0,(count-1)):
        page = driver.find_element_by_xpath("//a[@class='nav next taLnk ui_button primary']")
        listnames()
        listprices()
        page.click()
        time.sleep(4)

cambiopag()


# In[ ]:





# In[ ]:




