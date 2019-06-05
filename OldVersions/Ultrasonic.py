import ev3dev.ev3 as ev3

# Connect ultrasonic and touch sensors to any sensor port
us = ev3.UltrasonicSensor() 
ts = ev3.TouchSensor()

# Put the US sensor into distance mode.
us.mode='US-DIST-CM'

units = us.units
# reports 'cm' even though the sensor measures 'mm'

while not ts.value():    # Stop program by pressing touch sensor button
    # US sensor will measure distance to the closest
    # object in front of it.
    distance = us.value()/10  # convert mm to cm
    print(str(distance) + " " + units)

    if distance < 60:  #This is an inconveniently large distance
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
    else:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

#ev3.Sound.beep()       
ev3.Leds.set_color(Leds.LEFT, Leds.GREEN)  #set left led green before exiting