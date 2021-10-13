import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd


list_of_properties = []
for i in range(1, 2):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
    driver = webdriver.Chrome(executable_path="driver/chromedriver")
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
                details_json = json.loads(script_content[script_content.index('['): script_content.index(']')+1])

            # if "window.classified" in str(script):
            #     script_content= str(script)
            #     details_string = eval(script_content[script_content.index('"facadeCount": '): script_content.index('"facadeCount": ')+2])
            #     # details_string.replace(";", "")
            #     # details_json = eval(details_string.replace(";", ""))
            #     print(details_string)
        
        property_details['Type_of_property'] = details_json[0]['classified']['type']

        property_details['Subtype_of_propertyubtype_of_property'] = details_json[0]['classified']['subtype']

        property_details['Price(in Euros)'] = details_json[0]['classified']['price']

        # property_details['transactionType']= details_json[0]['classified']['transactionType']

        property_details['No_of_rooms'] = details_json[0]['classified']['bedroom']['count']

        if property_details['No_of_rooms'] == '':
            property_details['No_of_rooms'] = 'Varies'

        property_details['Kitchen'] = details_json[0]['classified']['kitchen']['type']
        if property_details['Kitchen'] == '':
            property_details['Kitchen'] = 0
        else:
            property_details['Kitchen'] = 1

        property_details['Surface_area'] = details_json[0]['classified']['land']['surface']
        if property_details['Surface_area'] == '':
            property_details['Surface_area'] = 'Varies'

        property_details['Terrace'] = details_json[0]['classified']['outdoor']['terrace']['exists']
        if property_details['Terrace'] == '':
            property_details['Terrace'] = 'No'
        else:
            property_details['Terrace'] = 'Yes'

        property_details['Garden'] = details_json[0]['classified']['outdoor']['garden']['surface']
        if property_details['Garden'] == '':
            property_details['Garden'] = 'No/Varies'
        else:
            property_details['Garden'] = 'Yes'

        property_details['Swimming_pool'] = details_json[0]['classified']['wellnessEquipment']['hasSwimmingPool']
        if property_details['Swimming_pool'] == '':
            property_details['Swimming_pool'] = 'No/Not specified'
        else:
            property_details['Swimming_pool'] = 'Yes'

        property_details['State_of_building'] = details_json[0]['classified']['building']['condition']
        if property_details['State_of_building'] == '':
            property_details['State_of_building'] = 'as new'
        
        list_of_properties.append(property_details)
        
    driver.quit()
print(list_of_properties)

# Creating datasets  from the list of properties

data = list_of_properties
df = pd.DataFrame(data)
# print(df)

# Moving the index to 1

df.index += 1


# Saving datasets to CSV file

df.to_csv('Collecting_Data.csv')