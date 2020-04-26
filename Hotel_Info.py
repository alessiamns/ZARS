#!/usr/bin/env python
# coding: utf-8

# In[76]:


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import re
import requests
import mysql.connector
from mysql.connector import Error


# In[77]:


options = Options()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

driver.get("http://www.tripadvisor.it")
driver.maximize_window()


# In[78]:


hotels = driver.find_element_by_xpath("//div[@class='FWWB-VUV']//a[@href= '/Hotels']")

hotels.click()

time.sleep(4)

input_name = driver.find_element_by_xpath("//input[@class='Smftgery']")
input_name.send_keys("noto")
time.sleep(3)
input_name.send_keys(Keys.RETURN)

time.sleep(2)
driver.find_element_by_xpath("//div[@class='h1-container']").click()


# In[88]:


def info():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text #nome hotel
    
    address = driver.find_element_by_xpath("//div[contains(@class, 'ListingEntry')]//span[contains(@class, 'ContactInfo')][2]").text
    
    rating_value = driver.find_element_by_xpath("//div[contains(@class, 'ratingContainer')]//span[contains(@class, 'ui_bubble')]")
    rating_class = rating_value.get_attribute("class")
    value_rating = rating_class[-2:]
    float_rating = value_rating[:1] + '.' + value_rating[1:]
    rating = float_rating

    review_count = driver.find_element_by_xpath("//div[contains(@class, 'ratingContainer')]//span[contains(@class, 'reviewCount')]").text

    popular_index = driver.find_element_by_xpath("//div[contains(@class, 'popIndex')]").text

    insert_table = "INSERT INTO info (Name, Address, Rating, Review_Count, Popular_Index) VALUES (%s, %s, %s, %s, %s)"
    records_to_insert = [(hotel_name, address, rating, review_count, popular_index)]
    cursor.executemany(insert_table, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "Record in Hotel_Info")


# In[89]:


#connessione al db
try:
        
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="ota"
            )
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE info (Name VARCHAR(64), Address VARCHAR(512), Rating VARCHAR(4), Review_Count VARCHAR(64), Popular_Index VARCHAR(64))") 
    
    
    homepage = driver.window_handles[0]  
    #view_urls = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-clicksource='HotelName']")))
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
    for i in range(0,(len(urls))):
        try:
            category = driver.find_element_by_xpath("//div[contains(@class, 'accommodation_category')]").text
            urls[i].click()
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            time.sleep(3)
            info()
            time.sleep(3)
            driver.close()
            driver.switch_to.window(homepage)
            time.sleep(5)
        except:
            urls[i].click()
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            time.sleep(3)
            info()
            time.sleep(3)
            driver.close()
            driver.switch_to.window(homepage)
            time.sleep(5)
            
        
    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


# In[87]:



window_before = driver.window_handles[0]
driver.switch_to.window(window_before)


# In[ ]:




