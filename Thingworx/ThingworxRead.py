import requests
import json

# Info
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': "f76e9513-0bbc-4b33-af7f-09e5ea959504",
        'Accept': "application/json",
        'Content-Type': "application/json"
        }
propName =raw_input("Enter Property: ")

# Get
getResponse=requests.request("GET",url+propName,headers=headers)
parsed_json = json.loads(getResponse.text)
print(('Property Value: ')+(parsed_json['rows'][0][propName]))
