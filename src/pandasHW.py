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

def collectData(myURL):
    response = requests.get(myURL)
    response.raise_for_status() # check for errors
    myhtml = response.text
    print(f'myhtml is {len(myhtml)} characters long')
    stationsInfo = re.findall(r"<a href=\"http:\/\/forecast\.weather\.gov\/data\/obhistory\/(?P<kname>[A-Z]{4})\.html\" class=\"link\">(?P<name>[a-zA-Z]+(?!Mun)[a-zA-Z ]+)", myhtml)
    print(f'Found {len(stationsInfo)} recording stations')
    stationDict = {"Kname":[],"Name":[]}
    for station in stationsInfo:
        stationDict["Kname"].append(station[0])
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
            stationDict["Name"].append("Spencer")
    df = pd.DataFrame(stationDict)
    print(f"this is Kname size: {df.groupby('Kname').size()}")
    print(f"this is Name size: {df.groupby('Name').size()}")
    print(df)

if __name__ == '__main__':
    """
    Runs if file called as script as opposed to being imported as a library
    """
    print(collectData("https://forecast.weather.gov/obslocal.php?warnzone=IAZ031&local_place=Sioux%20City%20IA&zoneid=CDT&offset=18000"))

    
