#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


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


# In[90]:


#connessione al db
try:
        
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="ota"
            )
    cursor = connection.cursor()

    #creazione tabella servizi
    cursor.execute("CREATE TABLE services (IDservice int(11) AUTO_INCREMENT PRIMARY KEY, Service VARCHAR(64)) ")

    window_before = driver.window_handles[0]    
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url
    for i in range(0,(len(urls))):
        
        urls[i].click() #aprire le pagine di ogni struttura           
        #for handle in driver.window_handles:
            #driver.switch_to.window(handle)
        window_after = driver.window_handles[i+1]
        driver.switch_to.window(window_after)
        #number = driver.find_element_by_xpath("//b[@class='rank']").text
        #name = driver.find_element_by_xpath("//h1[@id='HEADING']").text #nome
        #address = driver.find_element_by_xpath("//div[@class='hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7']/div[1]").text #indirizzo
        #box = driver.find_elements_by_xpath("//div[@class='react-container' and @id='component_4']")
        #for i in range(len(box)):
            #telephone = driver.find_element_by_xpath("//div[@class='hotels-hotel-review-atf-info-parts-BusinessListing__row--24M_7']/div[2]").text
            #if telephone in box:
                #print(telephone)
            #else:
                #print('0')
        #print(address)
        mostraplus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='hotels-hr-about-amenities-AmenityGroup__showMore--pPz2S']")))
        plus = driver.find_element_by_xpath("//div[@class='hotels-hr-about-amenities-AmenityGroup__showMore--pPz2S']")
        plus.click()
        services = driver.find_elements_by_xpath("//div[@class='hotels-hr-about-amenities-AmenitiesModal__group--3nudN']/div") #servizi+
        for i in range(0,(len(services))):
            time.sleep(2)
            s_hotel = services[i].text
            insert_table = "INSERT INTO services (Service) VALUES (%s)"
            records_to_insert = (s_hotel, )
            cursor.execute(insert_table, records_to_insert)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into services table")
        
        close_window = driver.find_element_by_xpath("//div[@class='_2EFRp_bb _3IWKziRc']").click()
        time.sleep(4)
        driver.switch_to.window(window_before)


except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


# In[89]:


window_before = driver.window_handles[0]
driver.switch_to.window(window_before)


# In[ ]:




