from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
token = os.environ["HUD_ACCESS_TOKEN"]
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "https://www.huduser.gov/hudapi/public/fmr/listMetroAreas",
    headers=headers
)

print(response.status_code)
data = response.json()

# for area in data:
#     if("Dallas" in area["area_name"]):
#        print(area)

#use METRO19100M19100 cause that is dallas we now get all the zipcodes from that place

response2 = requests.get(
    "https://www.huduser.gov/hudapi/public/fmr/data/METRO19100M19100",
    headers = headers   
)

data_area = response2.json()

print(data_area)


for cool in data_area['data']['basicdata']:
    print(cool)


