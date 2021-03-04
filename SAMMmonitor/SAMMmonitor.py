'''
SAMMmonitor.py
Python Version: 3.9.1
Purpose: Screens APEX3D ion mobility data and report intensities of
experimental reference data. 

Used for integration of selected ions from multiple .raw experiment files.

Input: Data folder containing .csv APEX3D data (ex: from 3D-TWIMS-extract.py)
Summary output .csv is exported to data directory.
'''

import sys, os, csv
from pathlib import Path
from datetime import datetime, date, time, timezone
import pandas as pd
from pandas.core.frame import DataFrame

# time functions
print('program start at: ' + str(datetime.now()) + '\n---===---\n')
hmmss = str(datetime.now()).split(' ')[1][0:8].replace(':', '')
day = str(datetime.now()).split(' ')[0][2:10].replace(':', '')

# directories:
monitorDir = str(os.getcwd())

# default directory of Apex3D output data csv files
data_directory = Path(
    r'D:\\2-SAMM\Data\EJ3-60-SAMM3-MoMonitoring\Raw Data\APEX Output')

# path of CSV file with target analyte
targets_csv = Path(
    r'D:\2-SAMM\Programs\SAMM\SAMMmonitor\experimental-target-list.csv')

# target m/z error tolerance (default: 1.0 m/z)
# target mobility error tolerance (as percentage. default: 0.05 m/z)
mz_tol, mob_tol = 1.0, 0.05

csv_files = [os.path.join(data_directory, csv_f)
             for csv_f in os.listdir(data_directory)]

### Main Functions

# for importing reference file csv. Used in 'fetch_target_data' func.
def read_data_csv(csv_file, delimitchar=',', headers=True):
    '''
    Reads input csv file, excluding headers. Used for reference data.
    *args: csv_file {str} -- Windows filepath of .csv file
    **kwargs: delimitchar {str} -- Comma delimiter for .csv
    Returns: data_list {list} -- imported .csv data
    '''
    data_list = []  # create new list
    with open(csv_file) as f:
        # open comma-delimited csv
        csvreader = csv.reader(f, delimiter=delimitchar)
        for row, columns in enumerate(csvreader):
            if (headers and row > 0) or not headers:
                data_list.append([columns[i] for i in range(0, len(columns))])
            else:
                pass
    return data_list

# import experimental reference data
def fetch_target_data(target_file):
    '''
    Returns dictionary of exp. analyte targets from .csv file
    Arguments:
    target_file {str} -- [full string path to targets CSV]
    Returns:
    target_dict {dict} -- [dictionary of name, m/z, mobility from target list]
    '''
    print(
        f'Loading target_file: \n {target_file}\n')
    target_dict = {}
    target_data_file = read_data_csv(target_file)
    for data in target_data_file:
        # from reference file get ion, experimental m/z, and drift time
        target, target_mz, target_mob, = data[0], float(data[2]), float(data[3])
        #determine ion charge, set as var z
        print(target[-3:])
        if target[-3:] == ']2-':
            target_z = 2
        else: target_z = 1
        # create dict
        target_dict[target] = {
            'mz': target_mz, 
            'mobility': target_mob,
            'charge': target_z
        }
    return target_dict

# create reference .csv data dictionary
ref_dic = fetch_target_data(targets_csv)

# experiment data import 
def importSAMM3D(csv_path):
    '''
    Processes mass/mobility/area data from Apex3D .csv file.

    Args:
        csv_path (string): [description]

    Returns:
        pd.DataFrame: m/z, mobility, and intensity data in a dataframe object.
        Ex:
        >>> data1 = importSAMM3D(csv_files[0])
        >>> output
                    m/z      DT  Area  m/z Error  DT Error  Area Error
        0      1273.1662  49.099    68    13.4383      0.31        3.18
        1       540.1503  26.155   677     8.2872      0.15        5.21
    '''
    path = str(csv_path)

    apexDF = pd.read_csv(path)
    x, y, z, = (
        list(apexDF['m_z']),
        list(apexDF['mobility']),
        list(apexDF['area']),
    )
    xError, yError, zError = (
        list(apexDF['errMzPPM']),
        list(apexDF['errMobility']),
        list(apexDF['errArea']),
    )
    newApexDF = pd.DataFrame(
        zip(x, y, z, xError, yError, zError),
        columns=['m/z', 'DT', 'Area', 'm/z Error', 'DT Error', 'Area Error']
        )

    return newApexDF

# set tolerance range for target ions
def set_tolerance(ion):
    '''
    Sets tolerance per-ion. Based on analyte dictionary.
    Args:
        ion (string): name of ion.
    Returns:
        floats: upper and lower m/z and DT ranges.
    '''
    # set tolerance range for ion (from: ref_dic)
    target_mz = float(ref_dic[ion]['mz'])
    target_dt = float(ref_dic[ion]['mobility'])
    upperMZ, lowerMZ = float(target_mz+mz_tol), float(target_mz-mz_tol)
    upperDT, lowerDT = target_dt*mob_tol, target_dt*(-mob_tol)
    # print(f'Checking {ion} with mass range: {lowerMZ}-{upperMZ}')
    return float(upperMZ), float(lowerMZ), float(upperDT), float(lowerDT)

# find areas within m/z+DT range and sum
def find_match(raw_data, upperMZ, lowerMZ, upperDT, lowerDT): 
    # raw_data = importSAMM3D(csv_files[0])
    # upperMZ, lowerMZ, upperDT, lowerDT = set_tolerance('[HMo4O13]-')
    print('Converting reference data to bins for DT comparison.')
    # TODO fixing drift time range...
        # constant C = *1.4105
        # need mass and charge!? # Above - 
    raw_data['m/z']
    raw_data['charge']
        t_c = t_d - c(m_ion/z_ion)^0.5
        tc*=td-C*np.sqrt(mion/zion)
        ### FIXME Here!
    m_range = (raw_data['m/z'] >= lowerMZ) & (raw_data['m/z'] <= upperMZ)
    d_range = (raw_data['DT'] >= lowerDT) & (raw_data['DT'] <= upperDT)
    matches = raw_data[['m/z', 'DT', 'Area']].loc[(m_range & d_range), 'Area']
    # then sum areas:
        # areaDF.sum()
    # return print(raw_data['Area'].loc(filt))
    return print(matches)

# run single analyte test:
raw_data = importSAMM3D(csv_files[0])
for ion in ref_dic.keys():
    upperMZ, lowerMZ, upperDT, lowerDT = set_tolerance(ion)
    find_match(raw_data, upperMZ, lowerMZ, upperDT, lowerDT)
# example_mass, example_dt = 879.50, 4.84
print('test done!') ### https://stackoverflow.com/questions/28236305/how-do-i-sum-values-in-a-column-that-match-a-given-condition-using-pandas

# main psuedocode:
def mainPC(): # FIXME
    for ion in ref_dic.keys():
        formula = str(ion)
        analyte_mz = ref_dic.get(ion).get('mz')
        analyte_dt = ref_dic.get(ion).get('mobility')

        # for each ion of interest, grab all files
        for dataDir in csv_files:
            raw_data = importSAMM3D(dataDir)
            upperMZ, lowerMZ, upperDT, lowerDT = set_tolerance(ion)
            # find_match(raw_data, upperMZ, lowerMZ, upperDT, lowerDT)
            m_range = (raw_data['m/z'] >= lowerMZ) & (raw_data['m/z'] <= upperMZ)
            d_range = (raw_data['DT'] >= lowerDT) & (raw_data['DT'] <= upperDT)
            matches = [raw_data[['m/z', 'DT', 'Area']].loc[m_range & d_range, 'Area']]
            # TODO write find_match: matches both m/z and mobility (line 131)
                # get area of match entry
                # get csv filename
                # append entry to an ('ion','filename'.area) dataframe and write to file 

### End Program
# sys.exit('\n- = - Complete - = -\n')

# file output functions
def get_output_csv_path(input_csv):
    ''' [Find output directory if it exists (otherwise create it). 
    Naming scheme based on input data name.]

    Arguments:
        data_csv = [CSV in which original APEX3D output data is stored]
        target_dict = [From fetch_target_data, list of target m/s vs. mob 
        pairs provided by user in CSV form]
        mz_tolerance = [Selected threshold entered for m/z tolerance required 
        for a 'hit' to be recorded]
        mob_tolerance = [Selected threshold entered for mobility tolerance in 
        BINS required for a 'hit' to be recorded]
        mz_units='abs' = [Changed if absolute m/z threshold is not used 
        (i.e. a percentage instead)]

    Returns:
        targ_dict = [A dictionary of targets returning True from check_hit]

    NOTE: Incompatible with DriftScope v 2.2 (ex: APEX exports use col 4 of .csv file)
    '''
    input_csv_name = os.path.basename(input_csv).replace('.csv', '')

    output_folder = os.path.join(
        monitorDir + 'SAMMmonitor Output - ' + str(hmmss))
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    return os.path.join(output_folder, f'{input_csv_name}-monitor.csv')

def write_output_csv(output_csv, headers=['target_molecule', 'id', 'obs_mz', 'RT', 'obs_mobility', 'intensity'],
                     delimitchar=','):
    with open(output_csv, 'w') as write_file:

        write = csv.writer(write_file, delimiter=delimitchar)
        write.writerow(headers)

def append_output_csv(output_csv, write_list, delimitchar=','):
    # print(f'for {output_csv}, write list = {write_list}')
    with open(output_csv, 'a') as opened_file:
        writer = csv.writer(opened_file, delimiter=delimitchar)
        writer.writerow(write_list)

def write_hits_for_single_csv(data_csv, target_dict, mz_tolerance, mob_tolerance,
                              out_folder=None, headers=['Target Formula', 'Index',
                                                        'Observed m/z', 'm/z No Cal', 'RT', 'Intensity', 'Area', 'Counts', 'Mobility']):
    targ_dict = screen_hits_for_single_csv(
        data_csv, target_dict, mz_tolerance, mob_tolerance
    )
    output_csv = get_output_csv_path(data_csv)
    write_output_csv(output_csv, headers)

    for target_molecule, hits_lists in targ_dict.items():

        for hit in hits_lists:
            if len(hit) > 0:
                write_list = [target_molecule]
                write_list.extend(hit)
                append_output_csv(output_csv, write_list)

def write_hits_multiple_csvs(target_dict, csv_folder,
                             mz_tolerance, mob_tolerance,
                             out_folder=None):
    for entry in csv_files:
        write_hits_for_single_csv(entry, target_dict,
                                  mz_tolerance, mob_tolerance,
                                  out_folder)


# module initiation
def main():
    pass
if __name__ == '__main__':
    main()
    print('\n---===--- \nprogram end at: ' + str(datetime.now()))
'''
( •_•)
( •_•)>⌐■-■
(⌐■_■)
'''