from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import pandas as pd

for i in range(1, 334):  # by the help of this loop we can reach all the pages
    page_num = str(i) + "&orderBy=relevance"
    url = (
        "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page=" + page_num
    )
    list_of_properties = []

    time.sleep(
        2
    )  # this sleep line can help us to give a break before reach each the pages
    driver = webdriver.Chrome(executable_path="driver/chromedriver")

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    listings = soup.find_all(
        "a", class_="card__title-link"
    )  # listing help us to find all web pages
    for pages in listings:

        property_details = {}
        driver.get(pages["href"])
        property_details_page = BeautifulSoup(driver.page_source, "html.parser")

        script_list = property_details_page.find_all("script")

        details_json = ""
        for script in script_list:
            if "window.dataLayer" in str(script):
                script_content = str(script)
                details_json = json.loads(
                    script_content[
                        script_content.index("[") : script_content.index("]") + 1
                    ]
                )

            if "window.classified" in str(script):
                script_content = str(script)
                facade_count = ""
                fireplace_exist = ""
                isFurnished = ""
                living_area = ""
                if '"facadeCount":' in script_content:
                    facade_count = script_content.split('"facadeCount":')[1][
                        :2
                    ].replace(",", "")
                if '"fireplaceExists":' in script_content:
                    fireplace_exist = script_content.split('"fireplaceExists":')[1][
                        :5
                    ].replace(",", "")
                if '"isFurnished":' in script_content:
                    isFurnished = script_content.split('"isFurnished":')[1][:5].replace(
                        ",", ""
                    )
                if '"netHabitableSurface"' in script_content:
                    living_area = (
                        script_content.split('"netHabitableSurface":')[1]
                    ).split(",")[0]


        """ first we take a specific html element that has the text of the locality
            and then we filter all the empty spaces and lines. That data is assigned into our property dataframe"""

        element_locality = (
            property_details_page.find(
                "span", class_="classified__information--address-row"
            )
            .text.replace("\n", "")
            .strip()
            .replace("           ", "  ")
        )

        """ if the value of the locality is empty on json then we are going to assign it as a None value otherwise it will copy the actual value
            and this is the way we filter all the other attributes of our dataframe"""
        property_details["locality"] = (
            None if element_locality == "" else element_locality
        )
        
        property_details["type_of_property"] = (
            None
            if details_json[0]["classified"]["type"] == ""
            else details_json[0]["classified"]["type"]
        )
        property_details["subtype_of_property"] = (
            None
            if details_json[0]["classified"]["subtype"] == ""
            else details_json[0]["classified"]["subtype"]
        )
        property_details["price"] = (
            None
            if details_json[0]["classified"]["price"] == ""
            else details_json[0]["classified"]["price"]
        )
        property_details["transactionType"] = (
            None
            if details_json[0]["classified"]["transactionType"] == ""
            else details_json[0]["classified"]["transactionType"]
        )
        property_details["no_of_rooms"] = (
            None
            if details_json[0]["classified"]["bedroom"]["count"] == ""
            else details_json[0]["classified"]["bedroom"]["count"]
        )
        property_details["kitchen"] = (
            0 if details_json[0]["classified"]["kitchen"]["type"] == "" else 1
        )
        property_details["isFurnished"] = 1 if isFurnished == "true" else 0
        property_details["fireplace_exist"] = 1 if fireplace_exist == "true" else 0
        property_details["garden"] = (
            1
            if len(details_json[0]["classified"]["outdoor"]["garden"]["surface"]) != 0
            else 0
        )
        property_details["terrace"] = (
            1
            if details_json[0]["classified"]["outdoor"]["terrace"]["exists"] == "true"
            else 0
        )
        property_details["surface_area"] = (
            None
            if details_json[0]["classified"]["land"]["surface"] == ""
            else details_json[0]["classified"]["land"]["surface"] + "m2"
        )
        property_details["area"] = None if living_area == "" else living_area + "m2"
        property_details["facade_count"] = None if facade_count == "" else facade_count
        property_details["swimming_pool"] = (
            0
            if details_json[0]["classified"]["wellnessEquipment"]["hasSwimmingPool"]
            == ""
            else 1
        )
        property_details["state_of_building"] = (
            None
            if details_json[0]["classified"]["building"]["condition"] == ""
            else details_json[0]["classified"]["building"]["condition"]
        )


        """ we are going to append the specific details of a property into the lists of properties"""
        list_of_properties.append(property_details)

    driver.quit()
    print("pageno.= ", i)

    """ we are going to connvert it into dataframe """

    data = list_of_properties
    df = pd.DataFrame(data)
    df.replace("", None, inplace=True)

    """Saving the dataframe into a CSV file
        We specify mode (append) so the data will be appended into the csv file for every webpage we scrape"""

    df.to_csv("property_data.csv", mode="a", header=None, index=False)