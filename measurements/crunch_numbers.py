#!/usr/bin/env python3
import json
import os
import csv
import numpy as np

from shared import crunch_number

directory = os.fsencode("out")
folders = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename == ".DS_Store":
        continue
    folders.append(filename)

folders.sort()

keys = ['wall', 'user', 'system', 'read', 'write', 'bitrate', 'avg_memory', 'max_memory']
rows = [['name'] + keys]
for codec in folders:
    data, samples = crunch_number("out/" + codec + "/data.json")
    fields = [codec]
    for key in keys:
        fields.append(round(data[key], 4))
    rows.append(fields)

with open('data/all.csv', 'w') as file:
    writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
    writer.writerows(rows)
