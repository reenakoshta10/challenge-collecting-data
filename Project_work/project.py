import pandas as pd
import numpy as np
import random

# List of dictionaries with housing data

list_of_housing_data = []
for i in range(10000):
    area = random.randint(130, 250)
    sleeping_room = random.randint(2, 5)
    property_type = ""
    random_house_price = random.randint(0, 1000000)
    random_property = random.randint(0, 2)
    if np.trunc(random_property) == 0:
        property_type = "house"
    else:
        property_type = "apartment"
    housing_data = {"property_type": property_type,
                    "price": random_house_price,
                    "sleeping_rooms": sleeping_room,
                    "area": str(area)+"m2"}
    list_of_housing_data.append(housing_data)
print(list_of_housing_data)

# Creating Dataframes from the list of Dictionaries

data = list_of_housing_data
df = pd.DataFrame(data)
print(df)

# Moving the index to 1

df.index += 1


# Saving dictionary list dataframes to CSV file

df.to_csv('Demo.csv')
