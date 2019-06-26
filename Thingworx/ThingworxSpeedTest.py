import requests
import json
import time

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
t0 = time.time()
# Put
requests.request("PUT",url+'*',headers=headers,json=propValue)
t1 = time.time()
# Get (validate value was posted)
getResponse=requests.request("GET",url+propName,headers=headers)
parsed_json = json.loads(getResponse.text)
value = set(parsed_json['rows'][0][propName])
if set(parsed_json['rows'][0][propName]) == set(value):
	print('Property Value Updated')
else:
	print('Property Value Not Updated')
t2 = time.time()

PUT_time = t1-t0
GET_time = t2-t1

print('PUT_time: %f seconds\nGET_time: %f seconds' % (PUT_time,GET_time))