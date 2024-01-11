## READING A SINGLE CONFIG FILE AND PRINTING OFF DATA IN A TIME SERIES IN AN EXTERNAL TEXT FILE ##

# importing relevent packages
import cdflib
import configparser
import os
import numpy as np
from datetime import datetime, timedelta
import ephem
from datetime import datetime

config = configparser.ConfigParser()
# reading my config file
config.read('config.dat')
# defining the location of the file being read 
savelocation = config['Path']['savelocation']
# reading the CDF file
cdffile = cdflib.CDF(savelocation)

# defining variables saved in the CDF file onto python
timestamp = cdffile.varget('Timestamp')
lat = cdffile.varget('Latitude')
lon = cdffile.varget('Longitude')   
height = cdffile.varget('Height')   
electemp = cdffile.varget('T_elec')    

# adjusting the year of collection to be 2023
target_year = 2023
# converting seconds measurement into correct units
seconds_array = timestamp / 1000.0
# converting the time given in the CDF file to current time in the form dd/mm/yyyy and hour:minutes
date_time_array = np.array([datetime.utcfromtimestamp(seconds) for seconds in seconds_array])
formatted_date_array = np.array([dt.strftime("%d/%m/%Y %H:%M") for dt in date_time_array])
adjusted_date_array = np.array([dt.replace(year=target_year) for dt in date_time_array])
adjustedtime = np.array([dt.strftime("%d/%m/%Y %H:%M") for dt in adjusted_date_array])
# printing adjusted times/dates
print(f"The adjusted dates are: {adjustedtime}")

# read the config file again
config.read('config.dat')
# creating a new text file specified by the config file
path = config['Output']['textfile']

# open the text file just created and writing in each variable name at the top of the file
with open(path, 'w') as file:
    file.write('Time Stamp\tHeight\tLatitude\tLongitude\tElectron Temperature\n')
#for each specific data point in each variable print off the data in the text file     
    for elem1, elem2, elem3, elem4, elem5 in zip(adjustedtime, height, lat, lon, electemp):
        file.write(f"{elem1}\t{elem2}\t{elem3}\t{elem4}\t{elem5}\n")

################################################################################################################################      

## USING WEBDRIVER TO NAVIGATE TO THE SWARM DATA WEBSITE (NOT FINISHED -- WILL BE USING HAPI TO REPLACE THIS CODE) ##
                  
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import configparser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

# specifying where I would like data saved via the config file
config = configparser.ConfigParser()
config.read('config.dat')
savelocation = config['Path']['savelocation']

# defining webdriver as the variable driver
driver = webdriver.Chrome()

# opening the website of interest
driver.get('https://swarm-diss.eo.esa.int')

# navigating to and clicking on the 'advanced' hyperlink 
link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced"]')))
link.click()

# navigating to and clicking on the 'Plasma_Data' hyperlink  
link2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced%2FPlasma_Data"]')))
link2.click()

# navigating to and clicking on the '2_Hz_Langmuir_Probe_Extended_Dataset' hyperlink 
link3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced%2FPlasma_Data%2F2_Hz_Langmuir_Probe_Extended_Dataset"]')))
link3.click()

# navigating to and clicking on the 'Sat A' hyperlink 
link4 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced%2FPlasma_Data%2F2_Hz_Langmuir_Probe_Extended_Dataset%2FSat_A"]')))
link4.click()

# close the website
driver.quit()


