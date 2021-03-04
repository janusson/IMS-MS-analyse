# Self-Assembly Mobility Mapping

Tools for ion mobility mass spectrometry data extraction and visualization.

Author: Eric Janusson
Dependencies: Python 3.9 (and additional libraries)

## Introduction

These modules are designed for processing experiment data produced with Waters Synapt ion mobility mass spectrometers (IMS-MS). It also contains functions for data processing, plotting and analysis of IMS-MS data. The modules were created to monitor selected analytes based on m/z and drift time.

## Instructions

Install Waters DriftScope 2.9 to default directory: "C:\DriftScope\".
    # Note that this module will not run chromatographic-based IMS peak picking without this program installed as proprietary Waters DLL files are required to work with files acquired with Waters MS software.

- Move all IMS-MS experiment files (Waters .RAW folder format) to desired working directory and copy full data directory path.

- Run samm.py in terminal shell.

- When prompted, paste data directory and press Enter.
    #By default, all data is exported to a folder in the data directory named "Apex Output"

'''

## Notes on apex3D

- Command line arguments: can be used for scripting with TWIMExtract.
- NOTE: not all features are available in command line mode.

General use: java -jar TWIMExtract.jar [ARGS]
Help: java -jar TWIMExtract.jar -h
NOTE: directories must be in quotes ('') if they contain spaces or other special 
characters.

**Arguments:**
Required:

```cmd

-i '[input directory]' : The full system path to the .raw file from which to extract
-o '[output directory]' : The full system path to the folder in which to save output
-m [mode] : the extraction mode (the dimension of data to save). 0 = RT, 1 = DT, 2 = MZ
```

**Optional:**

```cmd

-f [func] : the individual function to extract. If not provided, extracts all functions
-r '[Range path]' : The full system path to a range (.txt) or rule (.rul) file to use
for extraction. If not provided, extracts the full ranges in all dimensions
-rulemode [true or false] : Whether to use range or rule file.
-combinemode [true or false] : Whether to combine all outputs from a single raw file
(e.g. multiple functions) into a single output.
-ms [true or false]: whether to save DT extractions in milliseconds (ms) or bins.

Example: The command below would extract DT information from all functions from the
'My_data.raw' file using the 'my_range.txt' range file, combine the output using bins as the
DT information, and place it in C:\Extracted Data:

java -jar TWIMExtract.jar -i 'C:\Data\My_data.raw' -o 'C:\Extracted Data' -m 1
-r 'C:\Ranges\my_range.txt' -rulemode false -combinemode true -ms false
```
