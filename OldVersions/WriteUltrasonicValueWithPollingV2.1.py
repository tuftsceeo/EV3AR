# Dan McGinn, Tufts CEEO

import ev3dev.ev3 as ev3 # For EV3 Commands
from time import sleep
import requests,json # For Thingworx POST & GET
import sys,select,termios # For Keyboard Inputs

# Define settings for Ultrasonic Sensor
us = ev3.UltrasonicSensor() # Connect ultrasonic sensor to any sensor port
us.mode='US-DIST-CM' # Put the US sensor into distance mode.
units = us.units # reports 'cm' even though the sensor measures 'mm'

#Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')
speed = 25 # Set Speed

# Thingworx info
url = "http://pp-1804271345f2.portal.ptc.io:8080/Thingworx/Things/CEEO_Summer_2019/Properties/"
headers = {
        'appKey': "f76e9513-0bbc-4b33-af7f-09e5ea959504",
        'Accept': "application/json",
        'Content-Type': "application/json"
        }
propName ="cone"

# Record Keyboard Inputs with Polling 
class KeyPoller():
    # Refactored from https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal
    def __enter__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)
        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        dr,dw,de = select.select([sys.stdin], [], [], 0)
        if not dr == []:
            return sys.stdin.read(1)
        return None
# Get distance from Ultrasonic Sensor
def getDist():
    return us.value()/10  # convert mm to cm
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
def setSpeed(action):
    global speed
    if action == 'fast' and speed < 100:
        speed = speed+5
    elif action == 'slow' and speed >= 0:
        speed = speed-5
    return updateSpeed = True
    return speed
def drive(direc,speed):
    if direc == 'Forward':
        forward()
    elif direc == 'Backward':
        back()
    elif direc == 'Left'
        left()
    elif direc == 'Right'
        right()
    elif direc == 'Stop'
        stop()
    print("Moving %s at speed %d" % (direc,speed))
# LED commands
def red():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
def orange():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
def yellow():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
def green():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
# Sound commands
def beep():
    ev3.Sound.beep()
# Run the EV3 
def Run():
    direc = 'stop'
    print("-----------Connection Initiated-----------")
    with KeyPoller() as keyPoller:
        while True:
            distance = getDist()
            print("US Distance: %s cm" % (distance))
            if distance > 50:
                green()
            elif distance <= 50 and distance >= 10:
                yellow()
            elif distance < 10:
                red()
                beep()
                stop()
                print("Stopped due to proximity to obstruction")
            thingworxPOST('cone',distance)
            # thingworxGET('cone',distance) #Uncomment for Debugging, Slows Code
            c = keyPoller.poll()
            if not c is None:
                if c == 'w':
                    direc = 'Forward'
                elif c == 's':
                    direc = 'Backward'
                elif c == 'a':
                    direc = 'Left'
                elif c == 'd':
                    direc = 'Right'
                elif c == ' ':
                    direc = 'Stop'
                elif c == 'q':
                    print("-------------------EXIT-------------------")
                    break
                elif c == 'b':
                    beep()
                    print("Beep")
                elif c == 'o':
                    setSpeed('fast')
                    print("Speed: %s" % (speed))
                elif c == 'l':
                    setSpeed('slow')
                    print("Speed: %s" % (speed))
                drive(direc,speed)
if __name__ == '__main__':
    Run()
