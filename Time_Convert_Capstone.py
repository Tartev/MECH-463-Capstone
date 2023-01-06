#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 11:11:21 2023

@author: vincenttarte
"""

import csv
import datetime

import csv
import datetime

# Open the input and output CSVs
with open('Griffin_DefaultTrial_Session1_Shimmer_6835_Calibrated_SD.csv', 'r') as input_csv, open('output.csv', 'w') as output_csv:
    # Create a CSV reader and writer
    reader = csv.reader(input_csv)
    writer = csv.writer(output_csv)

    # Iterate over the rows of the input CSV
    for i, row in enumerate(reader):
        # Skip the first two rows (the header rows)
        if i < 2:
            writer.writerow(row)
            continue

        # Convert the timestamp to a datetime object and then to UTC
        timestamp = float(row[0])
        dt = datetime.datetime.utcfromtimestamp(timestamp / 1000.0)

        # Modify the row and write it to the output CSV
        row[0] = dt.strftime('%Y-%m-%d %H:%M:%S:%f')
        writer.writerow(row)
