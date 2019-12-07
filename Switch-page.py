#!/usr/bin/env python
# coding: utf-8

# In[209]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


# In[210]:


driver = webdriver.Chrome('chromedriver.exe')
wait = WebDriverWait(driver, 10)
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


# In[213]:


def openpage():
    window_before = driver.window_handles[0]    
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']")
    for i in range(0,(len(urls))):
        urls[i].click() #aprire le pagine di ogni struttura           
        #for handle in driver.window_handles:
            #driver.switch_to.window(handle)
        window_after = driver.window_handles[i+1]
        driver.switch_to.window(window_after)
        #number = driver.find_element_by_xpath("//b[@class='rank']").text
        name = driver.find_element_by_xpath("//h1[@id='HEADING']")
        address = driver.find_element_by_xpath("//div[@class='hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7']/div[1]").text
        #box = driver.find_elements_by_xpath("//div[@class='react-container' and @id='component_4']")
        #for i in range(len(box)):
            #telephone = driver.find_element_by_xpath("//div[@class='hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7']/div[2]").text
            #if telephone in box:
                #print(telephone)
            #else:
                #print('0')
        print(address)
        mostraplus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='hotels-hr-about-amenities-AmenityGroup__showMore--pPz2S']")))
        plus = driver.find_element_by_xpath("//div[@class='hotels-hr-about-amenities-AmenityGroup__showMore--pPz2S']")
        plus.click()
        services = driver.find_elements_by_xpath("//div[@class='hotels-hr-about-amenities-AmenitiesModal__group--3nudN']")
        for i in range(0,(len(services))):
            print(services[i].text)
            time.sleep(2)
        close_window = driver.find_element_by_xpath("//div[@class='_2EFRp_bb _3IWKziRc']").click()
        time.sleep(4)
        driver.switch_to.window(window_before)


openpage()


# In[212]:


window_before = driver.window_handles[0]
driver.switch_to.window(window_before)


# In[ ]:




