import pandas as pd
import re
import csv

df = pd.read_csv(open('dataFinished.csv', 'rb'))
df = df.dropna()

# Avg stress by temp
countDict = {}
totalDict = {}

for index, row in df.iterrows():
    try:
        totalDict[row['Temperature (F)']] += row['Stress Rating']
        countDict[row['Temperature (F)']] += 1
    except KeyError:
        totalDict[row['Temperature (F)']] = row['Stress Rating']
        countDict[row['Temperature (F)']] = 1

avgDict = {}
for temp in countDict.keys():
    avgDict[temp] = totalDict[temp] / countDict[temp]

with open('avgStressbyTemp.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in avgDict.items():
       writer.writerow([key, value])