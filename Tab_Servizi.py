#!/usr/bin/env python
# coding: utf-8

# In[82]:


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


# In[83]:


driver = webdriver.Chrome('chromedriver.exe')
wait = WebDriverWait(driver, 15)
chrome_options = Options()
driver.get("http://www.tripadvisor.it")



# In[84]:


hotels = driver.find_element_by_xpath("//a[@href= '/Hotels']")

actions = ActionChains(driver)
actions.click(hotels) 
time.sleep(4)
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()


# In[20]:


url = driver.current_url
print (url)


# In[123]:


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
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url
    window_before = driver.window_handles[0]  
    for i in range(0,(len(urls))):
        urls[i].click()
        window_after = driver.window_handles[i+1]
        driver.switch_to.window(window_after)
        time.sleep(3)
        mostra_servizi = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='hotels-hr-about-amenities-Amenity__amenity--3fbBj']")))
        servizi_active = driver.find_elements_by_xpath("//div[@class='hotels-hr-about-amenities-Amenity__amenity--3fbBj']")                                                 
        for j in range(0,(len(servizi_active))):
            one_service = servizi_active[j].text
            print(one_service)
       #così funziona ma il testo nascosto non compare
                                                        
        
        
    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


# In[169]:


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
    cursor.execute("CREATE TABLE services (IDservice int(11), Service VARCHAR(64)) ")
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url
    window_before = driver.window_handles[0]  
    for i in range(0,(len(urls))):
        urls[i].click()
        window_after = driver.window_handles[i+1]
        driver.switch_to.window(window_after)
        time.sleep(3)
        mostraplus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='hotels-hr-about-amenities-AmenityGroup__showMore--pPz2S']")))
        plus = driver.find_element_by_xpath("//div[@class='hotels-hr-about-amenities-AmenityGroup__showMore--pPz2S']")
        plus.click()
        active_services = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[@class='hotels-hr-about-amenities-Amenity__amenity--3fbBj']")
        for i in range(0,(len(active_services))):
            time.sleep(2)
            first_service = active_services[i].text
            insert_table = "INSERT INTO services (Service) VALUES (%s)"
            records_to_insert = (first_service, )
            cursor.execute(insert_table, records_to_insert)
            #soluzione per eliminare le stringhe vuote dalla tabella: effettuare una query
            cursor.execute("DELETE FROM services WHERE Service = ''")
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into services table")
            cursor.execute("DELETE FROM services WHERE Service = ''")
        #problema di gestione dei div che contengono il testo di ogni servizio
        #ActiveGroup e InactiveGroup
        go_on = driver.find_element_by_xpath("//span[text() = 'Caratteristiche delle camere']").click()
        active_services = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[@class='hotels-hr-about-amenities-Amenity__amenity--3fbBj']")
        for i in range(0,(len(active_services))):
            time.sleep(2)
            first_service = active_services[i].text
            insert_table = "INSERT INTO services (Service) VALUES (%s)"
            records_to_insert = (first_service, )
            cursor.execute(insert_table, records_to_insert)
            #soluzione per eliminare le stringhe vuote dalla tabella: effettuare una query
            cursor.execute("DELETE FROM services WHERE Service = ''")
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into services table")
            
        #problema di gestione dei div che contengono il testo di ogni servizio
        #ActiveGroup e InactiveGroup
        go_on_third = driver.find_element_by_xpath("//span[text() = 'Tipi di camera']").click()
        active_services = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[@class='hotels-hr-about-amenities-Amenity__amenity--3fbBj']")
        for i in range(0,(len(active_services))):
            time.sleep(2)
            first_service = active_services[i].text
            insert_table = "INSERT INTO services (Service) VALUES (%s)"
            records_to_insert = (first_service, )
            cursor.execute(insert_table, records_to_insert)
            #soluzione per eliminare le stringhe vuote dalla tabella: effettuare una query
            cursor.execute("DELETE FROM services WHERE Service = ''")
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into services table")
        
        cursor.execute("ALTER TABLE services CHANGE IDservice IDservice int(11) AUTO_INCREMENT PRIMARY KEY")
        connection.commit()
        
        
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


# In[132]:





# In[168]:


window_before = driver.window_handles[0]
driver.switch_to.window(window_before)


# In[ ]:





# In[60]:





# In[ ]:




