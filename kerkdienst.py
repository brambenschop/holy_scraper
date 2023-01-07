import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

link = input("https://kerkdienstgemist.nl/stations/1883-Hervormde-kerk-Kamerik/events")

wait = WebDriverWait(driver, 10)
driver.get(link)

get_url = driver.current_url
wait.until(EC.url_to_be(link))

if get_url == link:
    page_source = driver.page_source

#nog ff aanpassen
#Kan deze code weg?
soup = BeautifulSoup(page_source,features="html.parser")
keyword=input("Enter a keyword to find instances of in the article:")
matches = soup.body.find_all(string=re.compile(keyword))

len_match = len(matches)

title = soup.title.text