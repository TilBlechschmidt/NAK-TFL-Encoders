#!/usr/bin/env python3
import json
import os
import csv
import numpy as np
import scipy.stats
from shared import crunch_number

# https://stackoverflow.com/a/15034143/6397601
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


directory = os.fsencode("variations")
files = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == ".DS_Store":
        continue
    files.append(filename)

files.sort()

keys = ['wall', 'user', 'system', 'read', 'write', 'bitrate', 'avg_memory', 'max_memory']
rows = [['name'] + keys + ['bitrate gamma', 'bitrate t_u', 'bitrate t_v', 'cpu gamma', 'cpu t_u', 'cpu t_v']]
for file in files:
    data, samples = crunch_number("variations/" + file)

    fields = [file]
    for key in keys:
        fields.append(round(data[key], 4))

    gamma, t_u, t_v = mean_confidence_interval(samples['bitrate'])
    fields += [round(gamma, 4), round(t_u, 4), round(t_v, 4)]

    cpu_samples = samples['duration']['user'] + samples['duration']['system']
    gamma, t_u, t_v = mean_confidence_interval(cpu_samples)
    fields += [round(gamma, 4), round(t_u, 4), round(t_v, 4)]

    rows.append(fields)

with open('data/variation.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
