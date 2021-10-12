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
        
        property_details ={}
        driver.get(pages["href"])
        property_details_page= BeautifulSoup(driver.page_source, "html.parser")
        
        price = property_details_page.find_all("script")
        
        details_json=''
        for script in price:
            if "window.dataLayer" in str(script):
                script_content= str(script)
                details_json= json.loads(script_content[script_content.index('['): script_content.index(']')+1])

            # if "window.classified" in str(script):
            #     script_content= str(script)
            #     details_string = eval(script_content[script_content.index('"facadeCount": '): script_content.index('"facadeCount": ')+2])
            #     # details_string.replace(";", "")
            #     # details_json = eval(details_string.replace(";", ""))
            #     print(details_string)
        
        property_details['type_of_property']= details_json[0]['classified']['type']
        property_details['subtype_of_property']= details_json[0]['classified']['subtype']
        property_details['price']=details_json[0]['classified']['price']
        # property_details['transactionType']= details_json[0]['classified']['transactionType']
        property_details['no_of_rooms']=details_json[0]['classified']['bedroom']['count']
        property_details['kitchen'] = details_json[0]['classified']['kitchen']['type']
        property_details['surface_area']= details_json[0]['classified']['land']['surface']
        property_details['swimming_pool']= details_json[0]['classified']['wellnessEquipment']['hasSwimmingPool']  
        property_details['state_of_building']= details_json[0]['classified']['building']['condition']
        
        list_of_properties.append(property_details)
        
    driver.quit()
print(list_of_properties)

    # Creating Dataframes from the list of Dictionaries

data = list_of_properties
df = pd.DataFrame(data)
# print(df)

# Moving the index to 1

df.index += 1


# Saving dictionary list dataframes to CSV file

df.to_csv('Demo.csv')
