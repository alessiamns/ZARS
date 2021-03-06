# ZARS
Zars is a software completely written in Python for the extraction of information relating to the accommodation facilities of a given city, passed as an argument, from a tourist portal called OTA (Online Travel agencies). With regard to each accommodation facility, Zars allows you to extract its description, services and associated reviews. The results obtained are returned in the form of a SQL database. Zars is released under the GNU General Public License v 3.0. 


## Getting Started
### Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [Xampp](https://www.apachefriends.org/download.html)
- [Chrome Driver](https://chromedriver.chromium.org/)
    #### Package
    - [Selenium](https://www.selenium.dev/downloads/)
    - [MySQL connector](https://www.mysql.com/it/products/connector/)
    - [Configparser](https://docs.python.org/3/library/configparser.html)
    - [Argparse](https://docs.python.org/3/library/argparse.html)
    - [Sys](https://docs.python.org/3/library/sys.html)
    - [Time](https://docs.python.org/3/library/time.html)
    - [Re](https://docs.python.org/3/library/re.html)
    
### Installing
Download [Zars-master](https://github.com/alessiamns/ZARS.git)

## Running the tests
### [Hotel_Info.py](Hotel_Info.py): example
```
python Hotel_Info.py -place Noto -pages 2
```
#### Arguments
> -place `[REQUIRED]`
> -pages `[OPTIONAL]`

### [Hotel_Facilities.py](Hotel_Facilities.py)
```
python Hotel_Facilities.py -place Noto -pages 2
```
#### Arguments
> -place `[REQUIRED]`
> -pages `[OPTIONAL]`

### [Hotel_Amenities.py](Hotel_Amenities.py)
```
python Hotel_Amenities.py -place Noto -pages 2
```
#### Arguments
> -place `[REQUIRED]`
> -pages `[OPTIONAL]`

### [Hotel_Reviews.py](Hotel_Reviews.py)
```
python Hotel_Reviews.py -place Noto -pages 2 -pr 2
```
#### Arguments
> -place `[REQUIRED]`
> -pages `[OPTIONAL]`
> -pr `[OPTIONAL]`

## Complete documentation
The complete technical documentation is available at this link: [Tecnical Report - IIT(CNR)](https://www.iit.cnr.it/node/58830)
