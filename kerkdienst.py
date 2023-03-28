from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

path = 'chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

linkje = 'https://kerkdienstgemist.nl/stations/1883-Hervormde-kerk-Kamerik/events'
driver.get(linkje)
time.sleep(5)

SCROLL_PAUSE_TIME = 0.5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height