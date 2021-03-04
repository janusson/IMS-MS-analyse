list1 = []


def integrate_targets(target_data):
    '''
    Combine analyte dictionary and Apex3D data to sum matching hits.
    '''
    #for each csv file

    for dataDir in csv_files:
        rawData = importSAMM3D(dataDir)
        mz_data, dt_data, counts = rawData['m/z'], rawData['DT'], rawData['Area']

        #for each analyte in experimental target reference data 
        for analyte in target_data.keys():
            formula = str(analyte)
            analyte_mz = target_data.get(analyte).get('mz')
            analyte_dt = target_data.get(analyte).get('mobility')
            # print(str(analyte_mz))

            for x in analyte_mz:
                for y in analyte_dt:
                    for experimental_mz in mz_data:
                        for experimental_dt in dt_data:
                            # if experimental_mz == (entry +/- mz_tolerance) and experimental_dt == (entry +/- mob_tolerance):
                            print('mz: ')
                            print(experimental_mz)
                            print('dt: ')
                            print(experimental_dt)
