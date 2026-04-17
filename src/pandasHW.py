"""
pandasHW.py
====================================
This is the homework that uses pandas and regex to get data on weather of Sioux City and information from that.

| Author: Eein McKinley
| Date: 2026 April 17
"""


import pandas as pd
import numpy as np
from datetime import datetime, UTC
import re
import requests
import string
import matplotlib.pyplot as plt
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase

def main():
    """
    This collects the data from the National Weather Service in the Siouxland area 
    and turns it into a pandas dataframe and shows statistics about the weather.
    """
    #Going online to get weather information
    response = requests.get("https://forecast.weather.gov/obslocal.php?warnzone=IAZ031&local_place=Sioux%20City%20IA&zoneid=CDT&offset=18000")
    response.raise_for_status() # check for errors
    myhtml = response.text
    #Using regex to extract information from html file
    stationsInfo = re.findall(r"<a href=\"http:\/\/forecast\.weather\.gov\/data\/obhistory\/(?P<Kname>[A-Z]{4})\.html\" class=\"link\">(?P<Name>[a-zA-Z ]+),?-?[A-Za-z <]+/a><\/td>\n\s+<td class=\"time\">(?P<Time>\d{2}:\d{2})<\/td>\n\s+<td class=\"wx\">[A-Za-z ]+<\/td>\n\s+<td>(?P<Temp>\d+)</td>\n\s+<td>\d+</td>\n\s+<td>(?P<Humidity>\d+)</td>\n\s+<td class=\"wind\">\s+[A-Z]+\n\s+\d+\n[G0-9 ]+</td>\n\s+<td>(?P<Pressure>\d+.\d+)", myhtml)
    print(f'Found {len(stationsInfo)} recording stations')
    #Creation of a dictionary that will be used for dataframe creation
    stationDict = {"Kname":[],"Name":[],"Time":[],"Temp":[],"Humidity":[],"Pressure":[]}
    for station in stationsInfo:
        stationDict["Kname"].append(station[0])
        stationDict["Name"].append(nameNormalizing(station[1]))
        #The final details regarding the dictionary
        stationDict["Time"].append((station[2]))
        stationDict["Temp"].append(float(station[3]))
        stationDict["Humidity"].append(float(station[4]))
        stationDict["Pressure"].append(float(station[5]))
    #Creation of dictionary
    df = pd.DataFrame(stationDict)
    print(df)
    #DataFrame manipulation
    pd.to_datetime(df["Time"], format="%H:%M")
    #Info is orgainzed: [avg,std,median,min,max,frequency]
    tempInfo = [df["Temp"].mean().item(),df["Temp"].std().item(),df["Temp"].median().item(),df["Temp"].min().item(),df["Temp"].max().item(),df["Temp"].value_counts()]
    humidInfo = [df["Humidity"].mean().item(),df["Humidity"].std().item(),df["Humidity"].median().item(),df["Humidity"].min().item(),df["Humidity"].max().item(),df["Humidity"].value_counts()]
    pressInfo = [df["Pressure"].mean().item(),df["Pressure"].std().item(),df["Pressure"].median().item(),df["Pressure"].min().item(),df["Pressure"].max().item(),df["Pressure"].value_counts()]
    showStats(tempInfo,humidInfo,pressInfo)
    ax1 = plt.subplot(3,1,1)
    ax2 = plt.subplot(3,1,2)
    ax3 = plt.subplot(3,1,3)
    ax1.boxplot(df["Temp"],orientation="horizontal")
    ax1.set_title("Weather Statistics from Weather Stations around Siouxland")
    ax1.set_xlabel("Temperature at Each Station (°F)")
    ax2.boxplot(df["Humidity"],orientation="horizontal")
    ax2.set_xlabel("Humidity at Each Station (%)")
    ax3.boxplot(df["Pressure"],orientation="horizontal")
    ax3.set_xlabel("Pressure at Each Station (in)")
    plt.tight_layout()
    plt.show()
    
    

def nameNormalizing(name):
    """
    Normalizes names for better use in the data frame

    Parameters
    ----------
    name: str
        The name that is being normalized

    Returns
    ------------
    str
        The normalized name
    """
    #Name changing shenanagins.
    containsLower = False
    containsUpper = False
    for letter in lowercase:
        if letter in name:
            containsLower = True
            break
    for letter in uppercase:
        if letter in name:
            containsUpper = True
            break
    if not (containsUpper and containsLower):
        if containsUpper:
            stationNameWords = name.split()
            stationName = ""
            for word in stationNameWords:
                stationName = word[0] + word[1:].lower()
            return stationName
        else:
            stationNameWords = name.split()
            stationName = ""
            for word in stationNameWords:
                stationName = word[0].upper() + word[1:]
            return stationName
    elif name != "Spencer Municipal Airport":
        return name
    else:
        #Had to Hard Code this one or else my sanity would be tested
        return "Spencer"
        
def showStats(tempInfo,humidInfo,pressInfo):
    """
    Prints statistics about the weather in the Siouxland area in the terminal

    Parameters
    -----------
    tempInfo : list
        Statistics regarding the temperature that are displayed

    -----------
    humidInfo : list
        Statistics regarding the humidity that are displayed

    -----------
    pressInfo : list
        Statistics regarding the pressure that are displayed    

    """
    print(f"\tTemp\tHumid\tPressure")
    for x in range(len(tempInfo)):
        if x == 0:
            print("Avg.:",end="")
        if x == 1:
            print("St.D.:",end="")
        if x == 2:
            print("Median:",end="")
        if x == 3:
            print("Min:",end="")
        if x == 4:
            print("Max:",end="")
        if x <= 4:
            print(f"\t{tempInfo[x]:.2f}\t{humidInfo[x]:.2f}\t{pressInfo[x]:.2f}")
        else:
            print(f"\n{tempInfo[x]}\n\n{humidInfo[x]}\n\n{pressInfo[x]}")

if __name__ == '__main__':
    """
    Runs if file called as script as opposed to being imported as a library
    """
    main()

    
