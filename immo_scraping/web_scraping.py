import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd
import re

list_of_properties = []
for i in range(1, 2):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=" + page_num
    driver = webdriver.Chrome(executable_path="/Users/yusufakcakaya/Desktop/chromedriver")
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:

        property_details = {}
        driver.get(pages["href"])
        property_details_page = BeautifulSoup(driver.page_source, "html.parser")

        try:
            element_price = property_details_page.find("p", class_="classified__price")
            price = element_price.find_all("span")[1].text
            property_details['price'] = price
        except ConnectionError:
            raise RuntimeError('Failed to open website')

        try:
            element_locality = property_details_page.find("span", class_="classified__information--address-row").text.replace("\n", "").strip()
            locality = re.sub(" +", " ", element_locality)
            property_details['Locality'] = locality
        except ConnectionError:
            raise RuntimeError('Failed to open website')


        list_of_properties.append(property_details)
    print(list_of_properties)


    driver.quit()
