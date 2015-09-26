#!/usr/bin/python
#import RPi.GPIO as GPIO
import time                 # Set up clock/timer
import datetime
from datetime import timedelta
import MySQLdb
import sys
import os
import glob
import Tkinter
from Tkinter import *

##########################################################################################################
## Initialize GPIO pins to LOW, to turn off components
##########################################################################################################
def initializeGPIO(GPIOpin):
    x = 1
    # GPIO.setup(GPIOpin, GPIO.OUT)       # Set GPIO pin as OUTPUT
    # GPIO.output(GPIOpin, GPIO.LOW)     # Set GPIO pin to LOW (Turn off the components)

##########################################################################################################
## Initialize the temperature sensor
##########################################################################################################
def initializeTempSensor():
    global device_file
    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

##########################################################################################################
## Open database connection
##########################################################################################################
def checkSpartanBrewDB():
    global db
    # db = MySQLdb.connect(
    #     host="160.153.56.137",
    #     port=3306,
    #     user="spartanbrewadmin",
    #     passwd="D3PIgAKN[dk4",
    #     db="spartanbrewdb"
    # )
    db = MySQLdb.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="",
        db="spartanbrewdb"
    )

    global cursor
    cursor = db.cursor()

##########################################################################################################
## Get Raspberry Pi serial number (SpartanBrew ID)
##########################################################################################################
def getSpartanBrewID():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    cpuserial = "0000000000000002"

    return cpuserial

##########################################################################################################
## Get brewer ID
##########################################################################################################
def getBrewerID():
    sql = "SELECT BREWER_ID FROM spartanbrewdb.brewer_info WHERE SPARTANBREW_ID='%s'" % SPARTANBREW_ID
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        for row in cursor:
            brewer_id = row[0]
    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    return brewer_id

##########################################################################################################
## Check if brewing session is already active
##########################################################################################################
def checkBrewingSession():
    sql = "SELECT * FROM spartanbrewdb.brewing_sessions WHERE SPARTANBREW_ID='%s'" % SPARTANBREW_ID
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        if(results):
            print("brewing session in progress")
            displayBrewingSessionData()
        else:
            print("checking brewing session...")

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    root.after(1000, checkBrewingSession)

##########################################################################################################
## Get beer styles
##########################################################################################################
def getBeerStyles(beer_type):
    beer_styles_window = Tkinter.Tk()
    beer_styles_window.overrideredirect(1)
    beer_styles_window.geometry("%dx%d+0+0" % (320, 240))

    action = lambda x = 1: beer_styles_window.destroy()
    button = Button(beer_styles_window, text='<- BACK', command=action)
    button.grid(row=0, column=0, sticky=W+E+N+S)
    label = Label(beer_styles_window, text="%s Styles" % beer_type, bg="red")
    label.grid(row=0, column=1, sticky=W+E+N+S)

    sql = "SELECT DISTINCT BEER_STYLE FROM spartanbrewdb.beer_styles WHERE BEER_TYPE='%s' ORDER BY BEER_STYLE ASC" \
          % (beer_type)
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        row_position = 0
        for row in results:
            row_position += 1
            beer_style = row[0]
            action = lambda x = beer_style: getBeerNames(x)
            button = Button(beer_styles_window, text=beer_style, command=action)
            button.grid(row=row_position, column=0, sticky=W+E+N+S)

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    beer_styles_window.mainloop()

##########################################################################################################
## Get beer names
##########################################################################################################
def getBeerNames(beer_style):
    print(beer_style)
    beer_names_window = Tkinter.Tk()
    beer_names_window.overrideredirect(1)
    beer_names_window.geometry("%dx%d+0+0" % (320, 240))

    action = lambda x = 1: beer_names_window.destroy()
    button = Button(beer_names_window, text='<- BACK', command=action)
    button.grid(row=0, column=0, sticky=W+E+N+S)
    label = Label(beer_names_window, text="%s Styles" % beer_style, bg="red")
    label.grid(row=0, column=1, sticky=W+E+N+S)

    sql = "SELECT DISTINCT BEER_NAME FROM beer_info WHERE BEER_STYLE='%s' ORDER BY BEER_NAME ASC" % (beer_style)
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        row_position = 0
        column_position = 0
        for row in results:
            row_position += 1
            beer_name = row[0]
            action = lambda x = beer_name: getBeerInfo(x)
            button = Button(beer_names_window, text=beer_name, command=action)
            button.grid(row=row_position, column=column_position, sticky=W+E+N+S)
            if(row_position % 8 == 0):
                row_position = 0
                column_position += 1

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    beer_names_window.mainloop()

##########################################################################################################
## Display beer choices from type and styles
##########################################################################################################
def getBeerInfo(beer_name):
    print(beer_name)
    beer_info_window = Tkinter.Tk()
    beer_info_window.overrideredirect(1)
    beer_info_window.geometry("%dx%d+0+0" % (320, 240))

    action = lambda x = 1: beer_info_window.destroy()
    button = Button(beer_info_window, text='<- BACK', command=action)
    button.grid(row=0, column=0, sticky=W+E+N+S)
    label = Label(beer_info_window, text="%s" % beer_name, bg="red")
    label.grid(row=0, column=1, sticky=W+E+N+S)

    sql = "SELECT BEER_ID,BEER_DESCRIPTION, BEER_URL, BEER_ABV, BEER_IBU, BEER_SRM, BEER_OG " \
          "FROM spartanbrewdb.beer_info WHERE BEER_NAME='%s'" % (beer_name)
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            beer_id = row[0]
            beer_description = row[1]
            beer_url = row[2]
            beer_abv = row[3]
            beer_ibu = row[4]
            beer_srm = row[5]
            beer_og = row[6]
            label1 = Label(beer_info_window, text="Description: %s" % beer_description, wraplength=310, anchor=W, justify=LEFT)
            label1.grid(row=1, column=0, sticky=W+E+N+S, columnspan=4)
            label2 = Label(beer_info_window, text="ABV: %s%%" % beer_abv, anchor=W, justify=LEFT)
            label2.grid(row=2, column=0, sticky=W+E+N+S)
            label3 = Label(beer_info_window, text="IBU: %s" % beer_ibu, anchor=W, justify=LEFT)
            label3.grid(row=3, column=0, sticky=W+E+N+S)
            label4 = Label(beer_info_window, text="SRM: %s" % beer_srm, anchor=W, justify=LEFT)
            label4.grid(row=4, column=0, sticky=W+E+N+S)
            label5 = Label(beer_info_window, text="OG: %s" % beer_og, anchor=W, justify=LEFT)
            label5.grid(row=5, column=0, sticky=W+E+N+S)
            action = lambda x = beer_id: startBrewingSession(beer_id)
            button = Button(beer_info_window, text="Start Brewing", command=action)
            button.grid(row=4, column=3, sticky=W+E+N+S)

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    beer_info_window.mainloop()

##########################################################################################################
## Start brewing session
##########################################################################################################
def startBrewingSession(BEER_ID):
    global SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG, \
        ADD_DME_FLAG,WORT_BOILING_TIME,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME, \
        ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,ADD_YEAST_FLAG
    # Get brewing program info for beer_id and store into variables.
    sql = "SELECT SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG," \
        "ADD_DME_FLAG,WORT_BOILING_TIME,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME, " \
        "ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,ADD_YEAST_FLAG " \
        "FROM spartanbrewdb.brewing_programs WHERE BREWING_PROGRAM_ID=(SELECT BREWING_PROGRAM_ID " \
        "FROM spartanbrewdb.beer_info WHERE BEER_ID=%d)" % (BEER_ID)

    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            SANITIZE_EQUIPMENT = row[0]
            ADD_WATER_FLAG = row[1]
            ADD_GRAINS_FLAG = row[2]
            ADD_GRAINS_TEMP = row[3]
            REMOVE_GRAINS_FLAG = row[4]
            REMOVE_GRAINS_TIME = row[5]
            ADD_LME_FLAG = row[6]
            ADD_DME_FLAG = row[7]
            WORT_BOILING_TIME = row[8]
            ADD_HOPS_1_FLAG = row[9]
            ADD_HOPS_1_TIME = row[10]
            ADD_HOPS_2_FLAG = row[11]
            ADD_HOPS_2_TIME = row[12]
            ADD_HOPS_3_FLAG = row[13]
            ADD_HOPS_3_TIME = row[14]
            ADD_HOPS_4_FLAG = row[15]
            ADD_HOPS_4_TIME = row[16]
            ADD_WHIRLFLOC_FLAG = row[17]
            ADD_YEAST_FLAG = row[18]

            sql = "INSERT INTO spartanbrewdb.brewing_sessions (SPARTANBREW_ID,BREWER_ID, BEER_ID,SANITIZE_EQUIPMENT," \
                "ADD_WATER_FLAG,ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG,ADD_DME_FLAG," \
                "WORT_BOILING_TIME,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG," \
                "ADD_HOPS_3_TIME,ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,ADD_YEAST_FLAG)" \
                "VALUES ('%s',%d,%d,%d,%d,%d,%d,%d,'%s',%d,%d,'%s',%d,'%s',%d,'%s',%d,'%s',%d,'%s',%d,%d)" \
              % (SPARTANBREW_ID,BREWER_ID,BEER_ID,SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG, \
                 REMOVE_GRAINS_TIME,ADD_LME_FLAG,ADD_DME_FLAG,WORT_BOILING_TIME,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG, \
                 ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME,ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG, \
                 ADD_YEAST_FLAG)
            try:
                checkSpartanBrewDB()
                cursor.execute(sql)
                db.commit()
                print("**BREWING SESSION ACTIVE**")

            except MySQLdb.Error, e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
                db.rollback()

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    checkBrewingSession()

##########################################################################################################
## display brewing session data
##########################################################################################################
def displayBrewingSessionData():
    brewing_session_window = Tkinter.Tk()
    brewing_session_window.overrideredirect(1)
    brewing_session_window.geometry("%dx%d+0+0" % (320, 240))

    ######################################################################################
    ## Get beer name currently brewing
    ######################################################################################
    global beer_name
    sql = "SELECT BEER_NAME FROM spartanbrewdb.beer_info WHERE BEER_ID=(SELECT BEER_ID FROM spartanbrewdb.brewing_sessions" \
          " WHERE SPARTANBREW_ID='%s')" % SPARTANBREW_ID

    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            beer_name = row[0]

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    ######################################################################################
    ## Header info
    ######################################################################################
    action = lambda x = brewing_session_window: cancelBrewingSession(x)
    button = Button(brewing_session_window, text='<- QUIT', command=action)
    button.grid(row=0, column=0, sticky=W+E+N+S)
    header = Label(brewing_session_window, text=str(beer_name), bg="red")
    header.grid(row=0, column=1, columnspan=5, sticky=W+E+N+S)

    ######################################################################################
    ## Sanitize flag
    ######################################################################################
    sanitize_equipment_label = Label(brewing_session_window, text="Sanitized?")
    sanitize_equipment_label.grid(row=1, column=0, sticky=E)
    sanitize_equipment_data = Label(brewing_session_window, fg="red")
    sanitize_equipment_data.grid(row=1, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Water flag
    ######################################################################################
    water_label = Label(brewing_session_window, text="Water?")
    water_label.grid(row=2, column=0, sticky=E)
    water_data = Label(brewing_session_window, fg="red")
    water_data.grid(row=2, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Add grains flag
    ######################################################################################
    add_grains_label = Label(brewing_session_window, text="Add Grains?")
    add_grains_label.grid(row=3, column=0, sticky=E)
    add_grains_data = Label(brewing_session_window, fg="red")
    add_grains_data.grid(row=3, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Remove grains flag
    ######################################################################################
    remove_grains_label = Label(brewing_session_window, text="Remove Grains?")
    remove_grains_label.grid(row=4, column=0, sticky=E)
    remove_grains_data = Label(brewing_session_window, fg="red")
    remove_grains_data.grid(row=4, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Malt extract flag
    ######################################################################################
    malt_extract_label = Label(brewing_session_window, text="Malt Extract?")
    malt_extract_label.grid(row=5, column=0, sticky=E)
    malt_extract_data = Label(brewing_session_window, fg="red")
    malt_extract_data.grid(row=5, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## 1st hops flag
    ######################################################################################
    first_hops_label = Label(brewing_session_window, text="1st Hops?")
    first_hops_label.grid(row=6, column=0, sticky=E)
    first_hops_data = Label(brewing_session_window, fg="red")
    first_hops_data.grid(row=6, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## 2nd hops flag
    ######################################################################################
    second_hops_label = Label(brewing_session_window, text="2nd Hops?")
    second_hops_label.grid(row=7, column=0, sticky=E)
    second_hops_data = Label(brewing_session_window, fg="red")
    second_hops_data.grid(row=7, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## 3rd hops flag
    ######################################################################################
    third_hops_label = Label(brewing_session_window, text="3rd Hops?")
    third_hops_label.grid(row=8, column=0, sticky=E)
    third_hops_data = Label(brewing_session_window, fg="red")
    third_hops_data.grid(row=8, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## 4th hops flag
    ######################################################################################
    fourth_hops_label = Label(brewing_session_window, text="4th Hops?")
    fourth_hops_label.grid(row=9, column=0, sticky=E)
    fourth_hops_data = Label(brewing_session_window, fg="red")
    fourth_hops_data.grid(row=9, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Whirlfloc flag
    ######################################################################################
    whirlfloc_label = Label(brewing_session_window, text="Whirfloc?")
    whirlfloc_label.grid(row=10, column=0, sticky=E)
    whirlfloc_data = Label(brewing_session_window, fg="red")
    whirlfloc_data.grid(row=10, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Yeast flag
    ######################################################################################
    yeast_label = Label(brewing_session_window, text="Yeast?")
    yeast_label.grid(row=11, column=0, sticky=E)
    yeast_data = Label(brewing_session_window, fg="red")
    yeast_data.grid(row=11, column=1, sticky=W+E+N+S)

    ######################################################################################
    ## Temperature data
    ######################################################################################
    temperature_label = Label(brewing_session_window, text="Temperature (F/C):")
    temperature_label.grid(row=1, column=2, columnspan=2, sticky=W)
    temperature_data = Label(brewing_session_window, fg="red")
    temperature_data.grid(row=2, column=2, columnspan=2, sticky=W)

    ######################################################################################
    ## Remaining time
    ######################################################################################
    remaining_time_label = Label(brewing_session_window, text="Remaining Time:")
    remaining_time_label.grid(row=3, column=2, columnspan=2, sticky=W)
    remaining_time_data = Label(brewing_session_window, fg="red")
    remaining_time_data.grid(row=4, column=2, columnspan=2, sticky=W)

    ######################################################################################
    ## Elapsed time
    ######################################################################################
    elapsed_time_label = Label(brewing_session_window, text="Elapsed Time:")
    elapsed_time_label.grid(row=5, column=2, columnspan=2, sticky=W)
    elapsed_time_data = Label(brewing_session_window, fg="red")
    elapsed_time_data.grid(row=6, column=2, columnspan=2, sticky=W)
    
    ######################################################################################
    ## Cooling flag
    ######################################################################################
    cooling_label = Label(brewing_session_window, text="Cooling:")
    cooling_label.grid(row=7, column=2, columnspan=1, sticky=W)
    cooling_data = Label(brewing_session_window, fg="red")
    cooling_data.grid(row=7, column=3, columnspan=1, sticky=W)
    
    ######################################################################################
    ## Solenoid flag
    ######################################################################################
    solenoid_label = Label(brewing_session_window, text="Solenoid:")
    solenoid_label.grid(row=8, column=2, columnspan=1, sticky=W)
    solenoid_data = Label(brewing_session_window, fg="red")
    solenoid_data.grid(row=8, column=3, columnspan=1, sticky=W)

    ######################################################################################
    ## Update the brewing session data
    ######################################################################################
    sql = "SELECT * FROM spartanbrewdb.brewing_sessions WHERE SPARTANBREW_ID='%s'" % SPARTANBREW_ID

    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        if(results == False):
            try:
                brewing_session_window.destroy()
            except ValueError,e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
        else:
            updateBrewingSessionData(brewing_session_window,sanitize_equipment_data,water_data,add_grains_data,
                            remove_grains_data,malt_extract_data,first_hops_data,second_hops_data,third_hops_data,
                            fourth_hops_data,whirlfloc_data,yeast_data,temperature_data,remaining_time_data,
                            elapsed_time_data,cooling_data,solenoid_data)

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    brewing_session_window.mainloop()

##########################################################################################################
## Update the brewing session data dynamically
##########################################################################################################
def updateBrewingSessionData(brewing_session_window,sanitize_equipment_data,water_data,add_grains_data,remove_grains_data,
                             malt_extract_data,first_hops_data,second_hops_data,third_hops_data,fourth_hops_data,
                             whirlfloc_data,yeast_data,temperature_data,remaining_time_data,elapsed_time_data,cooling_data,
                             solenoid_data):
    def getData():
        global ELAPSED_TIME,REMAINING_TIME,TEMPERATURE_F,TEMPERATURE_C,SANITIZE_EQUIPMENT,ADD_WATER_FLAG, \
                    ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG,ADD_DME_FLAG,WORT_BOILING_TIME, \
                    ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME, \
                    ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,COOLING_FLAG,SOLENOID_FLAG,ADD_YEAST_FLAG, \
                    BREWING_DATE_START
        sql = "SELECT TEMPERATURE_F,TEMPERATURE_C,SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,ADD_GRAINS_TEMP,REMOVE_GRAINS_FLAG, \
                REMOVE_GRAINS_TIME,ADD_LME_FLAG,ADD_DME_FLAG,WORT_BOILING_TIME,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME, \
                ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME, ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME, \
                ADD_WHIRLFLOC_FLAG,COOLING_FLAG,SOLENOID_FLAG,ADD_YEAST_FLAG,BREWING_DATE_START \
                FROM spartanbrewdb.brewing_sessions WHERE SPARTANBREW_ID='%s'" % SPARTANBREW_ID

        try:
            checkSpartanBrewDB()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                TEMPERATURE_F = row[0]
                TEMPERATURE_C = row[1]
                SANITIZE_EQUIPMENT = row[2]
                ADD_WATER_FLAG = row[3]
                ADD_GRAINS_FLAG = row[4]
                ADD_GRAINS_TEMP = row[5]
                REMOVE_GRAINS_FLAG = row[6]
                REMOVE_GRAINS_TIME = row[7]
                ADD_LME_FLAG = row[8]
                ADD_DME_FLAG = row[9]
                WORT_BOILING_TIME = row[10]
                ADD_HOPS_1_FLAG = row[11]
                ADD_HOPS_1_TIME = row[12]
                ADD_HOPS_2_FLAG = row[13]
                ADD_HOPS_2_TIME = row[14]
                ADD_HOPS_3_FLAG = row[15]
                ADD_HOPS_3_TIME = row[16]
                ADD_HOPS_4_FLAG = row[17]
                ADD_HOPS_4_TIME = row[18]
                ADD_WHIRLFLOC_FLAG = row[19]
                COOLING_FLAG = row[20]
                SOLENOID_FLAG = row[21]
                ADD_YEAST_FLAG = row[22]
                BREWING_DATE_START = row[23]

        except MySQLdb.Error, e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

        global ingredient_add_time
        x = time.strptime('00:00:00',"%H:%M:%S")
        REMAINING_TIME = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        ######################################################################################
        ## Temperature data
        ######################################################################################
        temperature = "%.1f / %.1f" % (TEMPERATURE_F,TEMPERATURE_C) #getTemperature()
        temperature_data.config(text=str(temperature))

        ######################################################################################
        ## Sanitize flag
        ######################################################################################
        if(SANITIZE_EQUIPMENT == 0):
            sanitize_info = "NO"
        elif(SANITIZE_EQUIPMENT == 1):
            sanitize_info = "WAITING"
            displayIngredientAdd(brewing_session_window,"SANITIZE_EQUIPMENT")
        elif(SANITIZE_EQUIPMENT == 2):
            sanitize_info = "YES"
        else:
            sanitize_info = "N/A"
        sanitize_equipment_data.config(text=str(sanitize_info))

        ######################################################################################
        ## Water flag
        ######################################################################################
        if(ADD_WATER_FLAG == 0):
            water_info = "NO"
        elif(ADD_WATER_FLAG == 1):
            water_info = "WAITING"
            displayIngredientAdd(brewing_session_window,"ADD_WATER_FLAG")
        elif(ADD_WATER_FLAG == 2):
            water_info = "YES"
        else:
            water_info = "N/A"
        water_data.config(text=str(water_info))

        ######################################################################################
        ## Add grains flag
        ######################################################################################
        if(ADD_GRAINS_FLAG == 0):
            add_grains_info = "NO"
        elif(ADD_GRAINS_FLAG == 1):
            add_grains_info = "WAITING"
            if(TEMPERATURE_F < ADD_GRAINS_TEMP):
                turnOnHeater()
            elif(TEMPERATURE_F >= ADD_GRAINS_TEMP):
                turnOffHeater()
                displayIngredientAdd(brewing_session_window,"ADD_GRAINS_FLAG")
        elif(ADD_GRAINS_FLAG == 2):
            add_grains_info = "YES"
        else:
            add_grains_info = "N/A"
        add_grains_data.config(text=str(add_grains_info))

        ######################################################################################
        ## Remove grains flag
        ######################################################################################
        if(REMOVE_GRAINS_FLAG == 0):
            remove_grains_info = "NO"
        elif(REMOVE_GRAINS_FLAG == 1):
            remove_grains_info = "WAITING"
            if(TEMPERATURE_F < ADD_GRAINS_TEMP):
                turnOnHeater()
            elif(TEMPERATURE_F >= ADD_GRAINS_TEMP):
                turnOffHeater()
            temp_remove_grains_time = time.strptime(str(REMOVE_GRAINS_TIME),"%H:%M:%S")
            remove_grains_seconds = datetime.timedelta(hours=temp_remove_grains_time.tm_hour,minutes=temp_remove_grains_time.tm_min,
                                   seconds=temp_remove_grains_time.tm_sec).total_seconds()
            ingredient_add_time = ingredient_start_time + remove_grains_seconds
            total_remaining_time = ingredient_add_time - time.time()
            hours = total_remaining_time / 3600
            minutes = total_remaining_time / 60
            seconds = total_remaining_time % 60
            REMAINING_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds)
            if(total_remaining_time <= zero_sec):
                if(TEMPERATURE_F < ADD_GRAINS_TEMP):
                    turnOnHeater()
                elif(TEMPERATURE_F >= ADD_GRAINS_TEMP):
                    turnOffHeater()
                displayIngredientAdd(brewing_session_window,"REMOVE_GRAINS_FLAG")
        elif(REMOVE_GRAINS_FLAG == 2):
            remove_grains_info = "YES"
        else:
            remove_grains_info = "N/A"
        remove_grains_data.config(text=str(remove_grains_info))

        ######################################################################################
        ## Malt extract flag
        ######################################################################################
        if(ADD_DME_FLAG == 3):
            ADD_MALT_EXTRACT_FLAG = ADD_LME_FLAG
            malt_extract_name = "ADD_LME_FLAG"
        else:
            ADD_MALT_EXTRACT_FLAG = ADD_DME_FLAG
            malt_extract_name = "ADD_DME_FLAG"

        if(ADD_MALT_EXTRACT_FLAG == 0):
            malt_extract_info = "NO"
        elif(ADD_MALT_EXTRACT_FLAG == 1):
            malt_extract_info = "WAITING"
            if(TEMPERATURE_F < 200):
                turnOnHeater()
            elif(TEMPERATURE_F >= 212):
                turnOffHeater()
                displayIngredientAdd(brewing_session_window,malt_extract_name)
        elif(ADD_MALT_EXTRACT_FLAG == 2):
            malt_extract_info = "YES"
        else:
            malt_extract_info = "N/A"
        malt_extract_data.config(text=str(malt_extract_info))

        ######################################################################################
        ## Boiling time
        ######################################################################################
        global total_boiling_time, boiling_remaining_time
        x = time.strptime(str(WORT_BOILING_TIME),"%H:%M:%S")
        total_boiling_time = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        boiling_remaining_time = total_boiling_time

        global add_hops_1_seconds,add_hops_2_seconds,add_hops_3_seconds,add_hops_4_seconds

        ######################################################################################
        ## 1st hops flag
        ######################################################################################
        if(ADD_HOPS_1_FLAG == 0):
            hops_1_info = "NO"
        elif(ADD_HOPS_1_FLAG == 1):
            hops_1_info = "WAITING"
            if(TEMPERATURE_F < 212):
                turnOnHeater()
            elif(TEMPERATURE_F >= 212):
                turnOffHeater()

            temp_add_hops_1_time = time.strptime(str(ADD_HOPS_1_TIME),"%H:%M:%S") ## Convert Add Hops 1 time to time format
            add_hops_1_seconds = datetime.timedelta(hours=temp_add_hops_1_time.tm_hour,minutes=temp_add_hops_1_time.tm_min,
                                   seconds=temp_add_hops_1_time.tm_sec).total_seconds() ## Retrieve seconds
            ingredient_add_time = ingredient_start_time + add_hops_1_seconds ## Get the end time to add Hops 1
            hop_remaining_time = ingredient_add_time - time.time() ## Calculate the remaining time until Hops 1 can be added
            hours = hop_remaining_time / 3600
            minutes = hop_remaining_time / 60
            seconds = hop_remaining_time % 60
            REMAINING_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds) ## Format the remaining time
            print("Remaining Time: %s" % REMAINING_TIME)
            if(hop_remaining_time <= zero_sec):
                if(TEMPERATURE_F < 212):
                    turnOnHeater()
                elif(TEMPERATURE_F >= 212):
                    turnOffHeater()
                boiling_remaining_time = total_boiling_time - add_hops_1_seconds
                displayIngredientAdd(brewing_session_window,"ADD_HOPS_1_FLAG")
        elif(ADD_HOPS_1_FLAG == 2):
            hops_1_info = "YES"
        else:
            hops_1_info = "N/A"
            temp_add_hops_1_time = time.strptime('00:00:00',"%H:%M:%S") ## Convert Add Hops 1 time to time format
            add_hops_1_seconds = datetime.timedelta(hours=temp_add_hops_1_time.tm_hour,minutes=temp_add_hops_1_time.tm_min,
                                   seconds=temp_add_hops_1_time.tm_sec).total_seconds() ## Retrieve seconds
        first_hops_data.config(text=str(hops_1_info))

        ######################################################################################
        ## 2nd hops flag
        ######################################################################################
        if(ADD_HOPS_2_FLAG == 0):
            hops_2_info = "NO"
        elif(ADD_HOPS_2_FLAG == 1):
            hops_2_info = "WAITING"
            if(TEMPERATURE_F < 212):
                turnOnHeater()
            elif(TEMPERATURE_F >= 212):
                turnOffHeater()

            temp_add_hops_2_time = time.strptime(str(ADD_HOPS_2_TIME),"%H:%M:%S") ## Convert Add Hops 2 time to time format
            add_hops_2_seconds = datetime.timedelta(hours=temp_add_hops_2_time.tm_hour,minutes=temp_add_hops_2_time.tm_min,
                                   seconds=temp_add_hops_2_time.tm_sec).total_seconds() ## Retrieve seconds
            ingredient_add_time = ingredient_start_time + add_hops_2_seconds ## Get the end time to add Hops 2
            hop_remaining_time = ingredient_add_time - time.time() ## Calculate the remaining time until Hops 2 can be added
            hours = hop_remaining_time / 3600
            minutes = hop_remaining_time / 60
            seconds = hop_remaining_time % 60
            REMAINING_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds) ## Format the remaining time
            print("Start time: %s" % ingredient_start_time)
            print("Add time: %s" % ingredient_add_time)
            print("Hop remaining time: %s" % hop_remaining_time)
            print("Remaining Time: %s" % REMAINING_TIME)
            if(hop_remaining_time <= zero_sec):
                if(TEMPERATURE_F < 212):
                    turnOnHeater()
                elif(TEMPERATURE_F >= 212):
                    turnOffHeater()
                boiling_remaining_time = total_boiling_time - add_hops_1_seconds - add_hops_2_seconds
                print("Boiling remaining time: %s" % boiling_remaining_time)
                displayIngredientAdd(brewing_session_window,"ADD_HOPS_2_FLAG")
        elif(ADD_HOPS_2_FLAG == 2):
            hops_2_info = "YES"
        else:
            hops_2_info = "N/A"
            temp_add_hops_2_time = time.strptime('00:00:00',"%H:%M:%S") ## Convert Add Hops 2 time to time format
            add_hops_2_seconds = datetime.timedelta(hours=temp_add_hops_2_time.tm_hour,minutes=temp_add_hops_2_time.tm_min,
                                   seconds=temp_add_hops_2_time.tm_sec).total_seconds() ## Retrieve seconds
        second_hops_data.config(text=str(hops_2_info))

        ######################################################################################
        ## 3rd hops flag
        ######################################################################################
        if(ADD_HOPS_3_FLAG == 0):
            hops_3_info = "NO"
        elif(ADD_HOPS_3_FLAG == 1):
            hops_3_info = "WAITING"
            if(TEMPERATURE_F < 212):
                turnOnHeater()
            elif(TEMPERATURE_F >= 212):
                turnOffHeater()

            temp_add_hops_3_time = time.strptime(str(ADD_HOPS_3_TIME),"%H:%M:%S") ## Convert Add Hops 3 time to time format
            add_hops_3_seconds = datetime.timedelta(hours=temp_add_hops_3_time.tm_hour,minutes=temp_add_hops_3_time.tm_min,
                                   seconds=temp_add_hops_3_time.tm_sec).total_seconds() ## Retrieve seconds
            ingredient_add_time = ingredient_start_time + add_hops_3_seconds ## Get the end time to add Hops 3
            hop_remaining_time = ingredient_add_time - time.time() ## Calculate the remaining time until Hops 3 can be added
            hours = hop_remaining_time / 3600
            minutes = hop_remaining_time / 60
            seconds = hop_remaining_time % 60
            REMAINING_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds) ## Format the remaining time
            print("Start time: %s" % ingredient_start_time)
            print("Add time: %s" % ingredient_add_time)
            print("Hop remaining time: %s" % hop_remaining_time)
            print("Remaining Time: %s" % REMAINING_TIME)
            if(hop_remaining_time <= zero_sec):
                if(TEMPERATURE_F < 212):
                    turnOnHeater()
                elif(TEMPERATURE_F >= 212):
                    turnOffHeater()
                boiling_remaining_time = total_boiling_time - add_hops_1_seconds - add_hops_2_seconds - add_hops_3_seconds
                print("Boiling remaining time: %s" % boiling_remaining_time)
                displayIngredientAdd(brewing_session_window,"ADD_HOPS_3_FLAG")
        elif(ADD_HOPS_3_FLAG == 2):
            hops_3_info = "YES"
        else:
            hops_3_info = "N/A"
            temp_add_hops_3_time = time.strptime('00:00:00',"%H:%M:%S") ## Convert Add Hops 3 time to time format
            add_hops_3_seconds = datetime.timedelta(hours=temp_add_hops_3_time.tm_hour,minutes=temp_add_hops_3_time.tm_min,
                                   seconds=temp_add_hops_3_time.tm_sec).total_seconds() ## Retrieve seconds
        third_hops_data.config(text=str(hops_3_info))

        ######################################################################################
        ## 4th hops flag
        ######################################################################################
        if(ADD_HOPS_4_FLAG == 0):
            hops_4_info = "NO"
        elif(ADD_HOPS_4_FLAG == 1):
            hops_4_info = "WAITING"
            displayIngredientAdd(brewing_session_window,"ADD_HOPS_4_FLAG")
        elif(ADD_HOPS_4_FLAG == 2):
            hops_4_info = "YES"
        else:
            hops_4_info = "N/A"
            temp_add_hops_4_time = time.strptime('00:00:00',"%H:%M:%S") ## Convert Add Hops 2 time to time format
            add_hops_4_seconds = datetime.timedelta(hours=temp_add_hops_4_time.tm_hour,minutes=temp_add_hops_4_time.tm_min,
                                   seconds=temp_add_hops_4_time.tm_sec).total_seconds() ## Retrieve seconds
        fourth_hops_data.config(text=str(hops_4_info))

        ######################################################################################
        ## Whirlfloc flag
        ######################################################################################
        if(ADD_WHIRLFLOC_FLAG == 0):
            whirlfloc_info = "NO"
        elif(ADD_WHIRLFLOC_FLAG == 1):
            whirlfloc_info = "WAITING"
            displayIngredientAdd(brewing_session_window,"ADD_WHIRLFLOC_FLAG")
        elif(ADD_WHIRLFLOC_FLAG == 2):
            whirlfloc_info = "YES"
        else:
            whirlfloc_info = "N/A"
        whirlfloc_data.config(text=str(whirlfloc_info))

        ######################################################################################
        ## Cooling flag
        ######################################################################################
        if(COOLING_FLAG == 0):
            cooling_info = "NO"
        elif(COOLING_FLAG == 1):
            cooling_info = "WAITING"
            cooling_start_time = ingredient_start_time - add_hops_1_seconds - add_hops_2_seconds - add_hops_3_seconds - \
                                 add_hops_4_seconds + total_boiling_time ## Get the endtime to begin cooling
            boiling_remaining_time = cooling_start_time - time.time() ## Calculate the remaining time until cooling starts
            hours = boiling_remaining_time / 3600
            minutes = (boiling_remaining_time / 60) % 60
            seconds = boiling_remaining_time % 60
            REMAINING_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds) ## Format the remaining time
            print("Boiling remaining time: %s" % boiling_remaining_time)
            if(boiling_remaining_time <= zero_sec):
                cooling_info = "IN PROGRESS"
                REMAINING_TIME = "00:00:00"
                turnOffHeater()
                if(TEMPERATURE_F > 90):
                    turnOnCooler()
                elif(TEMPERATURE_F <= 90):
                    turnOffCooler()
                    updateIngredientFlag(brewing_session_window,"COOLING_FLAG","SOLENOID_FLAG")
            elif(TEMPERATURE_F < 212):
                turnOnHeater()
            elif(TEMPERATURE_F >= 212):
                turnOffHeater()
            #displayIngredientAdd(brewing_session_window,"COOLING_FLAG")
        elif(COOLING_FLAG == 2):
            cooling_info = "DONE"
            turnOffCooler()
        else:
            cooling_info = "N/A"
            turnOffCooler()
        cooling_data.config(text=str(cooling_info))

        ######################################################################################
        ## Release flag
        ######################################################################################
        if(SOLENOID_FLAG == 0):
            solenoid_info = "NO"
        elif(SOLENOID_FLAG == 1):
            solenoid_info = "IN PROGRESS"
            turnOffHeater()
            turnOffCooler()
            temp_solenoid_time = time.strptime('00:00:10',"%H:%M:%S") ## Convert solenoid open time to time format
            solenoid_seconds = datetime.timedelta(hours=temp_solenoid_time.tm_hour,minutes=temp_solenoid_time.tm_min,
                                   seconds=temp_solenoid_time.tm_sec).total_seconds() ## Retrieve seconds
            solenoid_close_time = ingredient_start_time + solenoid_seconds ## Get the end time to keep solenoid open
            solenoid_remaining_time = solenoid_close_time - time.time() ## Calculate the remaining time until solenoid closes
            hours = solenoid_remaining_time / 3600
            minutes = (solenoid_remaining_time / 60) % 60
            seconds = solenoid_remaining_time % 60
            REMAINING_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds) ## Format the remaining time
            turnOnSolenoid()
            if(solenoid_remaining_time <= zero_sec):
                turnOffSolenoid()
                updateIngredientFlag(brewing_session_window,"SOLENOID_FLAG","ADD_YEAST_FLAG")
            #displayIngredientAdd(brewing_session_window,"SOLENOID_FLAG")
        elif(SOLENOID_FLAG == 2):
            solenoid_info = "DONE"
        else:
            solenoid_info = "N/A"
        solenoid_data.config(text=str(solenoid_info))

        ######################################################################################
        ## Yeast flag
        ######################################################################################
        if(ADD_YEAST_FLAG == 0):
            yeast_info = "NO"
        elif(ADD_YEAST_FLAG == 1):
            yeast_info = "WAITING"
            displayIngredientAdd(brewing_session_window,"ADD_YEAST_FLAG")
            updateIngredientFlag(brewing_session_window,"ADD_YEAST_FLAG","FINISH_FLAG")
            time.sleep(2)
        elif(ADD_YEAST_FLAG == 2):
            yeast_info = "YES"
            finishBrewingSession(brewing_session_window)
        else:
            yeast_info = "N/A"
        yeast_data.config(text=str(yeast_info))

        ######################################################################################
        ## Remaining time
        ######################################################################################
        sql = "UPDATE spartanbrewdb.brewing_sessions SET REMAINING_TIME='%s' WHERE SPARTANBREW_ID='%s'" \
                % (REMAINING_TIME,SPARTANBREW_ID)
        try:
            checkSpartanBrewDB()
            cursor.execute(sql)
            db.commit()

        except MySQLdb.Error, e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()

        remaining_time_data.config(text=str(REMAINING_TIME))

        ######################################################################################
        ## Elapsed time
        ######################################################################################
        total_elapsed_time = (datetime.datetime.today() - BREWING_DATE_START).seconds
        hours = total_elapsed_time / 3600
        minutes = (total_elapsed_time / 60) % 60
        seconds = total_elapsed_time % 60
        ELAPSED_TIME = "%02d:%02d:%02d" % (hours,minutes,seconds)

        sql = "UPDATE spartanbrewdb.brewing_sessions SET ELAPSED_TIME='%s' WHERE SPARTANBREW_ID='%s'" \
                % (ELAPSED_TIME,SPARTANBREW_ID)
        try:
            checkSpartanBrewDB()
            cursor.execute(sql)
            db.commit()

        except MySQLdb.Error, e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()

        print("Elapsed Time: %s" % ELAPSED_TIME)
        elapsed_time_data.config(text=str(ELAPSED_TIME))

        if(results):
            try:
                print('brewing in session...')
                elapsed_time_data.after(1000, getData)
            except ValueError,e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
        else:
            brewing_session_window.destroy()
            checkBrewingSession()

    getData()

##########################################################################################################
## Cancel the brewing session
##########################################################################################################
def cancelBrewingSession(brewing_session_window):
    try:
        brewing_session_window.destroy()
    except ValueError,e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    sql = "DELETE FROM spartanbrewdb.brewing_sessions WHERE SPARTANBREW_ID='%s'" % (SPARTANBREW_ID)
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        db.commit()

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()

    turnOffHeater()
    turnOffCooler()
    turnOffSolenoid()
    checkBrewingSession()

##########################################################################################################
## Finish the brewing session
##########################################################################################################
def finishBrewingSession(brewing_session_window):
    try:
        brewing_session_window.destroy()
    except ValueError,e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    sql = "DELETE FROM spartanbrewdb.brewing_sessions WHERE SPARTANBREW_ID='%s'" % (SPARTANBREW_ID)
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        db.commit()

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()

    turnOffHeater()
    turnOffCooler()
    turnOffSolenoid()
    checkBrewingSession()

##########################################################################################################
## Get temperature from DS18B20 temperature sensor
##########################################################################################################
def getTemperature():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
    temperature_c = float(temp_string) / 1000.0
    temperature_f = temperature_c * 9.0 / 5.0 + 32.0

    temperature = "%.1f / %.1f" % (temperature_f,temperature_c)

    sql = "UPDATE spartanbrewdb.brewing_sessions SET TEMPERATURE_F=%.1f,TEMPERATURE_C=%.1f \
          WHERE SPARTANBREW_ID='%s'" % (temperature_f,temperature_c,SPARTANBREW_ID)
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        db.commit()

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()

    return temperature

##########################################################################################################
## Read the raw temperature from DS18B20 temperature sensor
##########################################################################################################
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

##########################################################################################################
## Display the confirmation of adding an ingredient
##########################################################################################################
def displayIngredientAdd(brewing_session_window,ingredient_name):
    try:
        brewing_session_window.destroy()
    except ValueError,e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    ingredient_add_window = Tkinter.Tk()
    ingredient_add_window.overrideredirect(1)
    ingredient_add_window.geometry("%dx%d+0+0" % (320, 240))

    header = Label(ingredient_add_window, text="Confirm Ingredient Add", bg="red")
    header.grid(row=0, column=0, columnspan=5, sticky=W+E+N+S)

    ingredient_label = Label(ingredient_add_window, text="", wraplength=310, anchor=W, justify=LEFT)
    ingredient_label.grid(row=1, column=0, sticky=W+E+N+S, columnspan=4)

    action = lambda x = 1: updateIngredientFlag(ingredient_add_window,ingredient_name,next_ingredient)
    button = Button(ingredient_add_window, text='YES', command=action)
    button.grid(row=2, column=0, sticky=W+E+N+S)

    button = Button(ingredient_add_window, text='NO')
    button.grid(row=2, column=1, sticky=W+E+N+S)

    confirmIngredientAdd(ingredient_label)

    ingredient_add_window.mainloop()

##########################################################################################################
## Confirm an ingredient has been added
##########################################################################################################
def confirmIngredientAdd(ingredient_label):
    def getIngredientFlag():
        global SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG, \
                ADD_DME_FLAG,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME, \
                ADD_HOPS_3_FLAG,ADD_HOPS_3_TIME,ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,COOLING_FLAG, \
                SOLENOID_FLAG,ADD_YEAST_FLAG
        sql = "SELECT SANITIZE_EQUIPMENT,ADD_WATER_FLAG,ADD_GRAINS_FLAG,REMOVE_GRAINS_FLAG,REMOVE_GRAINS_TIME,ADD_LME_FLAG, \
                ADD_DME_FLAG,ADD_HOPS_1_FLAG,ADD_HOPS_1_TIME,ADD_HOPS_2_FLAG,ADD_HOPS_2_TIME,ADD_HOPS_3_FLAG, \
                ADD_HOPS_3_TIME,ADD_HOPS_4_FLAG,ADD_HOPS_4_TIME,ADD_WHIRLFLOC_FLAG,COOLING_FLAG,SOLENOID_FLAG,ADD_YEAST_FLAG \
                FROM spartanbrewdb.brewing_sessions WHERE SPARTANBREW_ID='%s'" % SPARTANBREW_ID

        try:
            checkSpartanBrewDB()
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                SANITIZE_EQUIPMENT = row[0]
                ADD_WATER_FLAG = row[1]
                ADD_GRAINS_FLAG = row[2]
                REMOVE_GRAINS_FLAG = row[3]
                REMOVE_GRAINS_TIME = row[4]
                ADD_LME_FLAG = row[5]
                ADD_DME_FLAG = row[6]
                ADD_HOPS_1_FLAG = row[7]
                ADD_HOPS_1_TIME = row[8]
                ADD_HOPS_2_FLAG = row[9]
                ADD_HOPS_2_TIME = row[10]
                ADD_HOPS_3_FLAG = row[11]
                ADD_HOPS_3_TIME = row[12]
                ADD_HOPS_4_FLAG = row[13]
                ADD_HOPS_4_TIME = row[14]
                ADD_WHIRLFLOC_FLAG = row[15]
                COOLING_FLAG = row[16]
                SOLENOID_FLAG = row[17]
                ADD_YEAST_FLAG = row[18]

        except MySQLdb.Error, e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

        if(SANITIZE_EQUIPMENT == 1):
            ingredient_flag = SANITIZE_EQUIPMENT
            ingredient_message = "Before brewing, please make sure all equipment has been washed and sanitized thoroughly. " \
                                 "Ready to brew?"
        elif(ADD_WATER_FLAG == 1):
            ingredient_flag = ADD_WATER_FLAG
            ingredient_message = "Add 6 gallons of dechlorinated water to the pot. Filtered and/or distilled water is " \
                                 "preferred, but not required. Confirm?"
        elif(ADD_GRAINS_FLAG == 1):
            ingredient_flag = ADD_GRAINS_FLAG
            ingredient_message = "Place the grains inside of a large nylon mesh bag, if available. Put the grains into " \
                                 "the center of the pot. Confirm?"
        elif(REMOVE_GRAINS_FLAG == 1):
            ingredient_flag = REMOVE_GRAINS_FLAG
            ingredient_message = "Remove the grains from the wort and squeeze the bag until most of the wort is out, " \
                                 "then remove from the pot. Confirm?"
        elif(ADD_LME_FLAG == 1):
            ingredient_flag = ADD_LME_FLAG
            ingredient_message = "Stir in the liquid malt extract (LME). Confirm?"
        elif(ADD_DME_FLAG == 1):
            ingredient_flag = ADD_DME_FLAG
            ingredient_message = "Stir in the dried malt extract (DME). Confirm?"
        elif(ADD_HOPS_1_FLAG == 1):
            ingredient_flag = ADD_HOPS_1_FLAG
            ingredient_message = "Add the 1st set of hops according to the recipe. Confirm?"
        elif(ADD_HOPS_2_FLAG == 1):
            ingredient_flag = ADD_HOPS_2_FLAG
            ingredient_message = "Add the 2nd set of hops according to the recipe. Confirm?"
        elif(ADD_HOPS_3_FLAG == 1):
            ingredient_flag = ADD_HOPS_3_FLAG
            ingredient_message = "Add the 3rd set of hops according to the recipe. Confirm?"
        elif(ADD_HOPS_4_FLAG == 1):
            ingredient_flag = ADD_HOPS_4_FLAG
            ingredient_message = "Add the 4th set of hops according to the recipe. Confirm?"
        elif(ADD_WHIRLFLOC_FLAG == 1):
            ingredient_flag = ADD_WHIRLFLOC_FLAG
            ingredient_message = "Add the whirlfloc tablet to the center of the pot. Confirm?"
        elif(COOLING_FLAG == 1):
            ingredient_flag = COOLING_FLAG
            ingredient_message = "Cooling session is active. Confirm?"
        elif(SOLENOID_FLAG == 1):
            ingredient_flag = SOLENOID_FLAG
            ingredient_message = "Wort is being solenoidd into the carboy. Confirm?"
        elif(ADD_YEAST_FLAG == 1):
            ingredient_flag = ADD_YEAST_FLAG
            ingredient_message = "Add the yeast to the wort, inside of the carboy. Prepare the wort for fermentation. Confirm?"
        else:
            ingredient_flag = 2
            ingredient_message = ""

        global next_ingredient
        if(SANITIZE_EQUIPMENT == 0):
            next_ingredient = "SANITIZE_EQUIPMENT"
        elif(ADD_WATER_FLAG == 0):
            next_ingredient = "ADD_WATER_FLAG"
        elif(ADD_GRAINS_FLAG == 0):
            next_ingredient = "ADD_GRAINS_FLAG"
        elif(REMOVE_GRAINS_FLAG == 0):
            next_ingredient = "REMOVE_GRAINS_FLAG"
        elif(ADD_LME_FLAG == 0):
            next_ingredient = "ADD_LME_FLAG"
        elif(ADD_DME_FLAG == 0):
            next_ingredient = "ADD_DME_FLAG"
        elif(ADD_HOPS_1_FLAG == 0):
            next_ingredient = "ADD_HOPS_1_FLAG"
        elif(ADD_HOPS_2_FLAG == 0):
            next_ingredient = "ADD_HOPS_2_FLAG"
        elif(ADD_HOPS_3_FLAG == 0):
            next_ingredient = "ADD_HOPS_3_FLAG"
        elif(ADD_HOPS_4_FLAG == 0):
            next_ingredient = "ADD_HOPS_4_FLAG"
        elif(ADD_WHIRLFLOC_FLAG == 0):
            next_ingredient = "ADD_WHIRLFLOC_FLAG"
        elif(COOLING_FLAG == 0):
            next_ingredient = "COOLING_FLAG"
        elif(SOLENOID_FLAG == 0):
            next_ingredient = "SOLENOID_FLAG"
        elif(ADD_YEAST_FLAG == 0):
            next_ingredient = "ADD_YEAST_FLAG"
        else:
            next_ingredient = "FINISH_FLAG"

        ingredient_label.config(text=str(ingredient_message))

        if(ingredient_flag == 1):
            try:
                print('brewing in session...')
                ingredient_label.after(1000, getIngredientFlag)
            except ValueError,e:
                print("Error %d: %s" % (e.args[0], e.args[1]))
        elif(ingredient_flag == 2):
            ingredient_start_time = time.time()
            checkBrewingSession()

    getIngredientFlag()

##########################################################################################################
## Update the current ingredient being added and the next ingredient being added
##########################################################################################################
def updateIngredientFlag(ingredient_add_window,ingredient_name,next_ingredient):
    try:
        ingredient_add_window.destroy()
    except ValueError,e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    sql = "UPDATE spartanbrewdb.brewing_sessions SET %s=2,%s=1 WHERE SPARTANBREW_ID='%s'" \
                % (ingredient_name,next_ingredient,SPARTANBREW_ID)

    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        db.commit()

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        db.rollback()

    global ingredient_start_time
    ingredient_start_time = time.time()
    checkBrewingSession()

##########################################################################################################
## Display test screen
##########################################################################################################
def displayTestScreen():
    test_window = Tkinter.Tk()
    test_window.overrideredirect(1)
    test_window.geometry("%dx%d+0+0" % (320, 240))

    action = lambda x = 1: test_window.destroy()
    button = Button(test_window, text='<- QUIT', command=action)
    button.grid(row=0, column=0, sticky=W+E+N+S)
    header = Label(test_window, text="Test Mode", bg="red")
    header.grid(row=0, column=1, columnspan=5, sticky=W+E+N+S)

    heating_element_label = Label(test_window, text="Heating Element")
    heating_element_label.grid(row=1, column=0, sticky=W)
    heating_element_data = Label(test_window, text="OFF", fg="red")
    heating_element_data.grid(row=1, column=5, sticky=W+E+N+S)
    action = lambda x = 1: turnOnComponent(heater,heating_element_data)
    button = Button(test_window, text='ON', command=action)
    button.grid(row=1, column=1, sticky=W+E+N+S)
    action = lambda x = 1: turnOffComponent(heater,heating_element_data)
    button = Button(test_window, text='OFF', command=action)
    button.grid(row=1, column=3, sticky=W+E+N+S)

    water_pump_label = Label(test_window, text="Water Pump")
    water_pump_label.grid(row=2, column=0, sticky=W)
    water_pump_data = Label(test_window, text="OFF", fg="red")
    water_pump_data.grid(row=2, column=5, sticky=W+E+N+S)
    action = lambda x = 1: turnOnComponent(cooler,water_pump_data)
    button = Button(test_window, text='ON', command=action)
    button.grid(row=2, column=1, sticky=W+E+N+S)
    action = lambda x = 1: turnOffComponent(cooler,water_pump_data)
    button = Button(test_window, text='OFF', command=action)
    button.grid(row=2, column=3, sticky=W+E+N+S)

    solenoid_label = Label(test_window, text="Solenoid Valve")
    solenoid_label.grid(row=3, column=0, sticky=W)
    solenoid_data = Label(test_window, text="OFF", fg="red")
    solenoid_data.grid(row=3, column=5, sticky=W+E+N+S)
    action = lambda x = 1: turnOnComponent(solenoid,solenoid_data)
    button = Button(test_window, text='ON', command=action)
    button.grid(row=3, column=1, sticky=W+E+N+S)
    action = lambda x = 1: turnOffComponent(solenoid,solenoid_data)
    button = Button(test_window, text='OFF', command=action)
    button.grid(row=3, column=3, sticky=W+E+N+S)

    temperature_label = Label(test_window, text="Temperature (F/C):")
    temperature_label.grid(row=4, column=0, sticky=W)
    temperature_data = Label(test_window, fg="red")
    temperature_data.grid(row=4, column=1, sticky=W+E+N+S)

    updateTestResults(test_window,heating_element_data,water_pump_data,solenoid_data,temperature_data)

    test_window.mainloop()

##########################################################################################################
## Update test results
##########################################################################################################
def updateTestResults(test_window,heating_element_data,water_pump_data,solenoid_data,temperature_data):
    def getData():
        TEMPERATURE_F,TEMPERATURE_C = 100.1,68.8
        temperature = "%.1f / %.1f" % (TEMPERATURE_F,TEMPERATURE_C) #getTemperature()
        temperature_data.config(text=str(temperature))
        print("%s" % temperature)

        temperature_data.after(1000,getData)
    getData()

##########################################################################################################
## Turn ON component
##########################################################################################################
def turnOnComponent(GPIOpin,label):
    print("Component ON, Port %d" % GPIOpin)
    # GPIO.output(GPIOpin, GPIO.HIGH)     # Set GPIO pin to HIGH (Turn on the components)
    label.config(text="ON")

##########################################################################################################
## Turn OFF component
##########################################################################################################
def turnOffComponent(GPIOpin,label):
    print("Component OFF, Port %d" % GPIOpin)
    # GPIO.output(GPIOpin, GPIO.LOW)     # Set GPIO pin to LOW (Turn off the components)
    label.config(text="OFF")

##########################################################################################################
## Turn ON heater
##########################################################################################################
def turnOnHeater():
    print("Heater ON, Port %d" % heater)
    # GPIO.output(heater, GPIO.HIGH)     # Set GPIO pin to HIGH (Turn on the components)

##########################################################################################################
## Turn OFF heater
##########################################################################################################
def turnOffHeater():
    print("Heater OFF, Port %d" % heater)
    # GPIO.output(heater, GPIO.LOW)     # Set GPIO pin to LOW (Turn off the components)

##########################################################################################################
## Turn ON cooler
##########################################################################################################
def turnOnCooler():
    print("Cooler ON, Port %d" % cooler)
    # GPIO.output(cooler, GPIO.HIGH)     # Set GPIO pin to HIGH (Turn on the components)

##########################################################################################################
## Turn OFF cooler
##########################################################################################################
def turnOffCooler():
    print("Cooler OFF, Port %d" % cooler)
    # GPIO.output(cooler, GPIO.LOW)     # Set GPIO pin to LOW (Turn off the components)

##########################################################################################################
## Turn ON cooler
##########################################################################################################
def turnOnSolenoid():
    print("Solenoid OPEN, Port %d" % solenoid)
    # GPIO.output(solenoid, GPIO.HIGH)     # Set GPIO pin to HIGH (Turn on the components)

##########################################################################################################
## Turn OFF cooler
##########################################################################################################
def turnOffSolenoid():
    print("Solenoid CLOSED, Port %d" % solenoid)
    # GPIO.output(solenoid, GPIO.LOW)     # Set GPIO pin to LOW (Turn off the components)

##########################################################################################################
# Main program
##########################################################################################################
def main():
    ## Set mode on GPIO pins
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)

    ## Set up appropriate GPIOs (Heater, Cooling, Solenoid)
    global heater, cooler, solenoid, unassigned
    heater = 13
    cooler = 6
    solenoid = 5
    unassigned = 21

    ## Initialize the GPIO pins connected to the components
    initializeGPIO(heater)
    initializeGPIO(cooler)
    initializeGPIO(solenoid)
    initializeGPIO(unassigned)
    #initializeTempSensor()

    ## Get SpartanBrew ID and Brewer ID
    global SPARTANBREW_ID
    SPARTANBREW_ID = getSpartanBrewID()
    print("SPARTANBREW_ID: %s" % SPARTANBREW_ID)

    global BREWER_ID
    BREWER_ID = getBrewerID()
    print("BREWER_ID: %s" % BREWER_ID)

    global zero_sec
    x = time.strptime('00:00:00',"%H:%M:%S")
    zero_sec = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()

    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (320, 240))
    label = Label(root, text="SpartanBrew", bg="red")
    label.grid(row=0, column=0, sticky=W+E+N+S)

    sql = "SELECT DISTINCT BEER_TYPE FROM spartanbrewdb.beer_styles ORDER BY BEER_TYPE ASC"
    try:
        checkSpartanBrewDB()
        cursor.execute(sql)
        results = cursor.fetchall()
        row_position = 0
        for row in results:
            row_position += 1
            beer_type = row[0]
            action = lambda x = beer_type: getBeerStyles(x)
            button = Button(root, text=beer_type, command=action)
            button.grid(row=row_position, column=0, sticky=W+E+N+S)

        row_position += 1
        action = lambda x = beer_type: displayTestScreen()
        button = Button(root, text="TEST", command=action)
        button.grid(row=row_position, column=0, sticky=W+E+N+S)

    except MySQLdb.Error, e:
        print("Error %d: %s" % (e.args[0], e.args[1]))

    root.after(1000,checkBrewingSession)
    root.mainloop()

root = Tkinter.Tk()
main()
