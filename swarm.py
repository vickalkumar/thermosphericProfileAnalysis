
import cdflib
import os
import numpy as np
from datetime import datetime, timedelta
import ephem
from datetime import datetime

cdffile = cdflib.CDF('/Users/madelinefarrugia/march1.cdf')

variable2 = cdffile.varget('Timestamp')
variable3 = cdffile.varget('Latitude')
variable4 = cdffile.varget('Longitude')   
variable5 = cdffile.varget('Height')   
variable6 = cdffile.varget('T_elec')    

target_year = 2023
seconds_array = variable2 / 1000.0
date_time_array = np.array([datetime.utcfromtimestamp(seconds) for seconds in seconds_array])
formatted_date_array = np.array([dt.strftime("%d/%m/%Y %H:%M") for dt in date_time_array])
adjusted_date_array = np.array([dt.replace(year=target_year) for dt in date_time_array])
formatted_adjusted_date_array = np.array([dt.strftime("%d/%m/%Y %H:%M") for dt in adjusted_date_array])
print(f"The adjusted dates are: {formatted_adjusted_date_array}")

path = '/Users/madelinefarrugia/swarm.txt'

with open(path, 'w') as file:
    file.write('Time Stamp\tHeight\tLatitude\tLongitude\tElectron Temperature\n')
    for elem1, elem2, elem3, elem4, elem5 in zip(formatted_adjusted_date_array, variable5, variable3, variable4, variable6):
        #file.write('{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\t{:.4f}\n'.format(elem1, elem2, elem3, elem4, elem5))
        file.write(f"{elem1}\t{elem2}\t{elem3}\t{elem4}\t{elem5}\n")

################################################################################################################################        
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import configparser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

config = configparser.ConfigParser()
config.read('config.dat')
savelocation = config['Path']['savelocation']

driver = webdriver.Chrome()
driver.get('https://swarm-diss.eo.esa.int')

link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced"]')))
link.click()
link2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced%2FPlasma_Data"]')))
link2.click()
link3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced%2FPlasma_Data%2F2_Hz_Langmuir_Probe_Extended_Dataset"]')))
link3.click()
link4 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#swarm%2FAdvanced%2FPlasma_Data%2F2_Hz_Langmuir_Probe_Extended_Dataset%2FSat_A"]')))
link4.click()
data = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="?do=download&amp;file=swarm%2FAdvanced%2FPlasma_Data%2F2_Hz_Langmuir_Probe_Extended_Dataset%2FSat_A%2FSW_EXTD_EFIA_LP_HM_20131202T101113_20131202T140109_0102.CDF.ZIP"]')))
data.click()

driver.quit()