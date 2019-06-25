import requests
import json
import re

# Info
with open('appkey.txt', 'r') as file:
    appkey = file.read()
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': appkey,
        'Accept': "application/json",
        'Content-Type': "application/json"
        }
propName =input("Enter Property: ")
value=input("Enter Value: ")
propValue = {propName: value}

# Put
requests.request("PUT",url+'*',headers=headers,json=propValue)

# Get (validate value was posted)
getResponse=requests.request("GET",url+propName,headers=headers)
parsed_json = json.loads(getResponse.text)
dist = (parsed_json['rows'][0]['cone'])
if float(value) == dist:
	print("Property Value Updated")
else:
	print('Property Value Not Updated')
