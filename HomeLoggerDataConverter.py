#!/usr/bin/env python

import requests
import pandas as pd
import string
import datetime
from time import mktime
import json
import pytz

def importMainData():
    L1Cols = list(range(3,37))
    L2Cols = list(range(37,71))
    L3Cols = list(range(71,105))

    header = ['Min.Volt','Min.Time','Max.Volt','Max.Time','Avg.Volt','AmpHours','Min.Amp','Min.Time','Max.Amp','Max.Time','Avg.Amp','KWHours','Min.KW','Min.Time','Max.KW','Max.Time','Avg.KW','KVAHours','Min.KVA','Min.Time','Max.KVA','Max.Time','Avg.KVA','Min.PF','Min.Time','Max.PF','Max.Time','Avg.PF','KVARHours','Min.KVAR','Min.Time','Max.KVAR','Max.Time','Avg.KVAR']
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

    return L1data, L2data, L3data, dateData


def importAverageParams(L1data, L2data, L3data, dateData):
    # End time corresponds to the time values for the averaged parameters.
    # Each time there is a 'max' parameter recorded, the time is alongside it, to its right.

    averageParameters = ['Avg.Volt', 'Avg.Amp', 'Avg.KW', 'Avg.KVA', 'Avg.PF', 'Avg.KVAR']
    L1Average = pd.concat([dateData, L1data[averageParameters]], axis=1, ignore_index=False)
    L2Average = pd.concat([dateData, L2data[averageParameters]], axis=1, ignore_index=False)
    L3Average = pd.concat([dateData, L3data[averageParameters]], axis=1, ignore_index=False)


    for row, index in L1Average.iterrows():
        date = index['Date']
        time = index['End Time']

        # Doing the timezone conversion, as the final mktime timetuple needs a UTC time (https://stackoverflow.com/questions/79797/how-to-convert-local-time-string-to-utc).
        localTimezone = pytz.timezone('Africa/Johannesburg')
        datetime_str = str(date) + ' ' + str(time)
        datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        localTime = localTimezone.localize(datetime_object, is_dst=None)
        utcTime = localTime.astimezone(pytz.utc)
        unixTime = str(mktime(utcTime.timetuple()))[:-2]


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

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)


    for row, index in L2Average.iterrows():
        date = index['Date']
        time = index['End Time']

        localTimezone = pytz.timezone('Africa/Johannesburg')
        datetime_str = str(date) + ' ' + str(time)
        datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        localTime = localTimezone.localize(datetime_object, is_dst=None)
        utcTime = localTime.astimezone(pytz.utc)
        unixTime = str(mktime(utcTime.timetuple()))[:-2]
        
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

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)



    for row, index in L3Average.iterrows():
        date = index['Date']
        time = index['End Time']

        localTimezone = pytz.timezone('Africa/Johannesburg')
        datetime_str = str(date) + ' ' + str(time)
        datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        localTime = localTimezone.localize(datetime_object, is_dst=None)
        utcTime = localTime.astimezone(pytz.utc)
        unixTime = str(mktime(utcTime.timetuple()))[:-2]
        
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
            
            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)

    return None

def importMinimumParams(L1data, L2data, L3data, dateData):

    L1MinVoltage = pd.concat([dateData['Date'], L1data.iloc[:,0:2]], axis=1, ignore_index=False)
    L1MinAmp = pd.concat([dateData['Date'], L1data.iloc[:,6:8]], axis=1, ignore_index=False)
    L1MinKW = pd.concat([dateData['Date'], L1data.iloc[:,12:14]], axis=1, ignore_index=False)
    L1MinKVA = pd.concat([dateData['Date'], L1data.iloc[:,18:20]], axis=1, ignore_index=False)
    L1MinPF = pd.concat([dateData['Date'], L1data.iloc[:,23:25]], axis=1, ignore_index=False)
    L1MinKVAR = pd.concat([dateData['Date'], L1data.iloc[:,29:31]], axis=1, ignore_index=False)

    minVectorPhase1 = [L1MinVoltage, L1MinAmp, L1MinKW, L1MinKVA, L1MinPF, L1MinKVAR]


    for item in minVectorPhase1:
        currentMetric = item.columns.values[1]

        for row, index in item.iterrows():
            date = index['Date']
            time = index['Min.Time']

            localTimezone = pytz.timezone('Africa/Johannesburg')
            datetime_str = str(date) + ' ' + str(time)
            datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            localTime = localTimezone.localize(datetime_object, is_dst=None)
            utcTime = localTime.astimezone(pytz.utc)
            unixTime = str(mktime(utcTime.timetuple()))[:-2]
                
            payload = {}
            payload['metric'] = 'L1.' + str(currentMetric)
            payload['timestamp'] = str(unixTime)
            payload['value'] = str(index[currentMetric])
            tags = {}
            tags['Measurement'] = str(currentMetric)
            payload['tags'] = tags

            url = 'http://146.141.16.82:4242/api/put?summary'
            jsonPayload = json.dumps(payload)

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)


    L2MinVoltage = pd.concat([dateData['Date'], L2data.iloc[:,0:2]], axis=1, ignore_index=False)
    L2MinAmp = pd.concat([dateData['Date'], L2data.iloc[:,6:8]], axis=1, ignore_index=False)
    L2MinKW = pd.concat([dateData['Date'], L2data.iloc[:,12:14]], axis=1, ignore_index=False)
    L2MinKVA = pd.concat([dateData['Date'], L2data.iloc[:,18:20]], axis=1, ignore_index=False)
    L2MinPF = pd.concat([dateData['Date'], L2data.iloc[:,23:25]], axis=1, ignore_index=False)
    L2MinKVAR = pd.concat([dateData['Date'], L2data.iloc[:,29:31]], axis=1, ignore_index=False)

    minVectorPhase2 = [L2MinVoltage, L2MinAmp, L2MinKW, L2MinKVA, L2MinPF, L2MinKVAR]

    for item in minVectorPhase2:
        currentMetric = item.columns.values[1]

        for row, index in item.iterrows():
            date = index['Date']
            time = index['Min.Time']

            localTimezone = pytz.timezone('Africa/Johannesburg')
            datetime_str = str(date) + ' ' + str(time)
            datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            localTime = localTimezone.localize(datetime_object, is_dst=None)
            utcTime = localTime.astimezone(pytz.utc)
            unixTime = str(mktime(utcTime.timetuple()))[:-2]

            payload = {}
            payload['metric'] = 'L2.' + str(currentMetric)
            payload['timestamp'] = str(unixTime)
            payload['value'] = str(index[currentMetric])
            tags = {}
            tags['Measurement'] = str(currentMetric)
            payload['tags'] = tags

            url = 'http://146.141.16.82:4242/api/put?summary'
            jsonPayload = json.dumps(payload)

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)

    L3MinVoltage = pd.concat([dateData['Date'], L3data.iloc[:,0:2]], axis=1, ignore_index=False)
    L3MinAmp = pd.concat([dateData['Date'], L3data.iloc[:,6:8]], axis=1, ignore_index=False)
    L3MinKW = pd.concat([dateData['Date'], L3data.iloc[:,12:14]], axis=1, ignore_index=False)
    L3MinKVA = pd.concat([dateData['Date'], L3data.iloc[:,18:20]], axis=1, ignore_index=False)
    L3MinPF = pd.concat([dateData['Date'], L3data.iloc[:,23:25]], axis=1, ignore_index=False)
    L3MinKVAR = pd.concat([dateData['Date'], L3data.iloc[:,29:31]], axis=1, ignore_index=False)

    minVectorPhase3 = [L3MinVoltage, L3MinAmp, L3MinKW, L3MinKVA, L3MinPF, L3MinKVAR]

    for item in minVectorPhase3:
        currentMetric = item.columns.values[1]

        for row, index in item.iterrows():
            date = index['Date']
            time = index['Min.Time']

            localTimezone = pytz.timezone('Africa/Johannesburg')
            datetime_str = str(date) + ' ' + str(time)
            datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            localTime = localTimezone.localize(datetime_object, is_dst=None)
            utcTime = localTime.astimezone(pytz.utc)
            unixTime = str(mktime(utcTime.timetuple()))[:-2]
                
            payload = {}
            payload['metric'] = 'L3.' + str(currentMetric)
            payload['timestamp'] = str(unixTime)
            payload['value'] = str(index[currentMetric])
            tags = {}
            tags['Measurement'] = str(currentMetric)
            payload['tags'] = tags

            url = 'http://146.141.16.82:4242/api/put?summary'
            jsonPayload = json.dumps(payload)

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)


    return None


def importMaximumParams(L1data, L2data, L3data, dateData):

    L1MaxVoltage = pd.concat([dateData['Date'], L1data.iloc[:,2:4]], axis=1, ignore_index=False)
    L1MaxAmp = pd.concat([dateData['Date'], L1data.iloc[:,8:10]], axis=1, ignore_index=False)
    L1MaxKW = pd.concat([dateData['Date'], L1data.iloc[:,14:16]], axis=1, ignore_index=False)
    L1MaxKVA = pd.concat([dateData['Date'], L1data.iloc[:,20:22]], axis=1, ignore_index=False)
    L1MaxPF = pd.concat([dateData['Date'], L1data.iloc[:,25:27]], axis=1, ignore_index=False)
    L1MaxKVAR = pd.concat([dateData['Date'], L1data.iloc[:,31:33]], axis=1, ignore_index=False)

    maxVectorPhase1 = [L1MaxVoltage, L1MaxAmp, L1MaxKW, L1MaxKVA, L1MaxPF, L1MaxKVAR]

    for item in maxVectorPhase1:
        currentMetric = item.columns.values[1]

        for row, index in item.iterrows():
            date = index['Date']
            time = index['Max.Time']

            localTimezone = pytz.timezone('Africa/Johannesburg')
            datetime_str = str(date) + ' ' + str(time)
            datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            localTime = localTimezone.localize(datetime_object, is_dst=None)
            utcTime = localTime.astimezone(pytz.utc)
            unixTime = str(mktime(utcTime.timetuple()))[:-2]
                
            payload = {}
            payload['metric'] = 'L1.' + str(currentMetric)
            payload['timestamp'] = str(unixTime)
            payload['value'] = str(index[currentMetric])
            tags = {}
            tags['Measurement'] = str(currentMetric)
            payload['tags'] = tags

            url = 'http://146.141.16.82:4242/api/put?summary'
            jsonPayload = json.dumps(payload)

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)


    L2MaxVoltage = pd.concat([dateData['Date'], L2data.iloc[:,2:4]], axis=1, ignore_index=False)
    L2MaxAmp = pd.concat([dateData['Date'], L2data.iloc[:,8:10]], axis=1, ignore_index=False)
    L2MaxKW = pd.concat([dateData['Date'], L2data.iloc[:,14:16]], axis=1, ignore_index=False)
    L2MaxKVA = pd.concat([dateData['Date'], L2data.iloc[:,20:22]], axis=1, ignore_index=False)
    L2MaxPF = pd.concat([dateData['Date'], L2data.iloc[:,25:27]], axis=1, ignore_index=False)
    L2MaxKVAR = pd.concat([dateData['Date'], L2data.iloc[:,31:33]], axis=1, ignore_index=False)

    maxVectorPhase2 = [L2MaxVoltage, L2MaxAmp, L2MaxKW, L2MaxKVA, L2MaxPF, L2MaxKVAR]

    for item in maxVectorPhase2:
        currentMetric = item.columns.values[1]

        for row, index in item.iterrows():
            date = index['Date']
            time = index['Max.Time']

            localTimezone = pytz.timezone('Africa/Johannesburg')
            datetime_str = str(date) + ' ' + str(time)
            datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            localTime = localTimezone.localize(datetime_object, is_dst=None)
            utcTime = localTime.astimezone(pytz.utc)
            unixTime = str(mktime(utcTime.timetuple()))[:-2]
                
            payload = {}
            payload['metric'] = 'L2.' + str(currentMetric)
            payload['timestamp'] = str(unixTime)
            payload['value'] = str(index[currentMetric])
            tags = {}
            tags['Measurement'] = str(currentMetric)
            payload['tags'] = tags

            url = 'http://146.141.16.82:4242/api/put?summary'
            jsonPayload = json.dumps(payload)

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)

    L3MaxVoltage = pd.concat([dateData['Date'], L3data.iloc[:,2:4]], axis=1, ignore_index=False)
    L3MaxAmp = pd.concat([dateData['Date'], L3data.iloc[:,8:10]], axis=1, ignore_index=False)
    L3MaxKW = pd.concat([dateData['Date'], L3data.iloc[:,14:16]], axis=1, ignore_index=False)
    L3MaxKVA = pd.concat([dateData['Date'], L3data.iloc[:,20:22]], axis=1, ignore_index=False)
    L3MaxPF = pd.concat([dateData['Date'], L3data.iloc[:,25:27]], axis=1, ignore_index=False)
    L3MaxKVAR = pd.concat([dateData['Date'], L3data.iloc[:,31:33]], axis=1, ignore_index=False)

    maxVectorPhase2 = [L3MaxVoltage, L3MaxAmp, L3MaxKW, L3MaxKVA, L3MaxPF, L3MaxKVAR]

    for item in maxVectorPhase3:
        currentMetric = item.columns.values[1]

        for row, index in item.iterrows():
            date = index['Date']
            time = index['Max.Time']

            localTimezone = pytz.timezone('Africa/Johannesburg')
            datetime_str = str(date) + ' ' + str(time)
            datetime_object = datetime.datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            localTime = localTimezone.localize(datetime_object, is_dst=None)
            utcTime = localTime.astimezone(pytz.utc)
            unixTime = str(mktime(utcTime.timetuple()))[:-2]
                
            payload = {}
            payload['metric'] = 'L3.' + str(currentMetric)
            payload['timestamp'] = str(unixTime)
            payload['value'] = str(index[currentMetric])
            tags = {}
            tags['Measurement'] = str(currentMetric)
            payload['tags'] = tags

            url = 'http://146.141.16.82:4242/api/put?summary'
            jsonPayload = json.dumps(payload)

            headers = {
                'Connection': 'close'
            }
            with requests.Session() as session:
                response = session.post(url, data=jsonPayload, headers=headers)




L1data, L2data, L3data, dateData = importMainData()

importAverageParams(L1data, L2data, L3data, dateData)

importMinimumParams(L1data, L2data, L3data, dateData)

importMaximumParams(L1data, L2data, L3data, dateData)

