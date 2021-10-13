import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import pandas as pd
from threading import Thread

# class ThreadFunction(Thread):
#     def __init__(self, name, url):
#         Thread.__init__(self)
#         self.name = name
#         self.url = url

#     def run(self):
        
        # print(f"Thread {self.name}: finishing")


for i in range(2, 3):
    page_num = str(i) + "&orderBy=relevance"
    url = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
    list_of_properties = []

        # print(f"Thread {self.name}: starting")
    time.sleep(2)
    driver = webdriver.Chrome(executable_path="driver/chromedriver")
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all("a", class_="card__title-link")
    for pages in listings:
            
        property_details ={}
        driver.get(pages["href"])
        property_details_page= BeautifulSoup(driver.page_source, "html.parser")
            
        script_list = property_details_page.find_all("script")
            
        details_json=''
        for script in script_list:
            if "window.dataLayer" in str(script):
                script_content= str(script)
                details_json= json.loads(script_content[script_content.index('['): script_content.index(']')+1])

            if "window.classified" in str(script):
                script_content= str(script)
                facade_count =''
                # if '"facadeCount":' in script_content:
                #     facade_count = script_content.split('"facadeCount":')[1][:2].replace(",", "")
                if '"fireplaceExists":' in script_content:
                    fireplace_exist = script_content.split('"fireplaceExists":')[1][:5].replace(",", "")
                if '"isFurnished":' in script_content:
                    isFurnished = script_content.split('"isFurnished":')[1][:5].replace(",", "")

                    
                    
                    # print(facade_count,fireplace_exist,isFurnished)
            
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
        property_details['isFurnished'] = 1 if isFurnished == "true" else 0
        property_details['fireplace_exist'] = 1 if fireplace_exist=="true" else 0
        property_details['garden'] = 1 if len(details_json[0]['classified']['outdoor']['garden']['surface']) != 0 else 0
        property_details['terrace'] = 1 if details_json[0]['classified']['outdoor']['terrace']['exists']=="true" else 0
        property_details['surface_area'] = None if details_json[0]['classified']['land']['surface'] == "" else details_json[0]['classified']['land']['surface']
        property_details['facade_count'] = None if facade_count == '' else facade_count
        property_details['swimming_pool'] = 0 if details_json[0]['classified']['wellnessEquipment']['hasSwimmingPool']=="" else 1
        property_details['state_of_building'] = None if details_json[0]['classified']['building']['condition']=="" else details_json[0]['classified']['building']['condition']

        list_of_properties.append(property_details)
    driver.quit()
            # Creating Dataframes from the list of Dictionaries

    data = list_of_properties
    df = pd.DataFrame(data)
    df.replace('', None, inplace=True) 
        # print(df)

        # Moving the index to 1

        # df.index = index
        # index += 1


        # Saving dictionary list dataframes to CSV file

    df.to_csv('IMMOWEB_property_data.csv', mode='a', header=None,index=False)
    # thread = ThreadFunction(i, url)
    # thread.start()
    
# print(list_of_properties)


