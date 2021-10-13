import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd

list_of_properties = []
for i in range(1, 334):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
    driver = webdriver.Firefox()

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")

    for pages in listings:

        property_details = {}
        driver.get(pages["href"])

        property_details_page = BeautifulSoup(driver.page_source, "html.parser")

        price = property_details_page.find_all("script")

        details_json = ''
        for script in price:
            if "window.dataLayer" in str(script):
                script_content = str(script)
                details_json = json.loads(script_content[script_content.index('['): script_content.index(']') + 1])

            # if "window.classified" in str(script):
            #     script_content= str(script)
            #     details_string = eval(script_content[script_content.index('"facadeCount": '): script_content.index('"facadeCount": ')+2])
            #     details_string.replace(";", "")
            #     details_json = eval(details_string.replace(";", ""))
            #     print(details_string)
        element_area = property_details_page.find("p", class_="classified__information--property").text.strip().split()
        area = element_area[3] + "m2"
        #
        element_locality = property_details_page.find("span",class_="classified__information--address-row")\
            .text.replace("\n", "").strip().replace("           ", "  ")

        property_details['locality'] = None if element_locality=="" else element_locality
        property_details['type_of_property'] = None if details_json[0]['classified']['type']=="" else details_json[0]['classified']['type']
        property_details['subtype_of_property'] = None if details_json[0]['classified']['subtype']=="" else details_json[0]['classified']['subtype']
        property_details['price']= None if details_json[0]['classified']['price']=="" else details_json[0]['classified']['price']
        property_details['transactionType'] = None if details_json[0]['classified']['transactionType']=="" else details_json[0]['classified']['bedroom']['count']
        property_details['no_of_rooms'] = None if details_json[0]['classified']['bedroom']['count']=="" else details_json[0]['classified']['bedroom']['count']
        property_details['area'] = None if area =="" else area
        property_details['kitchen'] = None if details_json[0]['classified']['kitchen']['type']=="" else details_json[0]['classified']['kitchen']['type']
        property_details['garden'] = 1 if len(details_json[0]['classified']['outdoor']['garden']['surface']) != 0 else 0
        property_details['terrace'] = 1 if details_json[0]['classified']['outdoor']['terrace']['exists']=="true" else 0
        property_details['surface_area'] = None if details_json[0]['classified']['land']['surface'] == "" else details_json[0]['classified']['land']['surface']
        property_details['swimming_pool'] = 0 if details_json[0]['classified']['wellnessEquipment']['hasSwimmingPool']=="" else 1
        property_details['state_of_building'] = None if details_json[0]['classified']['building']['condition']=="" else details_json[0]['classified']['building']['condition']


        list_of_properties.append(property_details)


    driver.quit()
    print(list_of_properties)

# Creating Dataframes from the list of Dictionaries

data = list_of_properties
df = pd.DataFrame(data)
# print(df)

# Moving the index to 1


# Saving dictionary list dataframes to CSV file

df.to_csv('Demo.csv',index=False,encoding="utf-8")
