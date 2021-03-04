#   Apex3D.py
#   Eric Janusson
#   Python 3.7.4 (Base: Conda)
#   S:\\Programming\\Apex3D-EJ090719\\Apex3D.py
#   Usage: Mass/Charge/Mobility Extraction with APEX3D

import os
import csv
import sys
import subprocess
from pathlib import Path

apexPath = r"C:\DriftScope\lib\Apex3D64.exe"     #NOTE Changed to backslash from forward slash
apexLogPath = r"C:\DriftScope\log\_Apex3DLog.txt"        #NOTE Changed to backslash from forward slash

#       Check DriftScope directory for required files 
def checkFiles():
        if (os.path.isfile(apexPath) and os.path.isfile(apexLogPath)):
                pass
        else:
                input("Log and Apex3D files not present. Check DriftScope installation is present at C:\DriftScope. Press Enter to Exit")
                sys.exit("Exiting...")
checkFiles()

#       Ask user for Data Directory path:
def findDataDir():
        print("Paste data directory containing Waters TWIMS .RAW files below:")
        dataDir = os.path.expanduser(input())
        # dataDir = os.path.abspath(r'S:\APEX Test')
        return dataDir
dataDir = findDataDir()

#       Return names of experiments then full paths for Apex
def getFilenames(directory):
        return [name for name in os.listdir(dataDir) if os.path.isdir(os.path.join(dataDir, name))]
expList = getFilenames(dataDir)

#       Generate list of full system paths for all experiment files in data folder
def getDataPaths(directory):
        return [os.path.join(dataDir, name) for name in expList if os.path.isdir(os.path.join(dataDir, name)) and name.lower().endswith((".raw"))]
pathList = getDataPaths(dataDir)

#       Find output folder if not there, then create one
def makeOutputDir():
        if os.path.isdir(os.path.join(dataDir, "APEX Output")):
                print('Writing to existing Apex Output directory. Old files will be overwritten.')
                outputDir =  os.path.join(dataDir, "APEX Output")
                return outputDir
        else:
                os.mkdir(os.path.join(dataDir, "APEX Output"))
                outputDir = os.path.join(dataDir, "APEX Output")
                return outputDir
                # outputDir = os.mkdir(os.path.join(dataDir, "APEX Output"))
                # outputDir = os.path.join(dataDir, "APEX Output")
outputDir = makeOutputDir()

#       Define batch strings and arguments for Apex3D
def apexGo():
        for i in pathList:
                apexGoPath = '{} -pRawDirName "{}" -outputDirName "{}" -outputUserDirName "{}" -lockMassZ1 556.2771 -bCSVOutput 1'.format(apexPath, i, outputDir, outputDir)
                apexGo = subprocess.Popen(apexGoPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = apexGo.communicate() #Error reporting available, if needed
                print('Export Complete for ' + i + '\n')
        print("All Exports Complete")

apexGo()