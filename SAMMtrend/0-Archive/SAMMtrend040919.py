#Creator: Eric Janusson
#!/usr/bin/env python3.7.4
#S:\Programming\SAMM\SAMMtrend\SAMMtrend.py
#Usage: SAMMtrend.py is used to determine DT/MS spectral features

#TODO
#1      import csv file with pandas DONE - loop this for each file
#2      trim data so x= m/z, y = intensity DONE - same warning as above
#3      fill x y paired data as numpy arrays - DONE
#4      integrate peaks IF under horizontal line / exponential equation

import matplotlib.pyplot as plt
import numpy as np
from numpy import trapz
import pandas as pd
import scipy
from scipy import signal
import os

# def findDataDir():
#         print("Paste data directory below:")
#         dataDir = os.path.expanduser(input())
#         # dataDir = os.path.abspath(r'S:\APEX Test')
#         return dataDir
# dataDir = findDataDir()
dataDir = r"D:\Programming\SAMM\SAMMtrend"  #if data is in current working directory

#       Generate list of full system paths for all CSV files in data folder
def getFilenames(directory):
        return [name for name in os.listdir(dataDir) if name.lower().endswith((".csv"))]
def getDataPaths(directory):
        return [os.path.join(dataDir, name) for name in csvList if  name.lower().endswith((".csv"))]
csvList = getFilenames(dataDir)
pathList = getDataPaths(dataDir)

# Loop through all files and do data treatment
def batchPreProc():
        for experiment in pathList:
                testData = pd.read_csv(experiment)
                print(testData)

#Preprocess file by removing headers and storing m/z and intensity as separate x / y numpy arrays
msSpectrum = pd.read_csv("MZ_EJ3-8-1i.csv", skiprows=1)
msSpectrum.columns = ["m/z", "Intensity"]
#Convert columns to numpy arrays
xCol, yCol= np.asarray(msSpectrum["m/z"]), np.asarray(msSpectrum["Intensity"])
#Spectrum axes boundaries and function/line coefficients
xBound = np.min(xCol), np.max(xCol)
yBound = np.min(yCol), np.max(yCol)
coefficients = np.polyfit(xBound, yBound, 1) #Set power of cutoff function, 1=linear
print(coefficients)
slope, yInt = coefficients[0], coefficients[1]
#process data - if x's y-value is above function's y-value, set y=yFunc
yNew = []
for i in range(len(xCol)):
        xExp, yExp = xCol[i], yCol[i]
        yMax = (slope*xExp)+yInt
        if yExp > yMax:
                yNew.append(yMax)
        else:
                yNew.append(yExp)
plt.plot(xCol, yNew)
yNewArray = np.asarray(yNew)

        #calculate area of new array
area = np.trapz(yNewArray, xCol, axis = 0)
print("Area = ", area)


# #       Find output folder if not there, then create one
# def makeOutputDir():
#         if os.path.isdir(os.path.join(dataDir, "SAMMtrend Output")):
#                 print('Writing to existing SAMMtrend Output directory. Old files will be overwritten.')
#                 outputDir =  os.path.join(dataDir, "SAMMtrend Output")
#                 return outputDir
#         else:
#                 os.mkdir(os.path.join(dataDir, "SAMMtrend Output"))
#                 outputDir = os.path.join(dataDir, "SAMMtrend Output")
#                 return outputDir
# outputDir = makeOutputDir()
