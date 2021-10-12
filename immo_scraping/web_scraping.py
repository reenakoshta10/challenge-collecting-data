import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd

list_of_properties = []
for i in range(1, 2):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=" + page_num
    driver = webdriver.Firefox()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:

        property_details = {}
        driver.get(pages["href"])
        property_details_page = BeautifulSoup(driver.page_source, "html.parser")

        try:
            # element = property_details_page.find("span", class_="overview__text")
            #
            # room = element.text.strip()
            # property_details['room'] = room
            # element = property_details_page.find("p", class_="classified__information--property").text.strip().split()
            # element = element[3]+element[4]
            # property_details['area'] = element
            element = property_details_page.find("tb")
            property_details['kitchen'] = element

        except ConnectionError:
            raise RuntimeError('Failed to open website')


        list_of_properties.append(property_details)
        print(list_of_properties)

    driver.quit()