import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd

houses_url = []

driver = webdriver.Chrome(executable_path="/Users/yusufakcakaya/Desktop/chromedriver")
for i in range(1, 334):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:
        houses_url.append(pages["href"])

print(houses_url)
print((len(houses_url)))

path_csv = "/Users/yusufakcakaya/PycharmProjects/change_collecting_data.house_apartments_urls.csv"
with open(path_csv, 'w') as file:
    for page_url in houses_url:
        for url in page_url:
            file.write(url + '\n')