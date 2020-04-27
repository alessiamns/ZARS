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
import mysql.connector
from mysql.connector import Error
import argparse
import sys

options = Options()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

#get url
driver.get("http://www.tripadvisor.it/Hotels")
driver.maximize_window()

#search destination
parser = argparse.ArgumentParser(description='Where to?')
parser.add_argument('-place', type=str, required=True, help='search destination')
args = parser.parse_args()
ahead_input = driver.find_element_by_class_name("typeahead_input").click()

time.sleep(1)

input_search = driver.find_element_by_class_name("typeahead_input")
input_search.send_keys(args.place)
time.sleep(4)
research = driver.find_element_by_xpath("//button[@id='SUBMIT_HOTELS']").click()

time.sleep(3)

#close calendar
view_calendar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_1HphCM4i")))
element = driver.find_element_by_class_name("_1HphCM4i")
driver.execute_script("arguments[0].style.position = 'initial';", element)


time.sleep(3)



#function amenities
def amenities():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text
    try:
        view_plus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ssr-init-26f']/*[2]/following-sibling::*[1]")))
        plus = driver.find_element_by_xpath("//div[@class='ssr-init-26f']/*[2]/following-sibling::*[1]").click()
        #gestione servizi in una finestra
        active_amenities = driver.find_elements_by_xpath("//div[contains(@class, 'activeGroup')]//div[contains(@class,'amenity--3fbBj')]")
        time.sleep(3)
        for i in range(0,(len(active_amenities))):
            time.sleep(3)
            amenity_hotel = active_amenities[i].text
            
            insert_table = "INSERT INTO amenities (Name, Amenity) VALUES (%s, %s)"
            records_to_insert = [(hotel_name, amenity_hotel)]
            cursor.executemany(insert_table, records_to_insert)
        close_window = driver.find_element_by_xpath("//div[@role='button']")
        close_window.click()
        
    except:
        active_amenities = driver.find_elements_by_xpath("//div[contains(@class, 'AmenityGroup')][1]//div[contains(@class, 'Amenity')]")
        for i in range(0,(len(active_amenities))):
            amenity_hotel = active_amenities[i].text
    
            insert_table = "INSERT INTO amenities (Name, Amenity) VALUES (%s, %s)"
            records_to_insert = [(hotel_name, amenity_hotel)]
            cursor.executemany(insert_table, records_to_insert)
    #delete empty strings
    cursor.execute("DELETE FROM amenities WHERE Amenity = ''")
    connection.commit()
    print(cursor.rowcount, "Record in amenities")




#connection
try:
    
    db = "ota"+ "_" + str(args.place)


    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
            )
    cursor = connection.cursor()

    def create_db(cursor):
        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db))
        except mysql.connector.Error as error:
            print("Failed creating database: {}".format(error))
            exit(1)

    try:
        cursor.execute("USE {}".format(db))
    except mysql.connector.Error as error:
        print("Database {} does not exists.".format(db))
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            create_db(cursor)
            print("Database {} created successfully.".format(db))
            connection.database = db
        else:
            print(error)
            exit(1)
    
    
    cursor.execute("CREATE TABLE amenities (Name VARCHAR(64), Amenity VARCHAR(64)) ")    
    
    #manage pages
    time_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'pageNum')]")))
    number_pages = driver.find_element_by_xpath("//a[contains(@class, 'pageNum')][position() = last()]").text
    pages = int(number_pages) #conversion

    for j in range(0,pages):
        homepage = driver.window_handles[0]  
        #view_urls = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-clicksource='HotelName']")))
        urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
        driver.find_element_by_xpath("//div[@class='h1-container']").click()
        time.sleep(2)
        if j < (pages-1):
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #button
            time.sleep(2)
            for i in range(0,(len(urls))):
                urls[i].click()
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                time.sleep(4)
                amenities() #call the function defined
                time.sleep(4)
                driver.close()
                driver.switch_to.window(homepage)
                time.sleep(5)
            go_on.click()
            time.sleep(5)  
        else:
            for i in range(0,(len(urls))):
                urls[i].click()
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                time.sleep(4)
                amenities() #call the function defined
                time.sleep(4)
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


#window_before = driver.window_handles[0]
#driver.switch_to.window(window_before)



