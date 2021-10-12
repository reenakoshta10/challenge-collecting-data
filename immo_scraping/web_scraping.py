import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd

all_urls = []

driver = webdriver.Chrome(executable_path="/Users/yusufakcakaya/Desktop/chromedriver")
for i in range(1, 334):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:
        all_urls.append(pages["href"])


print((len(all_urls)))

