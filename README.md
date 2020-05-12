# ZARS
Software per l’estrazione di informazioni relative alle strutture ricettive di una data città da un portale turistico.

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
### [Hotel_Amenities.py](Hotel_Amenities.py)

```
python Hotel_Amenities.py -place Noto -pages 2
```
### [Hotel_Reviews.py](Hotel_Reviews.py)

```
python Hotel_Reviews.py -place Noto -pages 2 -pr 2
```
