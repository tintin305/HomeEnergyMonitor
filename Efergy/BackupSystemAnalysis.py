#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('Test.csv')

data.dropna(inplace=True)

timeVec = data['Timestamp'].to_numpy()
timeVec = list(range(0, len(data)))


inputPower = data['Power (Wm) - sid = 695907 (Input)'].to_numpy()
outputPower = data['Power (Wm) - sid = 809799 (Output)'].to_numpy()
print(inputPower)
# Input power
plt.plot(timeVec, inputPower)
plt.show()


# Output power
plt.plot(timeVec, outputPower)
plt.show()


diff = np.subtract(outputPower, inputPower)
diff = diff[np.logical_not(np.isnan(diff))]
np.savetxt('Diff.csv', diff, delimiter=',')

plt.plot(timeVec, diff)
plt.show()

data['Timestamp'] = pd.to_datetime(data['Timestamp'])
dateDiff = data['Timestamp'].iloc[-1] - data['Timestamp'].iloc[0]

print('Time Recording: ' + str(dateDiff))


diffHours = (int(dateDiff.days) * 24) + (int(dateDiff.seconds) / 3600)

print('Number of hours: ' + str(diffHours))

summedDiff = np.sum(diff, axis=0) / (60**2)
print('Per minute energy: ' + str(summedDiff))


energy = (summedDiff * diffHours) / (10**3)

print('Energy generated over period of ' + str(diffHours/24) + ' days is: ' + str(energy) + ' kWh')

averageDailyGeneration = energy / (diffHours/24)
print('Average daily generation: ' + str(averageDailyGeneration) + ' kWh')
