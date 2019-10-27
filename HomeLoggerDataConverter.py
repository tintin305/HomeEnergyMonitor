#!/usr/bin/env python

import requests
import pandas as pd
import string
import datetime
from time import mktime
import json

L1Cols = list(range(3,14))
L2Cols = list(range(14,25))
L3Cols = list(range(25,36))

header = ['Max.Volt','Max.Time','Avg.Volt','Max.Amp','Max.Time','Avg.Amp','KWHours','Max.KW','Max.Time','Avg.KW','Avg.PF']
L1data = pd.read_csv('HomeLoggerData.csv', skiprows=10, usecols=L1Cols)
L2data = pd.read_csv('HomeLoggerData.csv', skiprows=10, usecols=L2Cols)
L3data = pd.read_csv('HomeLoggerData.csv', skiprows=10, usecols=L3Cols)

# Renaming the columns for the headers, otherwise it introduces numbers as the original has duplicate column names.
L1data.columns = header
L2data.columns = header
L3data.columns = header


dateCols = list(range(0,3))
dateData = pd.read_csv('HomeLoggerData.csv', skiprows=10, usecols=dateCols)
dateData.columns = ['Number', 'Date', 'End Time']


# End time corresponds to the time values for the averaged parameters.
# Each time there is a 'max' parameter recorded, the time is alongside it, to its right.

averageParameters = ['Avg.Volt', 'Avg.Amp', 'KWHours', 'Avg.KW', 'Avg.PF']
L1Average = pd.concat([dateData, L1data[averageParameters]], axis=1, ignore_index=False)
L2Average = pd.concat([dateData, L2data[averageParameters]], axis=1, ignore_index=False)
L3Average = pd.concat([dateData, L3data[averageParameters]], axis=1, ignore_index=False)


for row, index in L1Average.iterrows():
    date = index['Date']
    time = index['End Time']

    datetime_str = str(date) + ' ' + str(time)
    datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    unixTime = str(mktime(datetime_object.timetuple()))[:-2]
    
    for item in averageParameters:
        payload = {}
        payload['metric'] = 'L1.' + str(item)
        payload['timestamp'] = str(unixTime)
        payload['value'] = str(index[item])
        tags = {}
        tags['Measurement'] = str(item)
        payload['tags'] = tags

        url = 'http://146.141.16.82:4242/api/put?summary'
        jsonPayload = json.dumps(payload)
        response = requests.post(url, data=jsonPayload)


for row, index in L2Average.iterrows():
    date = index['Date']
    time = index['End Time']

    datetime_str = str(date) + ' ' + str(time)
    datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    unixTime = str(mktime(datetime_object.timetuple()))[:-2]
    
    for item in averageParameters:
        payload = {}
        payload['metric'] = 'L2.' + str(item)
        payload['timestamp'] = str(unixTime)
        payload['value'] = str(index[item])
        tags = {}
        tags['Measurement'] = str(item)
        payload['tags'] = tags

        url = 'http://146.141.16.82:4242/api/put?summary'
        jsonPayload = json.dumps(payload)
        response = requests.post(url, data=jsonPayload)



for row, index in L3Average.iterrows():
    date = index['Date']
    time = index['End Time']

    datetime_str = str(date) + ' ' + str(time)
    datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
    unixTime = str(mktime(datetime_object.timetuple()))[:-2]
    
    for item in averageParameters:
        payload = {}
        payload['metric'] = 'L3.' + str(item)
        payload['timestamp'] = str(unixTime)
        payload['value'] = str(index[item])
        tags = {}
        tags['Measurement'] = str(item)
        payload['tags'] = tags

        url = 'http://146.141.16.82:4242/api/put?summary'
        jsonPayload = json.dumps(payload)
        response = requests.post(url, data=jsonPayload)

