#!/usr/bin/env python3
import json
import os
import csv
import numpy as np

def last_not_zero_value(lst):
    for value in reversed(lst):
        if value != 0.0:
            return value
    return 0.0

def crunch_number(file):
    with open(file, "r") as f:
        data = json.load(f)

    bitrates = []
    memory_usages = []
    duration = {
        "wall": [],
        "user": [],
        "system": []
    }
    io = {
        "read": [],
        "write": []
    }

    # Extract the values from the measurements
    for measurement in data['measurements']:
        bitrates.append(measurement['bitrate'])
        memory_usages.append(last_not_zero_value(measurement['memory']))
        
        for key in duration:
            duration[key].append(last_not_zero_value(measurement['times'][key]))

        for key in io:
            io[key].append(last_not_zero_value(measurement['io'][key]))

    # Calculate the averages for times and io
    output = {}
    for key in duration:
        output[key] = float(np.median(duration[key]))
    for key in io:
        output[key] = float(np.median(io[key]))

    # Accumulate individual values
    output['bitrate'] = float(np.median(bitrates))
    output['avg_memory'] = float(np.median(memory_usages))
    output['max_memory'] = float(np.max(memory_usages))

    samples = {}
    samples['bitrate'] = bitrates
    samples['memory'] = memory_usages
    samples['duration'] = duration
    samples['io'] = io

    return (output, samples)