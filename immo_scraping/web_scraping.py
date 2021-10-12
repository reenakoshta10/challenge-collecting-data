import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd
import re

list_of_properties = []  # This list will keep all  properties from dict.

# In ImmoWeb there is total 333 pages for apartment and house.It will help us to reach all these pages
for i in range(1, 334):
    page_num = str(i) + "&orderBy=relevance"
    url = (
        "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=" + page_num
    )
    driver = webdriver.Chrome(
        executable_path="/Users/yusufakcakaya/Desktop/chromedriver"
    )
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # it finds all links in a page
    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:

        property_details = {}  # creates a dict for properties
        driver.get(pages["href"])
        property_details_page = BeautifulSoup(driver.page_source, "html.parser")

        try:  # it tries to find all data for locality
            element_locality = (
                property_details_page.find(
                    "span", class_="classified__information--address-row"
                )
                .text.replace("\n", "")
                .strip()
            )
            locality = re.sub(" +", " ", element_locality)
            property_details["Locality"] = locality
        except ConnectionError:
            raise RuntimeError("Failed to open website")

        try:  # it tries to find all data for type_of_property
            element_type_of_property = (
                property_details_page.find("h1", class_="classified__title")
                .text.replace("\n", "")
                .strip()
                .split()
            )
            type_of_property = element_type_of_property[0]
            property_details["type_of_property"] = type_of_property
        except ConnectionError:
            raise RuntimeError("Failed to open website")

        # we are just checking for house or apartment
        property_details["subtype_of_property"] = None

        try:  # it tries to find all data for price
            element_price = property_details_page.find("p", class_="classified__price")
            price = element_price.find_all("span")[1].text
            property_details["price"] = price
        except ConnectionError:
            raise RuntimeError("Failed to open website")

        list_of_properties.append(property_details)
    print(list_of_properties)

    driver.quit()
