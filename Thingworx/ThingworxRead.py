import requests
import json

# Info
with open('appkey.txt', 'r') as file:
    appkey = file.read()
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': appkey,
        'Accept': "application/json",
        'Content-Type': "application/json"
        }
propName =raw_input("Enter Property: ")

# Get
getResponse=requests.request("GET",url+propName,headers=headers)
parsed_json = json.loads(getResponse.text)
print(('Property Value: ')+(parsed_json['rows'][0][propName]))
