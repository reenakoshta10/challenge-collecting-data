import requests
from bs4 import BeautifulSoup
import json 
import pandas as pd

url = "https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&orderBy=newest"

resp = requests.get(url)
soup = BeautifulSoup(resp.content, "lxml")
page_results = soup.find('iw-search')
# page_attributes = page_results.attrs
res = json.loads(page_results.attrs[':results'])

id = json.loads(page_results.attrs[':unique-id'])
print("id= ", id)
content1 = json.dumps(res, indent = 4)
content = json.dumps(res, indent = 4)
print(content)
print(content1)