#!/usr/bin/env python
# coding: utf-8

# In[103]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import re
import requests
import urllib.request
import urllib.parse
import mysql.connector
from mysql.connector import Error


# In[104]:


driver = webdriver.Chrome('chromedriver.exe')
chrome_options = Options()
driver.get("http://www.tripadvisor.it")
hotels = driver.find_element_by_xpath("//a[@href= '/Hotels']")

actions = ActionChains(driver)
actions.click(hotels) 
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()

url = driver.current_url
print (url)


# In[106]:


def openpage():
    window_before = driver.window_handles[0]
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']")
    for i in range(0,(len(urls))):
        urls[i].click() #aprire le pagine di ogni struttura           
        #for handle in driver.window_handles:
            #driver.switch_to.window(handle)
        window_after = driver.window_handles[i+1]
        driver.switch_to.window(window_after)
        number = driver.find_element_by_xpath("//b[@class='rank']").text
        indirizzo = driver.find_element_by_xpath("//div[@class='hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7']/div[1]").text
        print(number)
        print(indirizzo)
        driver.switch_to.window(window_before)

openpage()


# In[ ]:





# In[ ]:





# In[ ]:




