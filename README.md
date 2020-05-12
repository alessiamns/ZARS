# ZARS
Software per l’estrazione di informazioni relative alle strutture 
ricettive di una data città da un portale turistico cosiddetto OTA (Online Travel Agencies). 

## Prerequisites
- Python 3 (https://www.python.org/downloads/)
- Xampp (https://www.apachefriends.org/download.html)
- Chrome Driver (https://chromedriver.chromium.org/)
    ### Package
    - Selenium
    - MySQL connector
    - Configparser
    - Argparse
    - Sys 
    - Time
    - Re
    
## Installing
Download [Zars-master](https://github.com/alessiamns/ZARS.git)

## Running the tests
### Example [Hotel_Info.py](Hotel_Info.py)

```
python Hotel_Info.py -place Noto -pages 2
```
### Example [Hotel_Facilities.py](Hotel_Facilities.py)

```
python Hotel_Facilities.py -place Noto -pages 2
```
