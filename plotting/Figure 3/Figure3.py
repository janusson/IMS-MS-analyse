# Figure3.py
# Python 3.7.4
# Eric Janusson
# 150320
import matplotlib.pyplot as plt
import mpl_scatter_density
from matplotlib import rcParams
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
from cycler import cycler

#Figure Defaults:
userInput = '57-176-BD2'    # Figure 3 uses 57-176-BD2 data
msRange = [150, 3000]
dtRange = [0, 200]
areaMin = 1

# Custom colour schemes:
def setColourScheme():
    mSun = ['#003f5c', '#444e86', '#955196', '#dd5182', '#ff6e54', '#ffa600']
    malDiv = '#1e394a #7175ab #ffa7ef #ff7087 #cc6200'.split(' ')
    malPal = '#1e394a #414471 #893e78 #c23a53 #cc6200'.split(' ')
    bojackGrad = '#D04F6D #84486A #9C4670 #A75C87 #8C5D8B #7088B3 #71B2CA #8EE7F0 #B7F9F9 #A6F5F7'.split(
        ' ')
    return(mSun, malDiv, malPal, bojackGrad)
mSun, malDiv, malPal, bojackGrad = setColourScheme()

def importSAMM3D(file3D):
    # Load Apex3D CSV files for given experiment
    # print('Enter EJ3-57 Experiment ID (Enter in the form: #-##-##-XX#): ') #TEST
    # userInputApex = input('Example: 57-24-RA2') #TEST
    userInputApex = str(file3D)

    apexPath = r'D:\\2-SAMM\SAMM - Data Workup Folder\Data Workup (300919)\SAMM3D Extracts\APEX Output(3-57)'
    apexMS = str(apexPath + r'\Full Range\MS\EJ3-' + userInputApex +
                 r'-Sampling-2\MZ_EJ3-' + r'-Sampling-2_Apex3DIons.csv')
    apexMS = str('D:\\2-SAMM\SAMM - Data Workup Folder\Data Workup (300919)\SAMM3D Extracts\APEX Output(3-57)\EJ3-' +
                 userInputApex + '-Sampling-2_Apex3DIons.csv')
    apexDF = pd.read_csv(apexMS)
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
        columns=['m/z', 'DT', 'Area', 'm/z Error', 'DT Error', 'Area Error'])
    return newApexDF

#   Default MPL Settings
def mplDefaults():
    colors = cycler('color', mSun)
    plt.rc('axes', edgecolor='black', axisbelow=False,
        grid=False, prop_cycle=colors)
    font = {'family': 'arial',
            # 'weight' : 'bold',
            'size': 16}
    plt.rc('font', **font)  # pass in the font dict as kwargs
    plt.rc('figure', edgecolor='white')
mplDefaults()

# Create Dataframes
data = importSAMM3D(userInput)# Create Dataframes for 3D data

# Data Processing
dims = data[(data['m/z'] > msRange[0]) & (data['m/z'] < msRange[1]) &
        (data['DT'] > dtRange[0]) & (data['DT'] < dtRange[1])
        & (data['Area'] > areaMin)]

# Scales
dims[r'log(Area)'] = dims['Area'].apply(lambda x: np.log(x))
# dims[r'DT (ms)'] = data['DT'].apply(lambda x: (x*0.1105))

# Sort
# Potential problem with sorting copy
dims.sort_values('Area', inplace=True, ascending=False)

#Plotting
# Plot scatter density (datashader MPL)
# def mplScatDen():
    # x = dims['m/z']
#     y = dims['DT']
#     fig = plt.figure(figsize=(6, 6), dpi=1200)
#     # figsize = 48.58 wide x 54.57
#     ax = fig.add_subplot(
#         1, 1, 1, projection='scatter_density', facecolor='black')

#     density = ax.scatter_density(x, y,
#                                 #  downres_factor=0,
#                                  c=dims[r'log(Area)'],
#                                  cmap='magma',
#                                  alpha=1
#                                  )
#     # ax.set_xlim(780, 1060)
#     # ax.set_ylim(30, 50)
#     ax.set_title('Figure 3', color='black')
#     ax.set_xlabel('$\it{m/z}$', color='black')
#     ax.set_ylabel('Drift Time (ms)', color='black')

#     # fig.colorbar(dims[r'log(Area)'], label='Signal')
#     plt.tight_layout()
#     # plt.show()
#     plt.savefig(r'D:\Programming\SAMM\SAMMplot\Figure 3\Figure 3 - MPLScatterDensity.png')
#     print('MPL Scatter Export Complete')
# mplScatDen()

# Plotting Axes (ms)
# def mplDTMSaxes():
#     # MPL HEXBIN Plot
#     # dtmsMap = plt.figure(figsize=(8, 8), dpi=600, facecolor='k', edgecolor='k')
#     dtmsMap = plt.figure(figsize=(8, 8), dpi=1200)
#     dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')
#     dtmsLayer1.set_title('Figure 2 Axes', color='black')

#     dtmsLayer1.scatter([1, 2], [1, 2])

#     dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
#     dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
#     # dtRange = ((12*(22.1)/200),(75*(22.1)/200))
#     dtmsLayer1.set(xlim=msRange, ylim=dtTime)
#     plt.tight_layout()
#     dtmsMap.savefig('D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 - Exports\Figure2-axes.svg')
#     print('Axes Export Complete')
# mplDTMSaxes()

def hexbin1(dataSet):
    from colorcet import bmw, bkr, bgyw, bkr, bgy, bmy, CET_CBL2, isolum, CET_L8
    from matplotlib.cm import viridis, plasma, magma, inferno, cividis
    dataSet[r'DT'] = dataSet['DT'].apply(lambda x: x*22.105125/200)     #Convert DT to ms - dataSet or dims?
    dtmsMap = plt.figure(figsize=(4, 4), dpi=800)  #create canvas
    dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')  

    # Sort
    dataSet.sort_values('log(Area)', inplace=True, ascending=True)
    # dataSet.sort_values('Area', inplace=True, ascending=True)

    dtmsLayer1.hexbin(dataSet['m/z'], dataSet['DT'], 
                        C=dataSet['log(Area)'],
                        # bins=(np.arange(len(dataSet['DT'])*0.02))
                        bins='log',
                        gridsize=(450, 450),
                        linewidths = 2.2, # 2.2
                        mincnt = 5,   ### Minimum log intensity ~5
                        alpha=0.7, # 0.5
                        edgecolor='face',
                        # hatch = 'O' #{'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
                        cmap = 'cet_bgyw' #cet_bmw or bgyw
                        )
    dtmsLayer1.set_title('DTMS Map', color='black')    #Labels
    dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
    dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
    dtmsLayer1.set(xlim=[150,1200], ylim=[1.5, 6])    # Ranges
    plt.tight_layout()
    dtmsMap.savefig(r"D:\Programming\SAMM\SAMMplot\Figure 3\Figure3-Hexbin-" + userInput + r"-bgyw.png")
    dtmsMap.savefig(r"D:\Programming\SAMM\SAMMplot\Figure 3\Figure3-Hexbin-" + userInput + r"-bgyw.svg")
    print('Hexbin Export of ' + userInput + ' Data Complete')

# Export Plots:
hexbin1(dims)

cwd = str(os.getcwd())
print(r'Export Complete to: *-_-_-_-* ' + cwd + ' *-_-_-_-*')