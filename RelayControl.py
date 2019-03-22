# SAMS - Smart Apiculture Management Services
# RelayControl.py is a function for the SAMS Control Unit framework to control the relay powering in cascades
#
# This software is open source.
#
# !/usr/bin/python
#
# from numpy import array as arr
import RPi.GPIO as GPIO
import time

# time to sleep  (in seconds) between operations in the main loop
MU_duration = 5
#540
GSM_forerun = 2
#120

# init scheme to BCM
GPIO.setmode(GPIO.BCM)

# init list with GPIO pin numbers as they are connected to the RPi
# pinList= [5, 12, 6, 7, 13, 25, 19, 24, 26, 23, 21, 18, 20, 15, 16]
# Prototype GPIO pin numbers:
pinList = [5, 6]
#pinGyver = [13, 19]
pinGSM = 22

# The array portsActive is set by the user control surface and
# saved on the local storage so it will not get lost when reboot.
# portsActive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# using the portsActive to filter unoccupied Relay Ports
# pinList = pinList*portsActive
# pinList = pinList[pinList != 0]

# loop through both gyver pins to activate reference pins (5V + GND) and wait 1 second before starting actual script
#for i in pinGyver:
#    GPIO.setup(i,GPIO.OUT)
#    GPIO.output(i,GPIO.LOW)
#time.sleep(1)


# loop through all monitor units (MU) and GSM pins and set mode and state to
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)

GPIO.setup(pinGSM, GPIO.OUT)
GPIO.output(pinGSM, GPIO.LOW)

# Power up GSM
GPIO.output(pinGSM, GPIO.HIGH)
print("GSM powered. RUnning cascades now...")
time.sleep(GSM_forerun)

# Start powering in cascades
try:
    for i in pinList:
        GPIO.output(i, GPIO.HIGH)
        time.sleep(MU_duration)
        GPIO.output(i, GPIO.LOW)

    GPIO.output(pinGSM, GPIO.LOW)
    GPIO.cleanup()

# End program cleanly with keyboard
except KeyboardInterrupt:
    print("Break (User requested)")
    # Reset GPIO settings
    GPIO.cleanup()