import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

BASE_URL = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+14&_sacat=0&Model=Apple%2520iPhone%252014&_dcat=9355"


def get_info(url):
    driver.get(url)
    c = driver.page_source
    s = BeautifulSoup(c)
    info = {}
    try:
        info["title"] = s.find('span', class_='u-dspn').text
    except AttributeError:
        info["title"] = "N/A"
    try:
        info["price"] = s.find('span', class_='ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD').text
    except AttributeError:
        info["price"] = "N/A"
    try:
        info["seller"] = s.find('span', class_='ux-textspans ux-textspans--PSEUDOLINK ux-textspans--BOLD').text
    except AttributeError:
        info["seller"] = "N/A"

    return info

driver.get(BASE_URL)

results = []
contents = driver.page_source
soup = BeautifulSoup(contents)

for a in soup.find_all('a', class_='s-item__link', href=True):
    link = a['href']
    results.append(get_info(link))
  

df = pd.DataFrame(results)
df.to_csv("ebay.csv")

driver.quit()


