# Blonde Brewing Sample Program?

# Initialization
def initialize(GPIOpin):
    GPIO.setup(GPIOpin, GPIO.OUT)
    GPIO.output(GPIOpin, GPIO.HIGH)

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

MAX = 99

# Set up appropriate GPIOs (Heater, Cooling, Solenoid)
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
        acknowledgement = raw_input("Did you add {}? (y/n) " .format(instruction))

# This function heats the liquid.
# Input Parameters: Temperature you want to reach, and time?
# This function will check temperature, time, activate gpio when appropriate.
def heatControl(goalTime, goalTemperature):
    print("Beginning Heating Stage")
    #currentTemperature = get currentTemperature
    #while (currentTemperature < goalTemperature):
    GPIO.output(heater, GPIO.LOW) #Active Low Relay

    # Upon reaching appropriate temperature
    # Check to see if you have to maintain boil or can leave immediately
    #if (goalTime != MAX):
        #if(goalTime > 0):
            #print("Placeholder")
            #decrement goalTime
            #Leave Heater on because max temp is ~212

    
    #Temperature Reached
    time.sleep(5)
    GPIO.output(heater, GPIO.HIGH) #Re-Activates Relay
    print("Heating Done!")

# This function cools the liquid.
# Input Parameter: Temperature you want to reach, time limit?
# This function will check temperature, time, activate gpio when appropriate.
def coolingControl(goalTime, goalTemperature):
    print("Beginning Cooling Stage")
    #currentTemperature = get currentTemperature
    #while (currentTemperature >= goalTemperature):
    GPIO.output(cooling, GPIO.LOW) #Activates Cooler

    time.sleep(5)
    GPIO.output(cooling, GPIO.HIGH) #Re-activates Relay
    print("Cooling Done")

# This functions disperses the liquid
# Input Parameter: time //total time to release liquid. Take upper estimate.
def solenoidControl(goalTime):
    print("Beginning Dispersal")
    #while(goalTime > 0):
    GPIO.output(solenoid, GPIO.LOW) #Activates Solenoid
        #decrement time

    time.sleep(5)
    GPIO.output(solenoid, GPIO.HIGH) #Re-Activates Relay
    print("Finished Dispersal")

print("Sanitize your equipment and Fermentation Vessel!")

# Add Water
printInstruction('6 gallons of water')

print("You added water!")

# Bring Water to Boil
# Parameters are time(s) and temperature(F)
heatControl(MAX, 210) # Unlimited Time to bring to boil

# Add Rice Extract
printInstruction("Rice Extract")

# Bring Water Back to Boil
heatControl(MAX, 210) # Unlimited Time to bring to boil

# Add Willamette hops
printInstruction("Willamette hops")

# Bring Water Back to Boil
heatControl(20, 210) # Bring to Boil, then boil for 20 minutes

# Add LME
printInstruction("Malt Extract")

# Add Whirlfloc
printInstruction("Whirlfloc Tablet")

# Bring Water Back to Boil
heatControl (10, 210)

# Remove Hops
print("Remove hops bag now.")
acknowledgement = raw_input("Did you remove the hops bag? (y/n) ")
# update flag on database

while acknowledgement != 'y':
    acknowledgement = raw_input("Did you remove the hops bag? (y/n) ")

# Chilling Phase
coolingControl(MAX, 90)

#Dispersal Phase
solenoidControl(MAX)
# 3-4 minutes have passed (assuming kettle is emptied)


print("Add Yeast")

print("Cover and Ferment! Refer to fermentation in manual on next steps!")
