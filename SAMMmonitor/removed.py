bin



def check_hit(hit_mz, data_mob, target_data, mz_tolerance, mob_tolerance):
    # DEPRECATED
    '''
    [Parse through data for given m/z (absolute values) and mobility (percentage) with tolerances.
    If value is a match, returns true. Otherwise, returns false]

    Arguments:
    hit_mz = [observed m/z value to check against target m/z value]
    data_mob = [observed m/z value to check against target m/z value]
    target_data = [APEX3D exported data file from .items in target_dict dictionary]
    mz_tolerance = [Selected threshold entered for m/z tolerance required for a 'hit' to be recorded]
    mob_tolerance = [Selected threshold entered for mobility tolerance in BINS required for a 'hit' to be recorded]
    mz_units='abs' = [Changed if absolute m/z threshold is not used (i.e. a percentage instead)]

    Returns: True if target value pair is within acceptable tolerance. Returns False otherwise.
    '''
    
    t_mz, target_mob = target_data['mz'], target_data['mobility']

    if hit_mz >= t_mz - mz_tolerance and hit_mz <= t_mz + mz_tolerance:
        mob_tolerance = target_mob * mob_tolerance
        if data_mob >= target_mob - mob_tolerance and data_mob <= target_mob + mob_tolerance:
            return True
        return False

    return False

def screen_hits_for_single_csv(data_csv, target_dict, mz_tolerance, mob_tolerance):
    '''
    [Appends valid hits in data with a given tolerance to a new list {tbd} and dictionary 'targ_dict' for each 'target']

    Arguments:
        data_csv = [CSV in which original APEX3D output data is stored]
        target_dict = [From fetch_target_data, list of target m/s vs. mob pairs provided by user in CSV form]
        mz_tolerance = [Selected threshold entered for m/z tolerance required for a 'hit' to be recorded]
        mob_tolerance = [Selected threshold entered for mobility tolerance in BINS required for a 'hit' to be recorded]
        mz_units='abs' = [Changed if absolute m/z threshold is not used (i.e. a percentage instead)]

    Returns:
        targ_dict = [A dictionary of targets returning True from check_hit]
        Incompatible with DriftScope v 2.2 (ex: APEX exports use col 4 of .csv file)
    '''
    targ_dict = {}
    hits_list = []
    data_list = read_data_csv(data_csv)

    for target, target_data in target_dict.items():
        hits_list = []
        for data in data_list:
            # obs_mz, obs_mobility = float(data[2]), float(data[4]) 
            # for older DriftScope v 2.2 APEX exports
            obs_mz, obs_mobility = float(data[2]), float(data[8])

            if check_hit(obs_mz, obs_mobility, target_data, mz_tolerance, mob_tolerance):
                relevant_data = [item for item in data[1:9]]
                # print(f'csv = {data_csv}')
                hits_list.extend(relevant_data) # append to extend
                print(f'Hit: + {relevant_data}')
        targ_dict[target] = hits_list

    return targ_dict
