
# USE: To find availability slot for next week
#      Better to run once every minute (API call limit 100/min)
#      >> python3 vaccine.py
#
# Author: Vinothkumar Ratnakumar
#
# APIs TO GET DISTRICT ID:
# STATE ID      => https://cdn-api.co-vin.in/api/v2/admin/location/states
# TN STATE ID   => 31 (USE STATE ID TO GET DISTRICT ID)
# DISTRICT ID   => https://cdn-api.co-vin.in/api/v2/admin/location/districts/31
# CHENNAI ID    => ["571"]
# BANGALORE IDS => ["265", "294", "276", "291", "277", "292"]

# for i in {1..10}; do python3 vaccine.py; sleep 20; done # run 10 times every 20 secs

# SAMPLE OUTPUT - START
# ****
# ('16/05/2021 [District:571]  Total Slots Available[Age:45]: ', '830')
#
# 1  . Hospital Name[600078]: Nesapakkam UPHC                         , Availability:6   , Vaccine:COVISHIELD
# 2  . Hospital Name[600021]: Korukkupet UPHC                         , Availability:8   , Vaccine:COVISHIELD
# 3  . Hospital Name[600050]: Padi UCHC - COVISHIELD                  , Availability:1   , Vaccine:COVISHIELD
# 4  . Hospital Name[600081]: Apollo Hospital Tondiarpet              , Availability:97  , Vaccine:COVISHIELD
# 5  . Hospital Name[600034]: Pushpa Nagar UPHC                       , Availability:10  , Vaccine:COVISHIELD
# 6  . Hospital Name[600034]: Pushpa Nagar UPHC                       , Availability:10  , Vaccine:COVISHIELD
# 7  . Hospital Name[600034]: Pushpa Nagar UPHC                       , Availability:10  , Vaccine:COVISHIELD
#****
# SAMPLE OUTPUT - END

# IMPORTS
import urllib.request
import json
from datetime import datetime, timedelta
import logging
import os
from sys import platform

# -------------------------------------
# IMP: CHANGE BELOW VARIABLS AS PER USE
# -------------------------------------
district = ["571"] # ["265", "294", "276", "291", "277", "292"] # ["554", "549"] Global variable.
debug = True       # !debug will log to belowfile. Can be used for cronjobs
logfile = "/cVac/vaccine.log" # Change if debug = False
age = 18    # min_age 18
#age = 45   # min_age 45
numDays = 7 # Gets output for 7 days startinf today
prefVaccine = "AnyVaccine"  #Preffered Vaccine "AnyVaccine"/"COVISHIELD"/"COVAXIN"
#prefVaccine = "COVAXIN"
# -------------------------------------
# IMP: CHANGE ABOVE VARIABLS AS PER USE
# -------------------------------------

# GLOBALS
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# INIT LOGGER
def getLogger():
    file_handler = logging.FileHandler(logfile) 
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

def initLogger():
    if False == debug:
        getLogger()

# METHOD TO CREATE BEEP SOUND
def beepsound():
    if platform == "win32":
        import winsound
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
    else:
        # currently tested for Mac OSXsss
        beetStr = "echo Vaccine available on " + today.strftime('%d/%m/%Y') + " '\a';sleep 0.2;"
        beep =  lambda x: os.system(beetStr  * x)
        beep(10)

# RESULT TO LOGGER FILE
def resultLogger(header, total_avail, result_str):
    if total_avail != 0:
        logger.info("****")
        logger.info(header)
        if result_str != "":
            logger.info(result_str)
            logger.info("****")
            beepsound()
    else:
        logger.info(header)
        logger.handlers[0].flush()
        return 

# RESULT TO CONSOLE
def resultConsole(header, total_avail, result_str):
    if total_avail != 0:
        print("****")
        print(header)
        if result_str != "":
            print(result_str)
            print("****")
            beepsound()
    else:
        print(header)

def printResult(header, total_avail=0, result_str=''):
    if False == debug:
        resultLogger(header, total_avail, result_str)
    else:
        resultConsole(header, total_avail, result_str)


# CUSTOM PRINT FOR EVERY AVAILABLE SLOT
def formatSlot(slot, index, result_str, hosp, pincode):
    result_str += str(index).ljust(3) + ". Hospital Name["+ str(pincode) + "]: " + hosp.ljust(40)
    result_str += ", Availability:" + str(slot["available_capacity"]).ljust(4)
    result_str += ", Vaccine:" +  slot["vaccine"].ljust(20) + "\n"
    return result_str


def getQueryResult(date, districtID):
    reg_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + districtID + "&date=" + date
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
    req = urllib.request.Request(url=reg_url, headers=headers)
    try:
        data = json.loads(urllib.request.urlopen(req).read()) 
    except:
        return None
    return data

# MAIN METHOD TO GET SLOTS
def getVaccineTimeslots(today, districtID):
    date = today.strftime("%d/%m/%Y")
    data = getQueryResult(date, districtID)
    if data == None:
        header = today.strftime('%d/%m/%Y [UnableToQuery]') 
        printResult(header)
        return
    result_str, index, total_avail  = "\n", 0, 0
    total_avail=0
    for center in data['centers']:
        hosp = center['name']
        for slot in center['sessions']:
            if slot["available_capacity"] >0 and slot['min_age_limit'] <=age:
                if prefVaccine == "AnyVaccine" or slot["vaccine"] == prefVaccine :
                    total_avail = total_avail + slot['available_capacity']
                    index += 1
                    result_str = formatSlot(slot, index, result_str, hosp, center["pincode"])

    header = today.strftime('%d/%m/%Y [District:') + districtID + "]  Total Slots Available[Age:" + str(age) + "][Vaccine:" + prefVaccine + "]: ", str(total_avail)
    printResult(header, total_avail, result_str)

if __name__ == '__main__':
    today = datetime.today()
    initLogger()

    for d in district:
        for i in range(numDays):
            dayOfChoice = today + timedelta(days=i)
            getVaccineTimeslots(dayOfChoice, d)
