#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


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


# In[58]:


def listnames():
    hotelnames = driver.find_elements_by_xpath("//*[@class='listing_title']") #nomi hotel
    structuretype = driver.find_elements_by_xpath("//span[@class='label']")
    
    for i in range(0,(len(hotelnames))):
        links = driver.find_element_by_link_text(hotelnames[i].text).get_attribute('href')
        hotelnames[i].text #nome struttura
        
    for i in range(0,(len(structuretype))):
        structuretype[i].text  #tipologia di struttura
        
        
        
        try:
        
            connection = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="ota"
            )
            
            cursor = connection.cursor()


            strutture_sql_query = "INSERT INTO strutture (id,name, type, url) VALUES (%s, %s, %s, %s)"

            records_to_insert = [(i, hotelnames[i].text, structuretype[i].text , links)]

            cursor.executemany(strutture_sql_query, records_to_insert)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into provastrutture table")

        except mysql.connector.Error as error:
            print("Failed to insert record into MySQL table {}".format(error))

        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


# In[ ]:


def cambiopag():
    num_pages = driver.find_elements_by_xpath("//div[@class='pageNumbers']/a")
    last = len(num_pages)-1
    count = int(num_pages[last].get_attribute("data-page-number"))
    for i in range(count-1):
        page = driver.find_element_by_xpath("//a[@class='nav next taLnk ui_button primary']")
        listnames()
        page.click()
        time.sleep(12)
        
        
cambiopag()

