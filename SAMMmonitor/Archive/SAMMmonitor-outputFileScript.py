import os
import sys
import csv

def get_output_csv_path(input_csv, output_folder=None, out_string='hits'):

    input_csv_name = os.path.basename(input_csv).replace('.csv', '')

    if not output_folder:
        output_folder = os.path.dirname(input_csv)
        output_folder = os.path.join(output_folder, 'out')
        # if not os.path.exists(output_folder):
        #     os.mkdir(output_folder)

    return os.path.join(output_folder, f'{input_csv_name}-{out_string}.csv')

"""
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
"""