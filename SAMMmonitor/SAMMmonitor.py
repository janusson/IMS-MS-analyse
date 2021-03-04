import sys, os, csv
from pathlib import Path
from datetime import datetime, time
import pandas as pd
import re

# default directory of Apex3D output data csv files
work_dir = os.getcwd(
    r'D:\2-SAMM\Programs\SAMM\database\experimental-target-list.csv')

# data_directory = Path(
#     r'D:\2-SAMM\Programs\SAMM\3D-TWIMS-extract\out') # apex files

data_directory = Path(r'D:\2-SAMM\Programs\SAMM\3D-TWIMS-extract\out')

# path of CSV file with target analyte
targets_csv = Path(
    r'D:\2-SAMM\Programs\SAMM\database\experimental-target-list.csv')

# directory of apex3d csv files
csv_files = [os.path.join(data_directory, csv_f)
             for csv_f in os.listdir(data_directory) 
             if csv_f[-4:] == '.csv']

# target m/z error and mobility tolerance
# FIXME adjust the peak detection settings, or use BA4
mz_tol, mob_tol = 10, 0.15 #(a.m.u., % dt bias)

# NOTE: See EJ3-60 experiments for monitoring data

### Main Functions
# reference csv import parameters (used in 'fetch_target_data' func.)
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
    '''Returns dictionary of exp. analyte targets from .csv file.
    Arguments:
    target_file {str} -- [full string path to targets CSV]
    Returns:
    target_dict {dict} -- [dictionary of name, m/z, mobility from target list]
    >>> # output example: 
    >>> {
        '[HMoO4]-': {'mz': 162.1, 'mobility': 18.17, 'charge': 1.0}, 
        '[HMo2O7]-': {'mz': 303.69, 'mobility': 25.25, 'charge': 1.0},
        ...
        }
    '''
    target_dict = {}
    target_data_file = read_data_csv(target_file)

    for data in target_data_file:
        target, target_mz, target_mob = data[0], float(data[2]), float(data[5])
        # create reference dict
        target_dict[target] = {
            'mz': target_mz, 
            'mobility': target_mob, # in bins
            'charge': int(data[4])
            }
    return target_dict

# experiment data import 
def import_apex3d(csv_path):
    '''
    Processes mass/mobility/area data from Apex3D .csv output file.
    Args:
        csv_path (string): filepath of an Apex3D .csv file

    Returns:
        pd.DataFrame: m/z, mobility, and intensity data in a dataframe object.
        >>> example output:
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
def set_tolerance(ion, ref_dic = fetch_target_data(targets_csv)):
    '''
    Sets m/z and dt check tolerance per-ion. Based on analyte dictionary.
    Considers charge of analyte.
    Args:
        ion (string): name of ion.
    Returns:
        floats: upper and lower m/z and DT ranges.
    '''
    target_mz = float(ref_dic[ion]['mz'])
    target_dt = float(ref_dic[ion]['mobility'])
    # adjust m/z tolerance for charge:
    mz_tol_z = mz_tol/ref_dic[ion]['charge']
    upperMZ, lowerMZ = float(target_mz + mz_tol_z), float(target_mz - mz_tol_z)
    upperDT, lowerDT = target_dt * (1 + mob_tol), target_dt * (1 - mob_tol)
    # print(f'. . . {ion} with mass range: {lowerMZ}-{upperMZ} m/z')
    # print(f'. . . {ion} with dt range: {lowerDT}-{upperDT} bins.')
    return float(upperMZ), float(lowerMZ), float(upperDT), float(lowerDT)

# find areas within m/z+DT range and sum
def find_match(raw_data, upperMZ, lowerMZ, upperDT, lowerDT):
    '''
    Checks raw apex3d data file for data matching threshold for each ion and
    returns Riemann sum of peak area. Note: base peak area should be used to
    avoid overlapping analyte signal.

    Args:
        raw_data (DataFrame): apex3d datafile to parse.
        upperMZ, lowerMZ, upperDT, lowerDT (float):
            Upper and lower m/z and drift time boundaries required for match.
    Returns:
        int: Riemann sum of data matching ion dt and m/z within tolerance.
    '''
    m_range = (raw_data['m/z'] >= lowerMZ) & (raw_data['m/z'] <= upperMZ)
    d_range = (raw_data['DT'] >= lowerDT) & (raw_data['DT'] <= upperDT)
    matches = raw_data[['m/z', 'DT', 'Area']].loc[(m_range & d_range), 'Area']
    match_area = int(matches.sum())
    # FIXME
    return match_area

def get_time_series(targets = fetch_target_data(targets_csv)):
    '''
    Calculates time-series abundance data for all target ions
    in each apex3D .csv experiment file in data directory. 

    Args:
        targets (dict, optional): Analyte dtms params.
        Defaults to fetch_target_data(targets_csv).

    Returns:
        DataFrame(data, columns = ['Inj.#', 'Ion', 'Base Peak Area'])
    '''
    list1 = []
    for apex_file in csv_files:
        raw_data = import_apex3d(apex_file)
        loc_inj = apex_file[-31:-28] # filter non numbers:
        inj_index = int(re.sub('[^0-9]', '', loc_inj))
        try: # set experiment and inj.#, or return error
            found = re.search('(-\D\D\d-)', apex_file[50:60]).group(1)
            exp_id = found[1:4]
            exp_inj_num = exp_id[2]
        except AttributeError:
            found = 'error, no experiment ID found'

        for ion in targets.keys():
            if len(ion)>1:
                upperMZ, lowerMZ, upperDT, lowerDT = set_tolerance(ion)
                ion_area = find_match(
                    raw_data, upperMZ, lowerMZ, upperDT, lowerDT)
                list1.append([exp_id, inj_index, exp_inj_num, ion, ion_area])

    time_series = pd.DataFrame(list1, columns = [
        'Exp. ID', 'Inj.#', 'Exp.#', 'Ion', 'Base Peak Area'])
    return time_series

def main():
    '''
    retrieves area data for ion target list and exports as .csv

    Returns:
        .csv file / None: output to ./SAMMmonitor/out
    '''
    # export time-series data as compressed file
    output_dir = Path(r'D:\2-SAMM\Programs\SAMM\SAMMmonitor\out')
    time_data = get_time_series()
    time_data.to_csv(f'{output_dir}\\apex-out.csv', compression = None)
    return None

if __name__ == '__main__':
    start_time = datetime.now()
    print(f'program start: {start_time}')
    main()
    print('### main program complete\n')
    print(f'runtime: {datetime.now()-start_time}')

### end main
