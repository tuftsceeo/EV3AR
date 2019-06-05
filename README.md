## Drive an EV3 with an Ultrasonic sensor

# Designed by Daniel McGinn in Summer 2019 at the Tufts CEEO

This code was created to dirve an EV3 running <a href="https://www.ev3dev.org/">ev3dev</a>, a Debian Linux-based operating system, while recording the distance measured by an ultrasonic sensor. The sensor data is pushed to Thingworx in order to create an AR expereince for visualizing sensor data.

To install the requests library for python3 use ```sudo apt-get install python3-requests```

To get the MAC address & IP Address use ```sudo ifconfig```