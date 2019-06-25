# Dan McGinn
# Designed at Tufts CEEO for Demo at LiveWorx
# Run with Python3
# Working Version EOB 6/5/19

import signal,sys,termios,tty
import ev3dev.ev3 as ev3
from time import sleep
import requests,json

# Define settings for Ultrasonic Sensor
us = ev3.UltrasonicSensor() # Connect ultrasonic sensor to any sensor port
us.mode='US-DIST-CM' # Put the US sensor into distance mode.
units = us.units # reports 'cm' even though the sensor measures 'mm'

# Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')
speed = 25 # Set Speed

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

# Timeout class for use in Getch
class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
    def __init__(self, sec):
        self.sec = sec
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

# keybaord inputs fnc
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        with Timeout(1):
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
    except Timeout.Timeout:
        ch=''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# get distance from Ultrasonic Sensor
def getDist():
    return us.value()/10  # convert mm to cm

# Post variable value to thingworx
def thingworxPOST(value):
    propValue = {propName: value}
    requests.request("PUT",url+'*',headers=headers,json=propValue)

def changeSpeed(action):
    if action == "fast":
        speed = speed + 5
        print("speed: %s" % (speed))
    elif action == "slow":
        speed = speed - 5
        print("speed: %s" % (speed))
    return speed

# motor commands
def forward():
   motor_left.run_direct(duty_cycle_sp=speed)
   motor_right.run_direct(duty_cycle_sp=speed)
def back():
   motor_left.run_direct(duty_cycle_sp=-speed)
   motor_right.run_direct(duty_cycle_sp=-speed)
def left():
   motor_left.run_direct( duty_cycle_sp=-speed)
   motor_right.run_direct( duty_cycle_sp=speed)
def right():
   motor_left.run_direct( duty_cycle_sp=speed)
   motor_right.run_direct( duty_cycle_sp=-speed)
def stop():
   motor_left.run_direct( duty_cycle_sp=0)
   motor_right.run_direct( duty_cycle_sp=-0)
# LED commands
def red():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
    sleep(0.01)
def orange():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
    sleep(0.01)
def yellow():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
    sleep(0.01)
def green():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    sleep(0.01)

print("-----------Connection Initiated-----------")
while True:
   char = getch()
   distance = getDist()
   thingworxPOST(distance)
   if distance < 50:  #show red LEDs for distance under 50 cm
      red()
   if distance > 50:  #show green LEDs for distance over 50 cm
      green()
   if char == 'w':
      forward()
      print("Forward")
   if char == 's':
      back()
      print("Backward")
   if char == 'a':
      left()
      print("Left")
   if char == 'd':
      right()
      print("Right")
   if char == ' ':
      stop()
   if char == '^[[A': # Up arrow
      changeSpeed(fast)
   if char == '^[[B': # Down arrow
      changeSpeed(slow)
   if char == 'q':
      print("-------------------EXIT-------------------")
      sleep(0.01)
      stop()
      ev3.Leds.all_off()
      exit()