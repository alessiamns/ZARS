"""ZARS Copyright (C) 2020  AMns


ZARS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.


ZARS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. """


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
import time
import re
import configparser
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import argparse
import sys

start = time.time()


options = Options()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
options.add_argument('headless')
options.add_argument('--lang=it')

driver = webdriver.Chrome(options=options)

config = configparser.ConfigParser()
config_zars = config.read('config.ini')
if not config_zars:
    exit('no config.ini')
else:
    host_zars = config['zarsDB']['host']
    user_zars = config['zarsDB']['user']
    time_zars = config['waiting time']['set_time']
    seconds = int(time_zars)

if not host_zars or not user_zars or not time_zars:
    exit('parametri file config.ini non definiti')

#get url
driver.get("http://www.tripadvisor.it/Hotels")
driver.maximize_window()

parser = argparse.ArgumentParser()
parser.add_argument('-place', type=str, required=True, help='enter with the city name')
parser.add_argument('-pages', type=int, help='enter number pages')
args = parser.parse_args()
ahead_input = driver.find_element_by_xpath("//div[contains(@class, 'typeahead_widget_component')]").click()
time.sleep(seconds)
input_search = driver.find_element_by_xpath("//div[@data-test-attribute='typeahead-trip_search_Hotels']//input[@type='search']")
input_search.send_keys(args.place)
time.sleep(seconds)
driver.find_element_by_xpath("//a[@title='" + args.place + "']").click()
#research = driver.find_element_by_xpath("//button[@id='SUBMIT_HOTELS']").click()
time.sleep(seconds)

#close calendar
calendar = driver.find_element_by_class_name("_1HphCM4i")
driver.execute_script("arguments[0].style.position = 'initial';", calendar)
time.sleep(seconds)

#function info
def info():
    insert_table = "INSERT INTO info (Name, City, Address, Url, Rating, Review_Count, Popular_Index) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text
    city = str(args.place)
    try:
        address = driver.find_element_by_xpath("//div[contains(@class, 'ListingEntry')]//span[contains(@class, 'ContactInfo')][2]").text
    except:
        address = ""
    try:
        rating_value = driver.find_element_by_xpath("//div[contains(@class, 'ratingContainer')]//span[contains(@class, 'ui_bubble')]")
        rating_class = rating_value.get_attribute("class")
        value_rating = rating_class[-2:]
        float_rating = value_rating[:1] + '.' + value_rating[1:]
        rating = float(float_rating)
    except:
        rating = None
    try:
        review_count = driver.find_element_by_xpath("//div[contains(@class, 'ratingContainer')]//span[contains(@class, 'reviewCount')]").text
    except:      
        review_count = ""
    try:
        popular_index = driver.find_element_by_xpath("//div[contains(@class, 'popIndex')]").text
    except:
        popular_index = ""

    time.sleep(seconds)

    records_to_insert = [(hotel_name, city, address, text_url, rating, review_count, popular_index)]
    cursor.executemany(insert_table, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "record in Info")

connection = mysql.connector.connect(
        host=host_zars,
        user=user_zars
            )
cursor = connection.cursor()

#connection
try:    
    db = "zars"
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
    
    cursor.execute("CREATE TABLE IF NOT EXISTS info (Name VARCHAR(64) NOT NULL, City VARCHAR(64) NOT NULL, Address VARCHAR(512), Url VARCHAR(512), Rating FLOAT(2,1), Review_Count VARCHAR(64), Popular_Index VARCHAR(64), PRIMARY KEY(Name, City))") 
    
    #manage page
    number_pages = driver.find_element_by_xpath("//a[contains(@class, 'pageNum')][position() = last()]").text
    pages = int(number_pages)  #conversion

    if args.pages:
        pages = args.pages

    for j in range(0,pages): 
        homepage = driver.window_handles[0]  
        time.sleep(seconds)
        urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
        driver.find_element_by_xpath("//div[@class='h1-container']").click()
        time.sleep(seconds)
        if j < (pages-1):
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #button
            time.sleep(seconds)
            for i in range(0,(len(urls))):
                try:
                    ads = driver.find_element_by_tag_name("iframe")
                    driver.switch_to.frame(ads)
                    time.sleep(seconds)
                    driver.switch_to.default_content()
                    hotel_url = urls[i]
                    text_url = hotel_url.get_attribute("href")
                    hotel_url.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    info() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
                except:
                    hotel_url = urls[i]
                    text_url = hotel_url.get_attribute("href")
                    hotel_url.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    info() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
            go_on.click()
            time.sleep(seconds)  
        else:
            for i in range(0,(len(urls))):
                try:
                    ads = driver.find_element_by_tag_name("iframe")
                    driver.switch_to.frame(ads)
                    time.sleep(seconds)
                    driver.switch_to.default_content()
                    hotel_url = urls[i]
                    text_url = hotel_url.get_attribute("href")
                    hotel_url.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    info() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)
                except:
                    hotel_url = urls[i]
                    text_url = hotel_url.get_attribute("href")
                    hotel_url.click()
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    time.sleep(seconds)
                    info() #call the function defined
                    time.sleep(seconds)
                    driver.close()
                    driver.switch_to.window(homepage)
                    time.sleep(seconds)              
    driver.quit()
                
except mysql.connector.Error as error:
    print("Failed to insert record into MySQL table {}".format(error))

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


end = time.time()
#test time
print(end - start)

