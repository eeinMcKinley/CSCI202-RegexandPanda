"""
pandasHW.py
====================================
This is the homework that uses pandas and regex to get data on weather of Sioux City and information from that.

| Author: Eein McKinley
| Date: 2026 April 17
"""


import pandas as pd
import re
import requests
import string
import matplotlib.pyplot as plt
from string import ascii_lowercase as lowercase
from string import ascii_uppercase as uppercase
#Useful for making boxplots
#plt.boxplot(data,vert=True)

def collectData():
    """
    This collects the data from the National Weather Service in the Siouxland area and turns it into a pandas dataframe.
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
        #Name changing shenanagins.
        containsLower = False
        containsUpper = False
        for letter in lowercase:
            if letter in station[1]:
                containsLower = True
                break
        for letter in uppercase:
            if letter in station[1]:
                containsUpper = True
                break
        if not (containsUpper and containsLower):
            if containsUpper:
                stationNameWords = station[1].split()
                stationName = ""
                for word in stationNameWords:
                    stationName = word[0] + word[1:].lower()
                stationDict["Name"].append(stationName)
            else:
                stationNameWords = station[1].split()
                stationName = ""
                for word in stationNameWords:
                    stationName = word[0].upper() + word[1:]
                stationDict["Name"].append(stationName)
        elif station[1] != "Spencer Municipal Airport":
            stationDict["Name"].append(station[1])
        else:
            #Had to Hard Code this one or else my sanity would be tested
            stationDict["Name"].append("Spencer")
        #The final details regarding the dictionary
        stationDict["Time"].append(station[2])
        stationDict["Temp"].append(station[3])
        stationDict["Humidity"].append(station[4])
        stationDict["Pressure"].append(station[5])
    #Creation of dictionary
    df = pd.DataFrame(stationDict)
    print(df)

if __name__ == '__main__':
    """
    Runs if file called as script as opposed to being imported as a library
    """
    print(collectData())

    
