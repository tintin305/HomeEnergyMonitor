#!/usr/bin/env python

import sys, os
import time
import datetime
import threading
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd

data = pd.read_csv('BackupSystem.csv')

print(data.head())
print(data.tail())
# data.dropna(inplace = True)

timeVec = data['Timestamp'].to_numpy()
timeVec = list(range(0,len(data)))
inputPower = data['Power (Wm) - sid = 695907 (Input)'].to_numpy()
outputPower = data['Power (Wm) - sid = 809799 (Output)'].to_numpy()

# Input power
# plt.plot(timeVec, inputPower)
# plt.show()


# Output power
# plt.plot(timeVec, outputPower)
# plt.show()


diff = np.subtract(outputPower,inputPower)
diff = diff[np.logical_not(np.isnan(diff))]
np.savetxt('Diff.csv', diff, delimiter=',')
print(type(diff))

# plt.plot(timeVec, diff)
# plt.show()

summedDiff = np.sum(diff, axis = 0)
print(summedDiff)

