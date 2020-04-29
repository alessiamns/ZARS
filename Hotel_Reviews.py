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
from mysql.connector import errorcode
import argparse
import sys

options = Options()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

#get url
driver.get("http://www.tripadvisor.it/Hotels")
driver.maximize_window()

parser = argparse.ArgumentParser()
parser.add_argument('-pr', type=int, help='enter number pages reviews')
parser.add_argument('-place', type=str, required=True, help='enter with the city name')
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



#function reviews: property name, rating, review, hometown, date, triptype for each property
def reviews():
    
    hotel_name = driver.find_element_by_xpath("//h1[contains(@class, 'hotel-review')]").text 
    go_review = driver.find_element_by_xpath("//span[contains(@class, 'reviewCount')]")
    go_review.click() #su per scendere giu alle recensioni
    
    time_page = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'pageNum')]")))
    number_pages = driver.find_element_by_xpath("//a[contains(@class, 'pageNum')][position() = last()]").text
    pages_review = int(number_pages) #conversion

    if args.pr:
        pages_review = args.pr
    
    for j in range(0,pages_review): 
        insert_table = "INSERT INTO reviews (Name, Rating, Review, Hometown, Date_of_stay, Trip_type) VALUES (%s, %s, %s, %s, %s, %s)"
        
        if j < (pages_review-1): 
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #button
            language = driver.find_element_by_xpath("//span[contains(text(),'Italiano')]")
            language.click() #language
            view_plus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'Expandable')]//span[contains(text(),'Scopri di pi')]")))
            info_plus = driver.find_element_by_xpath("//div[contains(@class,'Expandable')]//span[contains(text(),'Scopri di pi')]")
            info_plus.click() 
            time.sleep(1)
            all_reviews = driver.find_elements_by_xpath("//q[contains(@class, 'location-review')]") 
            
            for i in range(0,(len(all_reviews))): #loop reviews
                review = all_reviews[i].text
                ix = str(i+1) #index
                #//a[contains(@class, 'MemberEvent')] nome di chi lascia la recensione (se dovesse servire)
                rating_value = driver.find_element_by_xpath("//div[contains(@class, 'RatingLine')]//span[contains(@class, 'ui_bubble')]")
                rating_class = rating_value.get_attribute("class")
                length_class = len(rating_class)
                value_rating_len = rating_class[length_class-2]
                rating = int(value_rating_len) #rating (1 a 5)
                try:
                    hometown_element = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class,'hometown-')]") #hometown
                    date_element = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class, 'event_date')]") #date
                    triptype_element = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')]["+ ix + "]//span[contains(@class, 'TripType')]") #type
                    
                    hometown = hometown_element.text
                    
                    date_bef = date_element.text
                    date = date_bef.replace('Data del soggiorno:', '')
                    
                    triptype_bef = triptype_element.text
                    triptype = triptype_bef.replace('Tipo di viaggio:', '')
                except:
                    hometown = ""
                    date = ""
                    triptype = ""
                    
                records_to_insert = [(hotel_name, rating, review, hometown, date, triptype)]
                cursor.executemany(insert_table, records_to_insert)
                connection.commit()
            print(cursor.rowcount, "Record in recensioni")
            go_on.click()
            time.sleep(5)            
        
        else: #last page
            
            language = driver.find_element_by_xpath("//span[contains(text(),'Italiano')]")
            language.click()
            view_plus = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'Expandable')]//span[contains(text(),'Scopri di pi')]")))
            info_plus = driver.find_element_by_xpath("//div[contains(@class, 'location-review')]//span[contains(text(),'Scopri di pi')]")
            info_plus.click() 
            time.sleep(1)
            all_reviews = driver.find_elements_by_xpath("//q[contains(@class, 'location-review')]")
            for i in range(0,(len(all_reviews))):
                review = all_reviews[i].text 
                ix = str(i+1) #index
                #//a[contains(@class, 'MemberEvent')] nome di chi lascia la recensione (se dovesse servire)
                rating_value = driver.find_element_by_xpath("//div[contains(@class, 'RatingLine')]//span[contains(@class, 'ui_bubble')]")
                rating_class = rating_value.get_attribute("class")
                length_class = len(rating_class)
                value_rating_len = rating_class[length_class-2]
                rating = int(value_rating_len) #rating (da 1 a 5)
                try:
                    hometown_element = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class,'hometown-')]")
                    date_element = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')][" + ix + "]//span[contains(@class, 'event_date')]")
                    triptype_element = driver.find_element_by_xpath("//div[contains(@class,'hotels-community')]["+ ix + "]//span[contains(@class, 'TripType')]")
                    
                    hometown = origin.text
                    
                    date_bef = eventdate.text
                    date = text_eventdate1.replace('Data del soggiorno:', '')
                    
                    triptype_bef = triptype.text
                    triptype = text_triptype1.replace('Tipo di viaggio:', '')
                except:
                    hometown = ""
                    date = ""
                    triptype = ""
                
                
                records_to_insert = [(hotel_name, rating, review, hometown, date, triptype)]
                cursor.executemany(insert_table, records_to_insert)
                connection.commit()
            print(cursor.rowcount, "Record in recensioni")


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
    
    
    cursor.execute("CREATE TABLE reviews (ID_hotel int(11), Name VARCHAR(64), Rating int(2), Review VARCHAR(512), Hometown VARCHAR(64), Date_of_stay VARCHAR(64), Trip_type VARCHAR(64), Language VARCHAR(64)) ")
    
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
            go_on = driver.find_element_by_xpath("//a[contains(text(),'Avanti')]") #scorre le pagine
            time.sleep(2)
            for i in range(0,(len(urls))):
                urls[i].click()
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                time.sleep(4)
                reviews() #call the function defined
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
                reviews() #call the function defined
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




