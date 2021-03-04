"""
Filename: SAMMmonitor-121219.py
Original: TWIMMonitor-3-16.py
Created: 270619
Python Version: 3.7.4 64-bit
Purpose: Script for screening APEX3D-generated ion mobility data to find intensities of known targets from list and generate a 'Hit list'. Hit list is exported to "SAMMmonitor Output'
in same folder as APEX3D data.
Notes: Script modified for EJ3-16 APEXOUT Export
"""

import os
import csv
import sys

#system path of Apex3d Data
data_folder = r'D:\2-SAMM\SAMM-Self-Assembly-Mobility-Mapping - Paper Folder\Programming\S-SAMM Programs\SAMM\SAMMmonitor\SAMMmonitor Data\3-72-Example Data\APEX Output'

#system path of targets CSV list
targets_csv = r'D:\2-SAMM\SAMM-Self-Assembly-Mobility-Mapping - Paper Folder\Programming\S-SAMM Programs\SAMM\SAMMmonitor\SAMMmonitor Data\TargetList-SAMMmonitor-testing.csv'

# mz_tolerance = error tolerance for m/z value, in either absolute (default), can set as percentage
# mob_tolerance = error tolerance for mobility, in percentage 
# mz_units set to 'abs' as default for absolute mz_tolerance. If not 'abs' (i.e. None or whatever, mz_tolerance is read as decimal fraction)
mz_tolerance, mob_tolerance = 1, 0.05

def read_data_csv(csv_file, delimitchar=',', headers=True):
    """[Reads and passes on data from input csv file]

    Arguments:
        csv_file {str} -- [full str path to .csv file]
    
    Keyword Arguments:
        delimitchar {str} -- [delimiter for csv] (default: {','})
    
    Returns:
        data_list {list} -- [list of csv data by row]
    """ 
    data_list = []  #create new list
    
    with open(csv_file) as f:
        csvreader = csv.reader(f, delimiter = delimitchar)  #open comma-delimited csv
        for row, columns in enumerate(csvreader):
            if (headers and row > 0) or not headers:
                data_list.append([columns[i] for i in range(0, len(columns))])
        
    return data_list

def list_csv_data_files(data_directory): 
    """[Returns list of full file paths for data files in directory]
    
    Arguments:
        data_directory {str} -- [full string path to data folder]
    
    Returns:
        files {list} -- [list of full string paths to data files]
    """
    files = [os.path.join(data_directory, csv_f) for csv_f in os.listdir(data_directory)]

    return files 

def fetch_target_data(target_file):
    """[Returns dictionary in given targets CSV file]
    
    Arguments:
        target_file {str} -- [full string path to targets CSV]
    
    Returns:
        target_dict {dict} -- [dictionary of name, m/z, mobility from target list]
    """
    print(f'target_file = {target_file}')
    target_dict = {}
    target_data_list = read_data_csv(target_file)

    for data in target_data_list: 
        target, target_mz, target_mob = data[0], data[1], data[2] #target Name / Expected m/z / Mobility NOTE - are headers skipped?
        target_dict[target] = {'mz': float(target_mz), 'mobility': float(target_mob)}

    return target_dict

def check_hit(hit_mz, hit_mobility, target_data, mz_tolerance, mob_tolerance, mz_units='abs'):
    """[Parse through data for given m/z (absolute values) and mobility (percentage) with tolerances. 
        If value is a match, returns true. Otherwise, returns false]
    
    Arguments:
        hit_mz = [observed m/z value to check against target m/z value]
        hit_mobility = [observed m/z value to check against target m/z value]
        target_data = [APEX3D exported data file from .items in target_dict dictionary]
        mz_tolerance = [Selected threshold entered for m/z tolerance required for a 'hit' to be recorded]
        mob_tolerance = [Selected threshold entered for mobility tolerance in BINS required for a 'hit' to be recorded]
        mz_units='abs' = [Changed if absolute m/z threshold is not used (i.e. a percentage instead)]
    
    Returns:
        True if target value pair is  within acceptable tolerance. Returns False otherwise.
    """
    # t_mz, t_mobility  = target m/z, target mobility  
    t_mz, t_mobility = target_data['mz'], target_data['mobility']

    # hit_mz = observed m/z value

    if mz_units != 'abs':   #if not abs, the given m/z tolerance is read as a decimal fraction
        mz_tolerance = mz_tolerance*t_mz
        print(f'mz_tolerance is not set to percentage value of target ({t_mz}), current mz_tolerance = {mz_tolerance}')
        if mz_tolerance > 1:
            raise Exception(f'm/z tolerance is set as percentage but can\'t be - either set mz_units to \'abs\', not this: {mz_units} or change mz_tolerance to decimal fraction')

    if hit_mz >= t_mz - mz_tolerance and hit_mz <= t_mz + mz_tolerance:
        mob_tolerance = t_mobility*mob_tolerance
        if hit_mobility >= t_mobility - mob_tolerance and hit_mobility <= t_mobility + mob_tolerance:
            return True 
        return False 
    
    return False

def screen_hits_for_single_csv(data_csv, target_dict, mz_tolerance, mob_tolerance, mz_units='abs'):
    """[Appends "hits" to a new list, "hits_dict" for each "target"]
    
    Arguments:
        data_csv = [CSV in which original APEX3D output data is stored]
        target_dict = [From fetch_target_data, list of target m/s vs. mob pairs provided by user in CSV form]
        mz_tolerance = [Selected threshold entered for m/z tolerance required for a 'hit' to be recorded]
        mob_tolerance = [Selected threshold entered for mobility tolerance in BINS required for a 'hit' to be recorded]
        mz_units='abs' = [Changed if absolute m/z threshold is not used (i.e. a percentage instead)]
    
    Returns:
        hits_dict = [A dictionary of targets returning True from check_hit]
    """
    hits_dict = {}
    hits_list = []
    data_list = read_data_csv(data_csv)
    
    for target, target_data in target_dict.items():
        hits_list = []
        for data in data_list:
            # obs_mz, obs_mobility = float(data[2]), float(data[4]) #for older DriftScope v 2.2 APEX exports
            obs_mz, obs_mobility = float(data[2]), float(data[8])   #change to row 8 for new APEX output
            
            if check_hit(obs_mz, obs_mobility, target_data, mz_tolerance, mob_tolerance, mz_units):
                # relevant_data = [item for item in data[1:6]]
                relevant_data = [item for item in data[1:9]]    #change to row 9 to stop - includes up to row 8 which is mobility in new APEX data
                print(f'csv = {data_csv}')
                hits_list.append(relevant_data)

        hits_dict[target] = hits_list
    
    return hits_dict

def get_output_csv_path(input_csv, output_folder=None, out_string='hits'):
    #Find output folder path if it exists (otherwise make it)
    input_csv_name = os.path.basename(input_csv).replace('.csv', '')

    if not output_folder:
        output_folder = os.path.dirname(input_csv)
        output_folder = os.path.join(output_folder, 'SAMMmonitor Output')
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

    return os.path.join(output_folder, f'{input_csv_name}-{out_string}.csv')

def write_output_csv(output_csv, headers=['target_molecule', 'id','obs_mz','Rt', 'obs_mobility', 'intensity'],
                    delimitchar=','):

        with open (output_csv, 'w') as write_file:
            
            write = csv.writer(write_file, delimiter=delimitchar)
            write.writerow(headers)

def append_output_csv(output_csv, write_list, delimitchar=','):

    print(f'for {output_csv}, write list = {write_list}')
    with open(output_csv, 'a') as ofile:
            writer = csv.writer(ofile, delimiter=delimitchar)
            writer.writerow(write_list)

def write_hits_for_single_csv(data_csv, target_dict, mz_tolerance, mob_tolerance, 
                                out_folder=None, headers=['Target Formula','Index', 
                                'Observed m/z','m/z No Cal', 'RT', 'Intensity', 'Area', 'Counts', 'Mobility']):
                            # headers=['target_molecule','id', 'obs_mz','Rt',
                            #             'obs_mobility', 'intensity']):

    print(f'target_dict = {target_dict}')
    hits_dict = screen_hits_for_single_csv(data_csv, target_dict, 
                                        mz_tolerance, mob_tolerance)

    output_csv = get_output_csv_path(data_csv)
    write_output_csv(output_csv, headers)

    for target_molecule, hits_lists in hits_dict.items():

        for hit in hits_lists:
            if len(hit) > 0: 
                write_list = [target_molecule]
                write_list.extend(hit)
                append_output_csv(output_csv, write_list)

def write_hits_multiple_csvs(target_dict, csv_folder, 
                            mz_tolerance, mob_tolerance,
                            out_folder=None):
    
    csv_files = list_csv_data_files(csv_folder)

    for csv_file in csv_files:
        write_hits_for_single_csv(csv_file, target_dict, 
                                mz_tolerance, mob_tolerance,
                                out_folder)

def main(data_folder, targets_csv, mz_tolerance, mob_tolerance, mz_units='abs'): 
   
    target_dict = fetch_target_data(targets_csv)

    write_hits_multiple_csvs(target_dict, data_folder, mz_tolerance, mob_tolerance)

if __name__ == '__main__':
    main(data_folder, targets_csv, mz_tolerance, mob_tolerance)