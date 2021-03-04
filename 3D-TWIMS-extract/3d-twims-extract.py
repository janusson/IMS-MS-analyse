'''
3d-twims-extract.py
Usage: 3D Mass/Charge/Mobility data extraction from Waters .RAW TWIMS-MS files 
using DriftScope Apex3D subprocess for high-density data extraction.
'''
import os
import sys
import subprocess
from pathlib import Path

# NOTE Waters DriftScope software must be installed in the default directory.

apex_path = Path(r'C:/DriftScope/lib/Apex3D64.exe')
apex_log_path = Path(r'C:/DriftScope/log/_Apex3DLog.txt')

def get_data_dir():
    '''
    Search directory and subdirectories for Waters .raw experiment file folders

    Returns:
        list: path_list is a list of full .raw directories.
    '''
    
    data_dir = Path(r'D:\2-SAMM\Data\EJ3-60-SAMM3-MoMonitoring\Raw Data\BA\BA4')
    print('>>>program searches topdown from directory given.')
    print(f'>>>enter data directory or use default: {data_dir}.')
    user_choice = input()
    if len(user_choice)<2:
        print(f'using default dir.')
    else:
        data_dir = user_choice
    path_list = [x[0] for x in os.walk(data_dir, 1) if x[0][-4:] == '.raw']
    print(f'Processing {len(path_list)} .raw experiment files.')

    return path_list

# find output folder in program CWD, or create if not there 
def get_output_dir():
    '''
    find data output folder in program working dir or create one.

    Returns:
        Pathlike: directory to send extracted data file
    '''
    output_dir = Path(r'D:/2-SAMM/Programs/SAMM/3D-TWIMS-extract/out/')
    if os.path.isdir(output_dir):
        output_dir
    else:
        output_dir = os.mkdir(output_dir)
    return output_dir

def check_dependencies():
    '''
    ensures apex3D executable and logfiles are accessible.
    only checks default install dir.

    Returns:
        print: ensures subprocess can run or ends program
    '''
    condition1 = (os.path.isfile(apex_path) and os.path.isfile(apex_log_path))
    if condition1:
        print(r'Apex exectuable found.')
    else:
        print(r'Apex log and exectuable not present.')
        print(r'Check DriftScope 2.2 installation in C:\DriftScope.')
        sys.exit('-error-')
    return print('extracting data')

def main():
    '''
    apex3D processing of Waters Synapt G2 TWIMS-MS .raw experiment file. 
    
    Args: 
        -leThresholdCounts [string]: LOD low pass threshold in counts. 
        -heThresholdCounts [string]: LOD high pass threshold in counts.
    Returns:
    '''
    path_list = get_data_dir()
    output_dir = get_output_dir()
    check_dependencies()
    print(f'Converting .raw files to .csv')
    for i in path_list:
        apex_goPath = ('{} -pRawDirName "{}" -outputDirName "{}" '
        +'-outputUserDirName "{}" -leThresholdCounts 10 -msOnly 0 '
        +'-heThresholdCounts 10 -lockMassZ1 556.2771 -bCSVOutput 1').format(
            apex_path, i, output_dir, output_dir)
        try:
            apex_go = subprocess.Popen(
            apex_goPath, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
            out, err = apex_go.communicate()  # error reporting
        except Exception:
            print('Error. Check DriftScope installation.')
            print(err)
            sys.exit()
        else:
            pass
        print(f'{i} extraction complete...')
    print(f'TWIMS data extraction complete. output directory: ')
    print(f'{output_dir}')
    return

# run main
if __name__ == '__main__':
    main()
