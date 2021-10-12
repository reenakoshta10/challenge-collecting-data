import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd


list_of_properties = []
for i in range(1, 3):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
    driver = webdriver.Chrome(executable_path="driver/chromedriver")
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:
        
        property_details ={}
        driver.get(pages["href"])
        property_details_page= BeautifulSoup(driver.page_source, "html.parser")
        
        price = property_details_page.find("p", class_="classified__price")
        property_details['price']= price

        print(price)
        list_of_properties.append(property_details)

    driver.quit()
