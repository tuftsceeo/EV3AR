# Dive an EV3 while projecting the data collected by and Ultrasonic sensor in AR (powered by Vuforia Studio)

## Designed by Daniel McGinn in Summer 2019 at the Tufts CEEO

This code was created to drive an EV3 running <a href="https://www.ev3dev.org/">ev3dev</a>, a Debian Linux-based operating system, while recording the distance measured by an ultrasonic sensor. The sensor data is pushed to Thingworx in order to create an AR experience for visualizing sensor data.

SSH into the EV3 ```ssh robot@<EV3 IP Address>``` and run the most recent version of the code on the EV3 with Python 3

To install the libraries for Python 3 used in this project run ```sudo apt-get install python3-<package name>``` on the EV3
The required packages are:
* ev3dev
* requests
* termios

To get the MAC address & IP Address use ```sudo ifconfig```

The Vuforia AR Experience is designed separately