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
    cursor.execute("CREATE TABLE strutture (IDhotel int(11) AUTO_INCREMENT PRIMARY KEY, NomeHotel VARCHAR(64),  tipologia VARCHAR(128), url VARCHAR(256)) ")


    def listnames():
        hotelnames = driver.find_elements_by_xpath("//*[@class='listing_title']") #nomi hotel
        structuretype = driver.find_elements_by_xpath("//span[@class='label']")

        for i in range(0,(len(hotelnames))):
            links = driver.find_element_by_link_text(hotelnames[i].text).get_attribute('href')
            hotelnames[i].text #nome struttura

        for i in range(0,(len(structuretype))):
            structuretype[i].text  #tipologia di struttura

            insert_table = "INSERT INTO strutture (NomeHotel, tipologia, url) VALUES (%s, %s, %s)"

            records_to_insert = [(hotelnames[i].text, structuretype[i].text , links)]

            cursor.executemany(insert_table, records_to_insert)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into provastrutture table")

    def cambiopag():
        num_pages = driver.find_elements_by_xpath("//div[@class='pageNumbers']/a")
        last = len(num_pages)-1
        count = int(num_pages[last].get_attribute("data-page-number"))
        for i in range(count-1):
            listnames()
            time_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='nav next ui_button primary']")))
            page = driver.find_element_by_xpath("//a[@class='nav next ui_button primary']")
            page.click()



    cambiopag()
    
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")