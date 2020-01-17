#!/usr/bin/env python
# coding: utf-8

# In[42]:


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


# In[43]:


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


# In[46]:


#connessione al db
try:
        
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="ota"
            )
    cursor = connection.cursor()

    #creazione tabella strutture
    cursor.execute("CREATE TABLE structures (IDhotel int(11) AUTO_INCREMENT PRIMARY KEY, NomeHotel VARCHAR(64), url VARCHAR(256)) ")

    num_pages = driver.find_elements_by_xpath("//div[@class='pageNumbers']/a")
    last = len(num_pages)-1
    count = int(num_pages[last].get_attribute("data-page-number"))

    for i in range(count):
        insert_table = "INSERT INTO structures (NomeHotel, url) VALUES (%s, %s)"
        if i < (count-1):
            time_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='nav next ui_button primary']")))
            page = driver.find_element_by_xpath("//a[@class='nav next ui_button primary']")
            hotelnames = driver.find_elements_by_xpath("//div[@class='listing_title']") #nomi hotel
            links = driver.find_elements_by_xpath("//div[@class='listing_title']/a")
            for i in range(len(hotelnames)):
                on_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='listing_title']")))
                name_one = hotelnames[i].text
                link_one = driver.find_element_by_link_text(hotelnames[i].text).get_attribute("href") #url
                records_to_insert = [(name_one, link_one)]
                cursor.executemany(insert_table, records_to_insert)
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully into structures table")
            page.click()
            time.sleep(8)
        else:
            hotelnames = driver.find_elements_by_xpath("//div[@class='listing_title']") #nomi hotel
            links = driver.find_elements_by_xpath("//div[@class='listing_title']/a")
            for i in range(len(hotelnames)):
                on_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='listing_title']")))
                name_one = hotelnames[i].text
                link_one = driver.find_element_by_link_text(hotelnames[i].text).get_attribute("href") #url
                records_to_insert = [(name_one, link_one)]
                cursor.executemany(insert_table, records_to_insert)
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully into structures table")
            time.sleep(8)


        

    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


# In[ ]:





# In[ ]:




