"""
SAMM3Dextract-190220.py
Eric Janusson
Python 3.7.4 (64-bit)
Usage: Mass/Charge/Mobility Extraction from Waters .RAW files using high-density APEX3D extraction. 
Paste data directory containing .RAW files to be exported into 3D CSV files in the given directory as "APEX Output"
"""

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
                input(r"Log and Apex3D files not present. Check DriftScope installation is present at C:\DriftScope. Press Enter to Exit")
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
                #The parameters -leThresholdCounts 10 -heThresholdCounts 10 below may be modified to adjust the minimum detectable peak threshold
                apexGoPath = '{} -pRawDirName "{}" -outputDirName "{}" -outputUserDirName "{}" -leThresholdCounts 10 -msOnly 0 -heThresholdCounts 10 -lockMassZ1 556.2771 -bCSVOutput 1'.format(apexPath, i, outputDir, outputDir)
                apexGo = subprocess.Popen(apexGoPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                out, err = apexGo.communicate() #Error reporting available, if needed
                print('Export Complete for ' + i + '\n')
        print("All Exports Complete")

apexGo()


# #SAMM3Dextract.py Notes
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
