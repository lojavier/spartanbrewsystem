# Blonde Brewing Sample Program?

# Initialization
# Set up appropriate GPIOs (Heater, Cooling, Solenoid)
def initialize(GPIOpin):
    GPIO.setup(GPIOpin, GPIO.OUT)
    GPIO.output(GPIOpin, GPIO.HIGH)

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

heater = 13
cooling = 6
solenoid = 5

initialize(heater)
initialize(cooling)
initialize(solenoid)

# Set up clock/timer?
import time

# This function is a template for the output prints. Code Re-Use
def printInstruction(instruction):
    print("Add {} to the pot." .format(instruction))
    acknowledgement = raw_input("Did you add {}? (y/n) " .format(instruction))
    # update flag on database
    while acknowledgement != 'y':
        acknowledgement = raw_input("Did you add the {}? (y/n) " .format(instruction))

# This function heats the liquid.
# Input Parameters: Temperature you want to reach, and time?
# This function will check temperature, time, activate gpio when appropriate.
def heatControl():
        print("HEAT!")

# This function cools the liquid.
# Input Parameter: Temperature you want to reach, time limit?
# This function will check temperature, time, activate gpio when appropriate.
def coolingControl():
        print("COOL!")


print("Sanitize your equipment and Fermentation Vessel!")

printInstruction('6 gallons of water')

print("You added water!")

# Parameters are time and temperature
# Bring Water to Boil
# Heater On (GPIO = LOW)
# Boiling Temperature reached
# Heater Off (GPIO = HIGH)

# Add Rice Extract
printInstruction("Rice Extract")

# Bring Water Back to Boil
# Heater On (GPIO = LOW)
# Boiling Temperature reached
# Heater Off (GPIO = HIGH)

# Add Willamette hops
printInstruction("Willamette hops")

# Bring Water Back to Boil
# Heater On (GPIO = LOW)
# if (temperature < 205)
#   Heater On
# if (temperature > 208)
#   Heater Off
# Repeat until 20 minutes have passed
# Heater Off (GPIO = HIGH)

# Add LME
printInstruction("Light Malt Extract")

# Add Whirlfloc
printInstruction("Whirfloc Tablet")

# Bring Water Back to Boil
# Heater On (GPIO = LOW)
# if (temperature < 205)
#   Heater On
# if (temperature > 208)
#   Heater Off
# Repeat until 10 minutes have passed
# Heater Off (GPIO = HIGH)

# Remove Hops
print("Remove hops bag now.")
acknowledgement = raw_input("Did you remove the hops bag? (y/n) ")
# update flag on database

while acknowledgement != 'y':
    acknowledgement = raw_input("Did you remove the hops bag? (y/n) ")

# Chilling Phase
# Pump On (GPIO = LOW)
# Until Temperature < 90F or
#   if 30 minutes have passed and temperature < 100F
# Pump Off (GPIO = HIGH)

# Solenoid On (GPIO = LOW)
# 3-4 minutes have passed (assuming kettle is emptied)
# Solenoid Off (GPIO = HIGH)

print("Add Yeast")

print("Cover and Ferment! Refer to fermentation in manual on next steps!")
