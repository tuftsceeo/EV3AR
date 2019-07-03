# Dan McGinn, Tufts CEEO
# Run with python3

from http.server import BaseHTTPRequestHandler, HTTPServer # package for Webserver
from urllib.parse import unquote # package for decoding UTF-8
import getpass, sys, socket, os, webbrowser
from time import sleep
import requests,json # packages for Thingworx POST & GET
import sys,select,termios # packages for Keyboard Inputs
import ev3dev.ev3 as ev3 # package for EV3 Commands

# Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')
speed = 20 # Set Speed
direc = 'Stop'

pageContent = open('ARDemo.html').read()%('50','')+open('styleSheet.html').read()

# Read Demo Page
def setPageContent(distance,speed):
    global pageContent
    DistStr = 'Distance to Obstruction:'+str(distance)
    pageContent = open('ARDemo.html').read()%(str(speed),DistStr)+open('styleSheet.html').read()
    return pageContent

# Get IP Address
ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
s.close()

# Set host port
host_port = 8000

# Thingworx info
with open('appkey.txt', 'r') as file:
    appkey = file.read()
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': appkey,
        'Accept': "application/json",
        'Content-Type': "application/json"
        }
propName ="cone"

# Post property value to thingworx
def thingworxPOST(propName,value):
    propValue = {propName: value}
    requests.request("PUT",url+'*',headers=headers,json=propValue)

# Get property value to thingworx and validate value was posted
def thingworxGET(propName,value):
    propValue = {propName: value}
    getResponse=requests.request("GET",url+propName,headers=headers)
    parsed_json = json.loads(getResponse.text)
    dist = (parsed_json['rows'][0][propName])
    if float(value) == dist:
        print("Property Value Updated")
    else:
        print('Property Value Not Updated')

# Motor commands
def forward(speed):
   motor_left.run_direct(duty_cycle_sp=speed)
   motor_right.run_direct(duty_cycle_sp=speed)
def left(speed):
   motor_left.run_direct( duty_cycle_sp=-speed)
   motor_right.run_direct( duty_cycle_sp=speed)
def right(speed):
   motor_left.run_direct( duty_cycle_sp=speed)
   motor_right.run_direct( duty_cycle_sp=-speed)
def back(speed):
   motor_left.run_direct(duty_cycle_sp=-speed)
   motor_right.run_direct(duty_cycle_sp=-speed)
def stop(speed):
   motor_left.run_direct( duty_cycle_sp=0)
   motor_right.run_direct( duty_cycle_sp=-0)

def setSpeed(NewSpeed):
   global speed
   speed = int(NewSpeed)
   return speed

def drive(direc,speed):
    if direc == 'Forward':
        forward(speed)
    elif direc == 'Backward':
        back(speed)
    elif direc == 'Left':
        left(speed)
    elif direc == 'Right':
        right(speed)
    elif direc == 'Stop':
        stop(speed)

# Define settings for Ultrasonic Sensor
us = ev3.UltrasonicSensor() # Connect ultrasonic sensor to any sensor port
us.mode='US-DIST-CM' # Put the US sensor into distance mode.
units = us.units # reports 'cm' even though the sensor measures 'mm'

# Get distance from Ultrasonic Sensor
def getDist():
    return us.value()/10  # convert mm to cm

# LED commands
def green():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
def yellow():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
def red():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)

# Webserver
class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self,pageContent):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        global pageContent
        self.do_HEAD(pageContent)
        self.wfile.write(pageContent.encode("utf-8"))

    def do_POST(self):
        global pageContent, speed, direc
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        print(post_data)
        if 'Fwd' in post_data:
            direc = 'Forward'
        if 'Left' in post_data:
            direc = 'Left'
        if 'Right' in post_data:
            direc = 'Right'
        if 'Bkwd' in post_data:
            direc = 'Backward'
        if 'Stop' in post_data:
            direc = 'Stop'
        if 'Speed' in post_data:
            setSpeed(post_data.split("=")[1])
        if 'Green' in post_data:
            green()
        if 'Yellow' in post_data:
            yellow()
        if 'Red' in post_data:
            red()
        drive(direc,int(speed))
        distance = getDist()
        setPageContent(distance,speed)
        thingworxPOST('cone',distance)
        # thingworxGET('cone',distance) #Uncomment for Debugging, Slows Code
        self._redirect('/')  # Redirect back to the root url
        return pageContent, speed, direc

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
