import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import pandas as pd
from threading import Thread


for i in range(163, 244): # To iterate through the given pages of the Immoweb website
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=" + page_num
    list_of_properties = []

    time.sleep(2) # To give a 2 second break to the browser before every page opens
    driver = webdriver.Chrome(executable_path="driver/chromedriver")
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser") # Using BeautifulSoup to parse through html

    listings = soup.find_all("a", class_="card__title-link")
    for pages in listings:

        property_details = {}
        driver.get(pages["href"])
        property_details_page = BeautifulSoup(driver.page_source, "html.parser")

        script_list = property_details_page.find_all("script")

    '''The attributes that we need are under 'window.dataLayer' and 'window.classified'.
    So we save those scripts in a json file and fetch the required attributes.'''
    
        details_json = ''
        for script in script_list:
            if "window.dataLayer" in str(script):
                script_content = str(script)
                details_json = json.loads(script_content[script_content.index('['): script_content.index(']') + 1])

            if "window.classified" in str(script):
                script_content = str(script)
                facade_count = ''
                fireplace_exist = ''
                isFurnished = ''
                living_area = ''
                if '"facadeCount":' in script_content:
                    facade_count = script_content.split('"facadeCount":')[1][:2].replace(",", "")
                if '"fireplaceExists":' in script_content:
                    fireplace_exist = script_content.split('"fireplaceExists":')[1][:5].replace(",", "")
                if '"isFurnished":' in script_content:
                    isFurnished = script_content.split('"isFurnished":')[1][:5].replace(",", "")
                if '"netHabitableSurface"' in script_content:
                    # str1= (script_content.split('"netHabitableSurface":')[1]).split(',')[0]
                    living_area = (script_content.split('"netHabitableSurface":')[1]).split(',')[0]
                    
                    
        ''' Fetching the data of the 'locality' element from the HTML file.
        Extra lines and spaces have been removed.'''

        element_locality = property_details_page.find("span", class_="classified__information--address-row") \
            .text.replace("\n", "").strip().replace("           ", "  ")

        ''' Fetching the data of various attributes from json file.
         If the value of the attribute is empty ie. '', then it will be assigned as None, 
         else it will return the data as specified.'''

        property_details["Locality"] = (
            None if element_locality == "" else element_locality
        )
        property_details["Type_of_property"] = (
            None
            if details_json[0]["classified"]["type"] == ""
            else details_json[0]["classified"]["type"]
        )
        property_details["Subtype_of_property"] = (
            None
            if details_json[0]["classified"]["subtype"] == ""
            else details_json[0]["classified"]["subtype"]
        )
        property_details["Price"] = (
            None
            if details_json[0]["classified"]["price"] == ""
            else details_json[0]["classified"]["price"]
        )
        property_details["TransactionType"] = (
            None
            if details_json[0]["classified"]["transactionType"] == ""
            else details_json[0]["classified"]["transactionType"]
        )
        property_details["No_of_rooms"] = (
            None
            if details_json[0]["classified"]["bedroom"]["count"] == ""
            else details_json[0]["classified"]["bedroom"]["count"]
        )
        property_details["Kitchen"] = (
            0 if details_json[0]["classified"]["kitchen"]["type"] == "" else 1
        )
        property_details["IsFurnished"] = 1 if isFurnished == "true" else 0
        property_details["Fireplace_exist"] = 1 if fireplace_exist == "true" else 0
        property_details["Garden"] = (
            1
            if len(details_json[0]["classified"]["outdoor"]["garden"]["surface"]) != 0
            else 0
        )
        property_details["Terrace"] = (
            1
            if details_json[0]["classified"]["outdoor"]["terrace"]["exists"] == "true"
            else 0
        )
        property_details["Surface_area"] = (
            None
            if details_json[0]["classified"]["land"]["surface"] == ""
            else details_json[0]["classified"]["land"]["surface"] + "m2"
        )
        property_details["Living_area"] = None if living_area == "" else living_area + "m2"
        property_details["Facade_count"] = None if facade_count == "" else facade_count
        property_details["Swimming_pool"] = (
            0
            if details_json[0]["classified"]["wellnessEquipment"]["hasSwimmingPool"]
               == ""
            else 1
        )
        property_details["State_of_building"] = (
            None
            if details_json[0]["classified"]["building"]["condition"] == ""
            else details_json[0]["classified"]["building"]["condition"]
        )

    list_of_properties.append(property_details) # To append all the data of every property in the list

    driver.quit() # To quit the driver after scrapping ends
    print("pageno.= ", i) # To print the page number of the page scrapped


    ''' Creating datasets from the list of Properties'''

    data = list_of_properties
    df = pd.DataFrame(data)
    df.replace('', None, inplace=True)


    '''Saving datasets to CSV file'''

    df.to_csv('property_data_2.csv', mode='a', header=None, index=False)
