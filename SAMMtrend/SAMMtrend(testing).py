#Creator: Eric Janusson
#!/usr/bin/env python3.7.4
#S:\Programming\SAMM\SAMMtrend\SAMMtrend.py
#Usage: SAMMtrend.py is used to determine trends in DT/MS spectra following TWIMExtract processing.

#TODO
#1      import csv file with pandas DONE
#2      trim data so x= m/z, y = intensity DONE
#3      fill x y paired data as numpy arrays - DONE
#4      integrate peaks IF under horizontal line / exponential equation - DONE

import matplotlib.pyplot as plt
import numpy as np
from numpy import trapz
import pandas as pd
import scipy
from scipy import signal
import os
import csv

def findDataDir():
        print("Paste data directory below (must contain CSV files and folders only!):")
        dataDir = os.path.expanduser(input())
        return dataDir
# dataDir = findDataDir()

dataDir = r"D:\Programming\SAMM\SAMMtrend\SAMMtrend Data\3-72-Example Data" #TESTING PURPOSES

def getFilenames(directory):
        dataIDs = []
        for root, dirs, files in os.walk(dataDir, topdown=False):
                for name in files:
                        dataIDs.append(name)
        return dataIDs
                # return[name for name in files if name.lower().endswith(".csv")]
expNames = getFilenames(dataDir)

def getDataPaths(directory):
        dataPaths = []
        for root, dirs, files in os.walk(dataDir, topdown=False):
                for name in files:
                        x = os.path.join(root, name)
                        dataPaths.append(x)
        return dataPaths
pathList = getDataPaths(dataDir)

def linearCutoff():
        print("Processing data...\n")
        expID, expPath, intList, wIntList  = ["Experiment ID"], ["Experiment Path"], ["Full-Spectrum Integration"], ["Linear Weighted Integration"]
        for file in pathList:
                        #Preprocess file: remove headers, store m/z, intensity as numpy arrays
                        # msSpectrum = pd.read_csv("MZ_EJ3-8-1i.csv", skiprows=1)
                msSpectrum = pd.read_csv(file, skiprows=1)
                msSpectrum.columns = ["m/z", "Intensity"]
                # msSpectrum.plot(kind = 'Line', x='m/z', y='Intensity', color='red')     #Diagnostic plot
                xCol = np.asarray(msSpectrum["m/z"])                    #Convert columns to numpy arrays
                yCol = np.asarray(msSpectrum["Intensity"])
                # xBound = 150, np.max(xCol)                    #Spectrum axes boundaries and function/line coefficients
                xBound = np.min(xCol), np.max(xCol)
                yBound = np.min(yCol), np.max(yCol)
                coefficients = np.polyfit(xBound, yBound, 1)                    #Set power of cutoff function, 1=linear
                # print(coefficients)
                slope, yInt = coefficients[0], coefficients[1]
                yNew = []                       #process data - if x's y-value is above function's y-value, set y=yFunc
                for i in range(len(xCol)):
                        xExp, yExp = xCol[i], yCol[i]
                        yMax = (slope*xExp)+yInt
                        if yExp > yMax:
                                yNew.append(yMax)
                        else:
                                yNew.append(yExp)
                # plt.plot(xCol, yNew)
                yNewArray = np.asarray(yNew)

                intList.append(np.trapz(yCol, xCol, axis = 0))                  #calculate areas of experiments, add to lists
                wIntList.append(np.trapz(yNewArray, xCol, axis = 0))
                expPath.append(file)
        for i in expNames:
                expID.append(i)
        return [expID, expPath, intList, wIntList, ]
                # print(file + "\n Full Area = ", fullArea, "\n Processed Area: ", processArea)
outputList = linearCutoff()

def makeOutputDir():                    #Find output folder if not there, then create one
        if os.path.isdir(os.path.join(dataDir, "SAMMtrend Output")):
                print('Writing to existing SAMMtrend Output directory. Old files will be overwritten.')
                outputDir =  os.path.join(dataDir, "SAMMtrend Output")
                return outputDir
        else:
                print("Creating output SAMMtrend Output directory.")
                os.mkdir(os.path.join(dataDir, "SAMMtrend Output"))
                outputDir = os.path.join(dataDir, "SAMMtrend Output")
                return outputDir
outputDir = makeOutputDir()

def writeOutputFile():
        print("Writing output file to " + outputDir + "\\SAMMtrendOutput.csv")
        with open (outputDir + "\\SAMMtrendOutput.csv", "w", newline="") as out:
                writer = csv.writer(out)
                writer.writerows(outputList)
        print("Completed!")
writeOutputFile()