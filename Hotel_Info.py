import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from http import cookies
import time
import re
import configparser
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import argparse
import sys

options = Options()
#options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
options.add_argument('headless')
options.add_argument('--lang=it')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)




config = configparser.ConfigParser()
config_zars = config.read('config.ini')
if not config_zars:
    exit('no config.ini')
else:
    host_zars = config['zarsDB']['host']
    user_zars = config['zarsDB']['user']
    time_zars = config['waiting time']['set_time']
    
    #passwd_zars = config["zarsDB"]["passwd"]
    #db_zars = config['zarsDB']['db']
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
ahead_input = driver.find_element_by_class_name("typeahead_input").click()

time.sleep(seconds)

input_search = driver.find_element_by_class_name("typeahead_input")
input_search.send_keys(args.place)
time.sleep(seconds)
research = driver.find_element_by_xpath("//button[@id='SUBMIT_HOTELS']").click()

time.sleep(seconds)
#driver.add_cookie({"name": "_uetsid", "value": "_uetd2a7c6e0-2416-ce9c-ead4-0042b8c47379", 'SameSite': 'None'})
#driver.add_cookie({"name": "_uetsid", "value": "_uet12514d11-bea2-dcfd-4c62-445dbbd139e0", 'SameSite': 'None'})



#close calendar
view_calendar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_1HphCM4i")))
element = driver.find_element_by_class_name("_1HphCM4i")
driver.execute_script("arguments[0].style.position = 'initial';", element)


time.sleep(seconds)




#function info
def info():
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text
    city = str(args.place)
    try:
        address = driver.find_element_by_xpath("//div[contains(@class, 'ListingEntry')]//span[contains(@class, 'ContactInfo')][2]").text
        #rating value
        rating_value = driver.find_element_by_xpath("//div[contains(@class, 'ratingContainer')]//span[contains(@class, 'ui_bubble')]")
        rating_class = rating_value.get_attribute("class")
        value_rating = rating_class[-2:]
        float_rating = value_rating[:1] + '.' + value_rating[1:]
        rating = float_rating
        review_count = driver.find_element_by_xpath("//div[contains(@class, 'ratingContainer')]//span[contains(@class, 'reviewCount')]").text
        popular_index = driver.find_element_by_xpath("//div[contains(@class, 'popIndex')]").text
        time.sleep(seconds)
    except:
        address = ""
        rating = ""
        review_count = ""
        popular_index = ""

    insert_table = "INSERT INTO info (Name, City, Address, Rating, Review_Count, Popular_Index) VALUES (%s, %s, %s, %s, %s, %s)"
    records_to_insert = [(hotel_name, city, address, rating, review_count, popular_index)]
    cursor.executemany(insert_table, records_to_insert)
    connection.commit()
    print(cursor.rowcount, "record in Info")



connection = mysql.connector.connect(
        host=host_zars,
        user=user_zars,
        #passwd=passwd_zars,
        #db = db_zars
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
    
    cursor.execute("CREATE TABLE IF NOT EXISTS info (Name VARCHAR(64) NOT NULL, City VARCHAR(64) NOT NULL, Address VARCHAR(512), Rating VARCHAR(4), Review_Count VARCHAR(64), Popular_Index VARCHAR(64))") 
    

    #manage page
    time_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'pageNum')]")))
    number_pages = driver.find_element_by_xpath("//a[contains(@class, 'pageNum')][position() = last()]").text
    pages = int(number_pages)  #conversion

    if args.pages:
        pages = args.pages

    for j in range(0,pages): 
        homepage = driver.window_handles[0]  
        time.sleep(seconds)
        view_urls = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-clicksource='HotelName']")))
        urls = driver.find_elements_by_xpath("//a[@data-clicksource='HotelName']") #url 
        driver.find_element_by_xpath("//div[@class='h1-container']").click()
        time.sleep(seconds)
        if j < (pages-1):
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #button
            time.sleep(seconds)
            for i in range(0,(len(urls))):
                urls[i].click()
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
                urls[i].click()
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




#window_before = driver.window_handles[0]
#driver.switch_to.window(window_before)





