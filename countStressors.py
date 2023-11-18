import pandas as pd
import re
import csv

df = pd.read_csv(open('dataFinished.csv', 'rb'))


# TODO: Count stressors
stressors = df['Element']
countStressors = {}
for row in stressors:
    row = row[2:-2].split('\', \'')
    for item in row:
        try:
            countStressors[item] += 1
        except KeyError:
            countStressors[item] = 1
countStressors = dict(sorted(countStressors.items(), key=lambda x:x[1], reverse=True))

stressorsDF = pd.DataFrame()
stressorsDF['Stimuli'] = countStressors.keys()
stressorsDF['Count'] = countStressors.values()
stressorsDF.to_csv('stimuliCounts.csv')