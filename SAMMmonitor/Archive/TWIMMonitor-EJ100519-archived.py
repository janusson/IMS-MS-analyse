"""
Created: DD 090519
Script for screening ion mobility data for EJ and finding intensities of a list of known targets.
Modified: EJ 100519 - renamed TWIMMonitor.
"""
import os
import csv
import sys

def read_data_csv(csv_file, delimitchar=',', headers=True):
    """[Reads and passes on data from input .CSV file]
    
    Arguments:
    csv_file {str} -- [full str path to .csv file]
    
    Keyword Arguments:
    delimitchar {str} -- [delimiter for csv] (default: {','})
    
    Returns:
    data_list {list} -- [list of csv data by row]
    """ 
    data_list = []
    
    with open(csv_file) as f:
        csvreader = csv.reader(f, delimiter = delimitchar)
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

    print(f'target_file = {target_file}')
    target_dict = {}
    target_data_list = read_data_csv(target_file)

    for data in target_data_list: 
        target, target_mz, target_mob = data[0], data[1], data[2]
        target_dict[target] = {'mz': float(target_mz),
                                'mobility': float(target_mob)
                                }
    return target_dict 

def check_hit(hit_mz, hit_mobility, target_data,
                mz_tolerance, mob_tolerance, 
                abs_mz_tolerance, abs_mob_tolerance):

    t_mz, t_mobility = target_data['mz'], target_data['mobility']
    
    if not abs_mz_tolerance:
        mz_tolerance = mz_tolerance*t_mz
    if not abs_mob_tolerance:
        mob_tolerance = mob_tolerance*t_mobility

    if hit_mz >= t_mz - mz_tolerance and hit_mz <= t_mz + mz_tolerance:
        if hit_mobility >= t_mobility - mob_tolerance and hit_mobility <= t_mobility + mob_tolerance:
            return True 
        return False 
    
    return False

def screen_hits_for_single_csv(data_csv, target_dict, 
                                mz_tolerance, 
                                mob_tolerance,
                                abs_mz_tolerance=True,
                                abs_mob_tolerance=False):

    hits_dict = {}
    hits_list = []
    data_list = read_data_csv(data_csv)
    
    for target, target_data in target_dict.items():
        hits_list = []
        for data in data_list:
            obs_mz, obs_mobility = float(data[2]), float(data[4])
            
            if check_hit(obs_mz, obs_mobility, target_data, 
                        mz_tolerance, mob_tolerance, abs_mz_tolerance,
                        abs_mob_tolerance):
                relevant_data = [item for item in data[1:5]]
                hits_list.append(relevant_data)
        hits_dict[target] = hits_list
    
    return hits_dict

def get_output_csv_path(input_csv, output_folder=None,
                        out_string='hits'):

    input_csv_name = os.path.basename(input_csv).replace('.csv', '')

    if not output_folder:
        output_folder = os.path.dirname(input_csv)
        output_folder = os.path.join(output_folder, 'out')
    
    return os.path.join(output_folder, f'{input_csv_name}-{out_string}.csv')

def write_output_csv(output_csv, headers=['target_molecule', 'id','obs_mz','Rt', 'obs_mobility'],
                    delimitchar=','):

        with open (output_csv, 'w') as write_file:
            
            write = csv.writer(write_file, delimiter=delimitchar)
            write.writerow(headers)

def append_output_csv(output_csv, write_list, delimitchar=','):
    
    with open(output_csv, 'a') as ofile:
            writer = csv.writer(ofile, delimiter=delimitchar)
            writer.writerow(write_list)


def write_hits_for_single_csv(data_csv, target_dict,
                            mz_tolerance,
                            mob_tolerance,
                            out_folder=None,
                            headers=['id', 'obs_mz','Rt',
                                        'obs_mobility']):

    print(f'target_dict = {target_dict}')
    hits_dict = screen_hits_for_single_csv(data_csv, target_dict, 
                                        mz_tolerance, mob_tolerance)
   
    output_csv = get_output_csv_path(data_csv)
    write_output_csv(output_csv, headers)
    
    for target_molecule, hits_lists in hits_dict.items():
        n_hits = len(hits_lists)+1
        for hit in hits_lists:
            if len(hit) > 0: 
                write_list = [target_molecule]
                write_list.extend(hit)
                append_output_csv(output_csv, write_list)

def write_hits_multiple_csvs(target_dict, csv_folder, 
                            mz_tolerance, mob_tolerance,
                            out_folder=None, 
                            headers=['id', 'obs_mz', 'Rt',
                            'obs_mobility']):
    
    csv_files = list_csv_data_files(csv_folder)
    
    for csv_file in csv_files:
        write_hits_for_single_csv(csv_file, target_dict, 
                                mz_tolerance, mob_tolerance,
                                out_folder, headers)

data_folder = 'C:\Workbench (Local)\TWIMMonitor\EJ3-8'
targets_csv = 'C:\Workbench (Local)\TWIMMonitor\EJ3-8\Peak list (mz with DT) - EJ090519.csv'
mz_tolerance, mob_tolerance = 2, 0.1   # +/- 2 m/z and +/- 0.02 mobility


def main(data_folder, targets_csv, mz_tolerance, 
            mob_tolerance): 
   
    target_dict = fetch_target_data(targets_csv)

    write_hits_multiple_csvs(target_dict, data_folder, mz_tolerance, mob_tolerance)


if __name__ == '__main__':
    main(data_folder, targets_csv, mz_tolerance, mob_tolerance)







    


    



                




