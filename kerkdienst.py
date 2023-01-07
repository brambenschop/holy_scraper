from webdriver_manager.chrome import ChromeDriverManager                            # Needed for Selenium                   #
from selenium.webdriver.common.by import By                                         # Needed for Selenium                   #
from selenium.webdriver.chrome.service import Service                               # Needed for Selenium                   #
from selenium import webdriver                                                      # Needed for Selenium                   #
import pandas as pd                                                                 # Used for exporting to csv             #                 
import time                                                                         # Used for waiting                      #
                                                                                                                            #
PATH = 'driver/chromedriver'                                                        # Set to path of local chromedriver     #
INIT = 'https://kerkdienstgemist.nl/stations/1883-Hervormde-kerk-Kamerik/events'    # Set to initial link to visit          #
#############################################################################################################################

service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=service)
driver.get(INIT)
time.sleep(5)

SCROLL_PAUSE_TIME = 0.5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

diensten = driver.find_elements("xpath", "//*[contains(@class, 'ember-view events-grid-item')]")
diensten.pop(0)

dienst_list = []
dienst_urls = []

for dienst in diensten:
    dienst_urls.append(dienst.get_attribute('href'))

for url in dienst_urls:
    driver.get(url)

    time.sleep(5)
    dienst_info = driver.find_element("xpath", "//*[contains(@class, 'media-player-info')]")
    dienst_typeTijd = dienst_info.find_elements("xpath", "//*[contains(@class, 'event-title')]")
    dienst_type = dienst_typeTijd[0].text
    dienst_tijdRaw = dienst_typeTijd[1].text.split(' ')

    dienst_dagNaam = dienst_tijdRaw[0]
    dienst_dagNummer = dienst_tijdRaw[1]
    dienst_dagMaand = dienst_tijdRaw[2]
    dienst_dagJaar = dienst_tijdRaw[3]
    dienst_dagUur =  dienst_tijdRaw[4].split(":")[0]
    dienst_dagMinuut = dienst_tijdRaw[4].split(":")[1]

    try:
        dienst_persoon = dienst_info.find_elements("xpath", "//*[contains(@class, 'content__artist')]")[0].text
    except:
        dienst_persoon = 'Onbekend'
    
    try:
        dienst_psalmen = dienst_info.find_elements("xpath", "//*[contains(@class, 'truncated-toggle__content')]")[0].find_element(By.TAG_NAME, 'p').text
    except:
        dienst_psalmen = 'Onbekend'

    output = [dienst_dagJaar, dienst_dagMaand, dienst_dagNummer, dienst_dagNaam, dienst_dagUur, dienst_dagMinuut, dienst_type, dienst_persoon, dienst_psalmen] 
    dienst_list.append(output)

colnames = ['Jaar', 'Maand', 'Dag', 'DagNaam', 'Uur', 'Minuut', 'Type', 'Persoon', 'Psalmen']

df_diensten = pd.DataFrame(dienst_list, columns=colnames)
df_diensten.to_csv("data/diensten.csv", index=False)