#!python3
import pathlib
import subprocess
import sys
import csv
import os
import numpy as np
import pandas as pd
import altair as alt

"""
2d-MSplot-interactive.py
Dr. Eric Janusson
Python 3.8.4
Usage: Mass/Charge/Mobility Extraction from Waters .RAW files
and plotting for data exploration.
"""

workingFile = pathlib.Path(
    'D:/2-SAMM/SAMM - Data Workup Folder/Data Workup(300919)/SAMM3D Extracts/EJ3-27-APEXHD Output/EJ3-27-12-Sample6_Apex3DIons.csv')
print(workingFile)


def read_data_csv(csv_file, delimitchar=',', headers=True):
    """[Reads and passes on data from input csv file]
    Arguments:
        csv_file {str} -- [full str path to .csv file]
    Keyword Arguments:
        delimitchar {str} -- [delimiter for csv] (default: {','})
    Returns:
        data_list {list} -- [list of csv data by row]
    """
    data_list = []  # create new list

    with open(csv_file) as f:
        # open comma-delimited csv
        csvreader = csv.reader(f, delimiter=delimitchar)
        for row, columns in enumerate(csvreader):
            if (headers and row > 0) or not headers:
                data_list.append([columns[i] for i in range(0, len(columns))])

    return data_list


data = read_data_csv(workingFile)

data


"""

plottnig with altair


points = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color=alt.condition(interval, 'Origin', alt.value('lightgray'))
).properties(
    selection=interval
)

"""
