#Creator: Eric Janusson
#!/usr/bin/env python3.7.4
#S:\Programming\SAMM\SAMMtrend\SAMMtrend.py
#Usage: SAMMtrend.py is used to determine DT/MS spectral features

#TODO
#1      import csv file with pandas DONE - remember to loop this for each file
#2      trim data so x= m/z, y = intensity DONE - same warning as above
#3      fill x y paired data as numpy arrays - DONE
#4      integrate peaks IF under horizontal line / exponential equation

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simps
from numpy import trapz
import pandas as pd
import scipy
import os

# def findDataDir():
#         print("Paste data directory below:")
#         dataDir = os.path.expanduser(input())
#         # dataDir = os.path.abspath(r'S:\APEX Test')
#         return dataDir
# dataDir = findDataDir()
dataDir = os.getcwd() #for now data is in current working directory

def getFilenames(directory):
        return [name for name in os.listdir(dataDir) if name.lower().endswith((".csv"))]
expList = getFilenames(dataDir)
print(expList)

#       Generate list of full system paths for all experiment files in data folder
def getDataPaths(directory):
        return [os.path.join(dataDir, name) for name in expList if  name.lower().endswith((".csv"))]
pathList = getDataPaths(dataDir)
print(pathList)

#Loop through all files and do data treatment (LATER)
# def batchPreProc():
# for file in pathList:
        # testData = pd.read_csv(file)

#Preprocess file by removing headers and storing m/z and intensity as separate x / y numpy arrays

msSpectrum = pd.read_csv("MZ_EJ3-8-1i.csv", skiprows=1)
msSpectrum.columns = ["m/z", "Intensity"]

dataArray = np.asarray(msSpectrum)

dataArray.shape
dataArray[0]
area = np.trapz(dataArray[:,1],dataArray[:,0])

print("Area = ", area)

#       Initial code idea:
# xExp = []
# yExp = []
# xF = [i for i in xExp]
# yF = [np.exp() for i in yExp]
#yFit = [e* for i in yExp]


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
