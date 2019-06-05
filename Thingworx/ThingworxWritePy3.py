import requests
import json

# Info
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': "f76e9513-0bbc-4b33-af7f-09e5ea959504",
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
value = set(parsed_json['rows'][0][propName])
if set(parsed_json['rows'][0][propName]) == set(value):
	print('Property Value Updated')
else:
	print('Property Value Not Updated')
