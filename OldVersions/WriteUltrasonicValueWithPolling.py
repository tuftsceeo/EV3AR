import ev3dev.ev3 as ev3
from time import sleep
import requests,json
global isWindows

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

# Record Keyboard Inputs with Polling Refactored from https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal
isWindows = False
try:
    from win32api import STD_INPUT_HANDLE
    from win32console import GetStdHandle, KEY_EVENT, ENABLE_ECHO_INPUT, ENABLE_LINE_INPUT, ENABLE_PROCESSED_INPUT
    isWindows = True
except ImportError as e:
    import sys
    import select
    import termios
class KeyPoller():
    def __enter__(self):
        global isWindows
        if isWindows:
            self.readHandle = GetStdHandle(STD_INPUT_HANDLE)
            self.readHandle.SetConsoleMode(ENABLE_LINE_INPUT|ENABLE_ECHO_INPUT|ENABLE_PROCESSED_INPUT)

            self.curEventLength = 0
            self.curKeysLength = 0

            self.capturedChars = []
        else:
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)

            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        if isWindows:
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def poll(self):
        if isWindows:
            if not len(self.capturedChars) == 0:
                return self.capturedChars.pop(0)

            eventsPeek = self.readHandle.PeekConsoleInput(10000)

            if len(eventsPeek) == 0:
                return None

            if not len(eventsPeek) == self.curEventLength:
                for curEvent in eventsPeek[self.curEventLength:]:
                    if curEvent.EventType == KEY_EVENT:
                        if ord(curEvent.Char) == 0 or not curEvent.KeyDown:
                            pass
                        else:
                            curChar = str(curEvent.Char)
                            self.capturedChars.append(curChar)
                self.curEventLength = len(eventsPeek)

            if not len(self.capturedChars) == 0:
                return self.capturedChars.pop(0)
            else:
                return None
        else:
            dr,dw,de = select.select([sys.stdin], [], [], 0)
            if not dr == []:
                return sys.stdin.read(1)
            return None

# get distance from Ultrasonic Sensor
def getDist():
    return us.value()/10  # convert mm to cm

# Post variable value to thingworx
def thingworxPOST(value):
    propValue = {propName: value}
    requests.request("PUT",url+'*',headers=headers,json=propValue)
    
def thingworxGET(value): # Get (validate value was posted)
    propValue = {propName: value}
    getResponse=requests.request("GET",url+propName,headers=headers)
    parsed_json = json.loads(getResponse.text)
    dist = (parsed_json['rows'][0]['cone'])
    if float(value) == dist:
        print("Property Value Updated")
    else:
        print('Property Value Not Updated')

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
            stop()
            print("Stopped due to proximity to obstruction")
        thingworxPOST(distance)
#        thingworxGET(distance) #Uncomment for Debugging, Slows Code
        c = keyPoller.poll()
        if not c is None:
            if c == 'w':
                forward()
                print("Forward")
            if c == 's':
                back()
                print("Backward")
            if c == 'a':
                left()
                print("Left")
            if c == 'd':
                right()
                print("Right")
            if c == ' ':
                stop()
                print("Stop")
            if c == 'q':
                print("-------------------EXIT-------------------")
                break