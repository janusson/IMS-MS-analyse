#!python3

#   SAMM-3D-extract.py
#   Eric Janusson
#   Python 3.7.4 (Base: Conda)
#   Usage: 3D Mass/Charge/Mobility data extraction from Waters .RAW TWIMS-MS files using Apex3D subprocess

import os
import csv
import sys
import subprocess
from pathlib import Path

#   Define Driftscope paths for APEX subprocess: 
# NOTE Waters DriftScope software must be installed in the default directory.
apexPath = r"C:\DriftScope\lib\Apex3D64.exe"
apexLogPath = r"C:\DriftScope\log\_Apex3DLog.txt"

# Check DS install dirs for required files
def checkFiles():
        if (os.path.isfile(apexPath) and os.path.isfile(apexLogPath)):
                pass
        else:
                print(r"Log and Apex3D files not present. Check DriftScope installation is present at C:\DriftScope.")
                sys.exit()
checkFiles() # ensure DS/APEX installed

def getDataDir():
        # print("Enter DATA directory with Waters .RAW experiment files below:")
        userData = os.path.expanduser(input('Paste data directory containing Waters TWIMS .RAW files below:'))   # expanduser to remove user account conflicts
        if os.path.isdir(userData):
                return userData
        else:
                print(r'ERROR: Path cannot be found. Exiting.')
                sys.exit()
dataDir = getDataDir() # Make output Directory in Data folder 

#       Return names of experiments then full paths for Apex
def getFilenames(directory):
        return [name for name in os.listdir(dataDir) if os.path.isdir(os.path.join(dataDir, name))]
expList = getFilenames(dataDir)

#       Produce list of dirs for all experiment files in data folder
def getDataPaths(directory):
        return [os.path.join(dataDir, name) for name in expList if os.path.isdir(os.path.join(dataDir, name)) and name.lower().endswith((".raw"))]
pathList = getDataPaths(dataDir)

#       Find output folder or create one
def makeOutputDir():

    # ask for data directory or use current
    print('Enter output directory path. Press Enter to create output folder here: ' + dataDir)
    userOutPath = input('Enter output directory path: ')

    if os.path.isdir(os.path.join(dataDir, "3D-data-extraction")): # if the data directory is a path 
            print('- - - > Writing to existing /"3D-data-extraction/" directory. Old files will be overwritten.')
            input('3D-data-extraction Data Export to...')
            outputDir =  os.path.join(dataDir, "3D-data-extraction")
            return outputDir
 
    elif os.path.isdir(os.path.join(userOutPath)): # CHECK
        outputDir = os.path.join(userOutPath)
        return outputDir

    else:
            os.mkdir(os.path.join(dataDir, "3D-data-extraction"))
            outputDir = os.path.join(dataDir, "3D-data-extraction")
            return outputDir
            # outputDir = os.mkdir(os.path.join(dataDir, "3D-data-extraction"))
            # outputDir = os.path.join(dataDir, "3D-data-extraction")

outputDir = makeOutputDir()

### chexk makeoutput dir function ^^^





#       Define batch strings and arguments for Apex3D
def apexGo():
        for i in pathList:
                #The parameters -leThresholdCounts 10 -heThresholdCounts 10 below may be modified to adjust the minimum detectable peak threshold
                apexGoPath = '{} -pRawDirName "{}" -outputDirName "{}" -outputUserDirName "{}" -leThresholdCounts 10 -msOnly 0 -heThresholdCounts 10 -lockMassZ1 556.2771 -bCSVOutput 1'.format(apexPath, i, outputDir, outputDir)
                apexGo = subprocess.Popen(apexGoPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = apexGo.communicate() #Error reporting available, if needed
                print('Export Complete for ' + i + '\n')
        print("All Exports Complete")

apexGo()


# Notes on APEX3D:
# - Command line arguments: can be used for scripting with TWIMExtract. NOTE: not all features are available in command line mode.
# 		General use: java -jar TWIMExtract.jar [ARGS]
# 		Help: java -jar TWIMExtract.jar -h
		
# 		NOTE: directories must be in quotes ("") if they contain spaces or other special characters
# 		Arguments:
# 			Required:
# 			-i "[input directory]" : The full system path to the .raw file from which to extract
# 			-o "[output directory]" : The full system path to the folder in which to save output
# 			-m [mode] : the extraction mode (the dimension of data to save). 0 = RT, 1 = DT, 2 = MZ

# 			Optional:
# 			-f [func] : the individual function to extract. If not provided, extracts all functions
# 			-r "[Range path]" : The full system path to a range (.txt) or rule (.rul) file to use
# 				for extraction. If not provided, extracts the full ranges in all dimensions
# 			-rulemode [true or false] : Whether to use range or rule file. 
# 			-combinemode [true or false] : Whether to combine all outputs from a single raw file
# 				(e.g. multiple functions) into a single output. 
# 			-ms [true or false]: whether to save DT extractions in milliseconds (ms) or bins. 

# 		Example: The command below would extract DT information from all functions from the 
# 		"My_data.raw" file using the "my_range.txt" range file, combine the output using bins as the
# 		DT information, and place it in C:\Extracted Data:

# 		java -jar TWIMExtract.jar -i "C:\Data\My_data.raw" -o "C:\Extracted Data" -m 1 
# 			-r "C:\Ranges\my_range.txt" -rulemode false -combinemode true -ms false