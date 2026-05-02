#!/usr/bin/python3
import sys
import math
import time
import os
from pprint import pprint
from FlightRadar24.api import FlightRadar24API
fr_api = FlightRadar24API()

DataFile = "/mem/fr24_data"
LiveFile = "/mem/fr24_live_data"

def getDate(secs):
    if secs == None:
        return None

    return time.strftime("%Y-%m-%d", time.localtime(secs))

def getTime(secs):
    if secs == None:
        return None

    return time.strftime("%H%M", time.localtime(secs))

def fixCallsign(callsign):
    if callsign == "ABLE1E":
        callsign = "ABLE10"

    if len(callsign) < 4 or callsign[0] != "G":
        return callsign

    if callsign[1] == "-":
        suffix = callsign[2:]
    else:
        suffix = callsign[1:]

    if suffix == "UCAN":
        callsign = "ABLE01"
    elif suffix == "OMJA":
        callsign = "ABLE02"
    elif suffix == "BCIR":
        callsign = "ABLE03"
    elif suffix == "BMFP":
        callsign = "ABLE04"
    elif suffix == "IDOO":
        callsign = "ABLE05"
    elif suffix == "SIXE":
        callsign = "ABLE06"
    elif suffix == "IDID":
        callsign = "ABLE07"
    elif suffix == "SAUP":
        callsign = "ABLE08"
    elif suffix == "OFTR":
        callsign = "ABLE10"
    elif suffix == "XXXXX":
        callsign = "ABLE11"
    elif suffix == "BRUD":
        callsign = "ABLE12"
    elif suffix == "CDMA":
        callsign = "ABLE14"

    return callsign

def printFlight(i, flight):
        #print("Flight", i, ":")
        #pprint(vars(flight))
        if flight != None:
            print(fixCallsign(flight.callsign), "(", flight.aircraft_code, ") hdg:", flight.heading, "spd", flight.ground_speed, "alt:", flight.altitude)

def getFlights(bounds):
    global lastAbleData
    global lastAbleLiveData

    success = False
    while not success:
        try:
            flights = fr_api.get_flights(bounds = bounds)
            success = True
        except:
            success = False
            time.sleep(2)

    able = []
    for i in range(16):
        able.append(None)

    for flight in flights:
        if flight.callsign == "":
            callsign = fixCallsign(flight.registration)
        else:
            callsign = fixCallsign(flight.callsign)

        if callsign[:4] != "ABLE":
            continue

        try:
            ableNum = int(callsign[4:])
        except:
            ableNum = 99

        if ableNum == 0 or ableNum > 16:
            continue

        able[ableNum - 1] = flight
        #printFlight(ableNum, flight)

    ableData = ""
    ableLiveData = ""
    for i in range(16):
        # Only show ABLE12 on map if no previous ABLES found
        if i == 11 and ableLiveData == "":
            ableLiveData += ableLive(i + 1, able[i])

        if i > 11:
            continue

        if i > 0:
            ableData += ","

        alt = ableAlt(able[i])
        ableData += alt

    if ableData != lastAbleData:
        with open(DataFile, "w") as file:
            file.write(f"{ableData}\n")
        lastAbleData = ableData

    if ableLiveData != lastAbleLiveData:
        with open(LiveFile, "w") as file:
            file.write(f"{ableLiveData}\n")
        lastAbleLiveData = ableLiveData

def ableAlt(flight):
    if flight == None:
        return "--"

    if flight.altitude > 9999:
        return "99"

    return f"{round(flight.altitude / 100):02d}"

def ableLive(num, flight):
    if flight == None:
        return ""

    try:
        flightInfo = fr_api.get_flight_details(flight)
    except:
        flightInfo = None

    if flightInfo == None:
        trail = None
        typeCode = flight.aircraft_code
    else:
        trail = flightInfo.get("trail")
        try:
            typeCode = flightInfo["aircraft"]["model"]["code"]
        except:
            typeCode = flight.aircraft_code

    if trail == None:
        lat = flight.latitude
        lon = flight.longitude
    else:
        lat = trail[0]["lat"]
        lon = trail[0]["lng"]

    return f"#{num},{typeCode},{lat},{lon},{flight.heading},{flight.altitude},{flight.ground_speed}"

# --------
# Main
# --------

bounds = "60,49,-11,3"

print("Running")

lastAbleData = None
lastAbleLiveData = None

while True:
    getFlights(bounds)
    time.sleep(3)
