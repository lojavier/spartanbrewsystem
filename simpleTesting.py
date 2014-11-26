pi@raspberrypi ~/Desktop $ cd pi_testing/
pi@raspberrypi ~/Desktop/pi_testing $ sudo python simpleTesting.py
Program Initialize
Beginning Cooling Stage
Cooling Done
pi@raspberrypi ~/Desktop/pi_testing $ sudo nano simpleTesting.py
  GNU nano 2.2.6                 File: simpleTesting.py

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Set up appropriate GPIOs (Heater, Cooling, Solenoid)
heater = 13
cooling = 6
solenoid = 5

GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)

print("Program Initialize")
time.sleep(15)
print("Beginning Cooling Stage")
GPIO.output(cooling, GPIO.HIGH) #Activates Cooler
time.sleep(15)
GPIO.output(cooling, GPIO.LOW) #Re-activates
print("Cooling Done")
time.sleep(15)
