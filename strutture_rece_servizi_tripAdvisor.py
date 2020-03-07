#!/usr/bin/env python
# coding: utf-8

# In[57]:


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


# In[58]:


driver = webdriver.Chrome('chromedriver.exe')
wait = WebDriverWait(driver, 15)
chrome_options = Options()
driver.get("http://www.tripadvisor.it")
driver.maximize_window()


# In[59]:


hotels = driver.find_element_by_xpath("//a[@href= '/Hotels']")

actions = ActionChains(driver)
actions.click(hotels) 
time.sleep(4)
actions.send_keys("noto")
actions.perform()
time.sleep(3)
actions.send_keys(Keys.ENTER).perform()


# In[ ]:


url = driver.current_url
print (url)


# In[83]:


#FUNZIONA
#tabella recensioni CON DATA DEL SOGGIORNO E TIPOLOGIA VIAGGIO
def recensioni():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text #nome hotel
    go_rece = driver.find_element_by_xpath("//span[contains(@class, 'reviewCount')]").click() #su per scendere giu alle recensioni
    time_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'pageNum')]")))
    number_pages = driver.find_element_by_xpath("//a[contains(@class, 'pageNum')][position() = last()]").text
    pages = int(number_pages) #numero di pagine
    for j in range(0,pages): #ciclo per tutte le pagine
        insert_table = "INSERT INTO recensioni (NomeHotel, Recensione, Provenienza, DataSoggiorno, TipologiaViaggio) VALUES (%s, %s, %s, %s, %s)"
        if j < (pages-1): #condizione per tutte le pagine tranne l'ultima
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #scorre le pagine
            the_rece = driver.find_elements_by_xpath("//q[contains(@class, 'location-review')]") #recensioni
            language = driver.find_element_by_xpath("//span[contains(text(),'Italiano')]").click() #lingua selezionata
            time.sleep(1)
            for i in range(0,(len(the_rece))): #ciclo per tutte le recensioni
                the_rece[i].click() #clicca per espandere
                text_rece = the_rece[i].text
                ix = str(i+1) #indice per estrarre info
                try:
                    origin = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class,'hometown-')]") #provenienza
                    eventdate = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class, 'event_date')]") #data del soggiorno
                    triptype = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')]["+ ix + "]//span[contains(@class, 'TripType')]") #tipo di viaggio
                    
                    text_origin = origin.text
                    
                    text_eventdate1 = eventdate.text
                    text_eventdate = text_eventdate1.replace('Data del soggiorno:', '')
                    
                    text_triptype1 = triptype.text
                    text_triptype = text_triptype1.replace('Tipo di viaggio:', '')
                except:
                    text_origin = ""
                    text_eventdate = ""
                    text_triptype = ""
                    
                records_to_insert = [(hotel_name, text_rece, text_origin, text_eventdate, text_triptype)]
                cursor.executemany(insert_table, records_to_insert)
                connection.commit()
            print(cursor.rowcount, "Record in recensioni")
            go_on.click()
            time.sleep(5)            
        else: #condizione per l'ultima pagina
            the_rece = driver.find_elements_by_xpath("//q[contains(@class, 'location-review')]")
            language = driver.find_element_by_xpath("//span[contains(text(),'Italiano')]").click()
            time.sleep(1)
            for i in range(0,(len(the_rece))):
                the_rece[i].click()
                text_rece = the_rece[i].text 
                ix = str(i+1)
                try:
                    origin = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class,'hometown-')]")
                    eventdate = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class, 'event_date')]")
                    triptype = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')]["+ ix + "]//span[contains(@class, 'TripType')]")
                    
                    text_origin = origin.text
                    
                    text_eventdate1 = eventdate.text
                    text_eventdate = text_eventdate1.replace('Data del soggiorno:', '')
                    
                    text_triptype1 = triptype.text
                    text_triptype = text_triptype1.replace('Tipo di viaggio:', '')
                except:
                    text_origin = ""
                    text_eventdate = ""
                    text_triptype = ""
                
                
                records_to_insert = [(hotel_name, text_rece, text_origin, text_eventdate, text_triptype)]
                cursor.executemany(insert_table, records_to_insert)
                connection.commit()
            print(cursor.rowcount, "Record in recensioni")
            


# In[84]:


#FUNZIONA
#tabella servizi
def servizi():
    mostraplus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Mostra di più')]")))
    plus = driver.find_element_by_xpath("//div[contains(text(),'Mostra di più')]")
    plus.click()
    #gestione servizi in una finestra
    active_services = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[@class='hotels-hr-about-amenities-Amenity__amenity--3fbBj']")
    time.sleep(3)
    for i in range(0,(len(active_services))):
        time.sleep(3)
        first_service = active_services[i].text
        
        
        insert_table = "REPLACE INTO servizi (Service) VALUES (%s)"
        records_to_insert = (first_service, )
        cursor.execute(insert_table, records_to_insert)
        #soluzione per eliminare le stringhe vuote dalla tabella: effettuare una query
        #cursor.execute("DELETE FROM servizi1 WHERE Service = ''")
        connection.commit()
    print(cursor.rowcount, "Record in servizi")
    
    #a idservice viene aggiunto auto_increment dopo aver eliminato le stringhe vuote
    #cursor.execute("ALTER TABLE servizi1 CHANGE IDservice IDservice int(11) AUTO_INCREMENT")
    cursor.execute("ALTER TABLE servizi AUTO_INCREMENT = 1")
    connection.commit()

    close_window = driver.find_element_by_xpath("//div[@role='button']").click()


# In[85]:


#creazione tabella strutture
def strutture():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text
    #url_hotel = driver.current_url
    address_hotel = driver.find_element_by_xpath("//div[@class='public-business-listing-ContactInfo__offer--KAFI4 public-business-listing-ContactInfo__atfInfo--3wJ1b']/span[2]").text
    insert_table = "INSERT INTO strutture (NomeHotel, indirizzo) VALUES (%s, %s)"
    
    records_to_insert = [(hotel_name, address_hotel)]
    cursor.executemany(insert_table, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "Record in strutture")


# In[86]:


#connessione al db
try:
        
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="ota"
            )
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE strutture (IDhotel int(11) AUTO_INCREMENT PRIMARY KEY, NomeHotel VARCHAR(64), indirizzo VARCHAR(128)) ")
    cursor.execute("CREATE TABLE servizi (IDservice int(11) UNIQUE , Service VARCHAR(64) PRIMARY KEY) ")
    cursor.execute("CREATE TABLE recensioni (ID_hotel int(11), NomeHotel VARCHAR(64), Recensione VARCHAR(512), Provenienza VARCHAR(64), DataSoggiorno VARCHAR(64), TipologiaViaggio VARCHAR(64), Lingua VARCHAR(64)) ")
    
    
    
    homepage = driver.window_handles[0]  
    urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
    for i in range(0,(len(urls))):
        urls[i].click()
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        time.sleep(3)
        strutture()
        servizi()
        recensioni()
        time.sleep(3)
        driver.close()
        driver.switch_to.window(homepage)
    
    
    cursor.execute("CREATE TABLE provajoin SELECT strutture.IDhotel, recensioni.NomeHotel, recensioni.Recensione, recensioni.Provenienza, recensioni.DataSoggiorno FROM strutture RIGHT JOIN recensioni ON strutture.NomeHotel = recensioni.NomeHotel")
    
    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


# In[82]:


window_before = driver.window_handles[0]
driver.switch_to.window(window_before)


# In[ ]:





# In[ ]:




