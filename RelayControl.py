# SAMS - Smart Apiculture Management Services
# RelayControl.py is a function for the SAMS Control Unit framework to control the relay powering in cascades
#
# This software is open source.
#
#!/usr/bin/python
#
#from numpy import array as arr
import RPi.GPIO as GPIO
import time

# init scheme to BCM
GPIO.setmode(GPIO.BCM)


# init list with GPIO pin numbers as they are connected to the RPi
pinList= [ 5, 12, 6, 7, 13, 25, 19, 24, 26, 23, 21, 18, 20, 15, 16]
pinGSM = 22

# The array portsActive is set by the user control surface and
# saved on the local storage so it will not get lost when reboot.
#portsActive = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# using the portsActive to filter unoccupied Relay Ports
#pinList = pinList*portsActive
#pinList = pinList[pinList != 0]


# loop through all monitor units (MU) and GSM pins and set mode and state to
GPIO.setup(pinGSM,GPIO.OUT)
GPIO.setup(pinGSM,GPIO.HIGH)

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

GPIO.cleanup()

# time to sleep between operations in the main loop
MU_duration  = .3 # This is seconds and will be 300 (5 min)
GSM_forerun  = 2 # This is the time the GSM/WiFi is powered before the cascade starts (10 sec?)

# Power up GSM
GPIO.output(pinGSM, GPIO.LOW)
print("GSM powered.")
time.sleep(GSM_forerun)

# Start powering in cascades
try:
    for i in pinList:
        print(i)
        GPIO.output(i,GPIO.LOW)
        time.sleep(MU_duration)
        GPIO.output(i,GPIO.HIGH)

    GPIO.output(pinGSM,GPIO.HIGH)
    GPIO.cleanup()

# End program cleanly with keyboard
except KeyboardInterrupt:
    print("Break (User requested)")
    # Reset GPIO settings
    GPIO.cleanup()