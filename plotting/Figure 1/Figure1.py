# Figure1.py
# Python 3.7.4
# Eric Janusson
# 150320

import os
import pandas as pd
import numpy as np
from cycler import cycler
from matplotlib import pyplot as plt

#Figure Defaults:
userInput = '57-158-BC4'  # Fig 1 is spectrum for 57-158-BC4
msRange = [150, 3000]
dtRange = [0, 200]
areaMin = 1

# Default colour schemes:
def setColourScheme():
    mSun = ['#003f5c', '#444e86', '#955196', '#dd5182', '#ff6e54', '#ffa600']
    malDiv = '#1e394a #7175ab #ffa7ef #ff7087 #cc6200'.split(' ')
    malPal = '#1e394a #414471 #893e78 #c23a53 #cc6200'.split(' ')
    bojackGrad = '#D04F6D #84486A #9C4670 #A75C87 #8C5D8B #7088B3 #71B2CA #8EE7F0 #B7F9F9 #A6F5F7'.split(
        ' ')
    return(mSun, malDiv, malPal, bojackGrad)
mSun, malDiv, malPal, bojackGrad = setColourScheme()

#   Default MPL Plot Settings
from matplotlib import rcParams
colors = cycler('color', mSun)
plt.rc('axes', edgecolor='black', axisbelow=False, grid=False, prop_cycle=colors)
plt.rc('grid', c='0.5', ls='-', lw=0.1)
plt.rc('xtick', direction='out', color='black')
plt.rc('ytick', direction='out', color='black')
plt.rc('patch', edgecolor='#003f5c')
plt.rc('lines', linewidth=0.18, aa=True)
font = {'family' : 'arial',
        # 'weight' : 'bold',
        'size'   : 16}
plt.rc('font', **font)  # pass in the font dict as kwargs
plt.rc('figure', edgecolor='white')

# Data import functions (From TWIMExtract and APEX3D Output) customized to user input (default: ID: 57-24-RA2)
def importSAMM2D(file2D):
    # Load 2D CSV files for FR, Z1, Z2
    # print('Enter EJ3-57 Experiment ID (Enter in the form: #-##-##-XX#): \n')
    # userInput = input('Example: 57-158-BC4')
    userInput = str(file2D)
    basePath = r'D:\2-SAMM\SAMM - Data Workup Folder\Data Workup (300919)\Experimental Data\3-57-SAMM2\2DExtract(3-57-2)'   #CSV file path
    frMS = str(basePath + r'\Full Range\MS\EJ3-' + userInput + r'-Sampling-2\MZ_EJ3-' +
               userInput + r'-Sampling-2_fn-1_#FullRange-POMSolv-Rangefile.txt_raw.csv')
    frDT = str(basePath + r'\Full Range\DT\EJ3-' + userInput + r'-Sampling-2\DT_EJ3-' +
               userInput + r'-Sampling-2_fn-1_#FullRange-POMSolv-Rangefile.txt_raw.csv')
    z1MS = str(basePath + r'\Z1\MS\EJ3-' + userInput + r'-Sampling-2\MZ_EJ3-' +
               userInput + r'-Sampling-2_fn-1_#POMSolv-Z1-RuleFile.rul_raw.csv')
    z1DT = str(basePath + r'\Z1\DT\EJ3-' + userInput + r'-Sampling-2\DT_EJ3-' +
               userInput + r'-Sampling-2_fn-1_#POMSolv-Z1-RuleFile.rul_raw.csv')
    z2MS = str(basePath + r'\Z2\MS\EJ3-' + userInput + r'-Sampling-2\MZ_EJ3-' +
               userInput + r'-Sampling-2_fn-1_#POMSolv-Z2-RuleFile.rul_raw.csv')
    z2DT = str(basePath + r'\Z2\DT\EJ3-' + userInput + r'-Sampling-2\DT_EJ3-' +
               userInput + r'-Sampling-2_fn-1_#POMSolv-Z2-RuleFile.rul_raw.csv')
    paths = [frMS, frDT, z1MS, z1DT, z2MS, z2DT]
    frScatter = ([pd.read_csv(i, skiprows=1)
                  for i in paths if os.path.lexists(i) and i[104:106] == r'Fu'])
    frScatter = pd.concat([frScatter[0], frScatter[1]], axis=1)
    frScatter.columns = ['m/z', 'Counts', 'Drift Time', 'Intensity']
    z1Scatter = ([pd.read_csv(i, skiprows=1)
                  for i in paths if os.path.lexists(i) and i[104:106] == r'Z1'])
    z1Scatter = pd.concat([z1Scatter[0], z1Scatter[1]], axis=1)
    z1Scatter.columns = ['m/z', 'Counts', 'Drift Time', 'Intensity']
    z2Scatter = ([pd.read_csv(i, skiprows=1)
                  for i in paths if os.path.lexists(i) and i[104:106] == r'Z2'])
    z2Scatter = pd.concat([z2Scatter[0], z2Scatter[1]], axis=1)
    z2Scatter.columns = ['m/z', 'Counts', 'Drift Time', 'Intensity']
    return frScatter, z1Scatter, z2Scatter, userInput

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

## Create Dataframes
specData, z1Data, z2Data, fileID = importSAMM2D(userInput)
data = importSAMM3D(userInput)

## Data Processing
# 3D Dimensions
dims = data[(data['m/z'] > msRange[0]) & (data['m/z'] < msRange[1]) #Set import scales
            & (data['DT'] > dtRange[0])
            & (data['DT'] < dtRange[1])
            & (data['Area'] > areaMin)]
# 3D Scales
dims[r'log(Area)'] = dims['Area'].apply(lambda x: np.log(x))
# 3D Sort
dims.sort_values('log(Area)', inplace=True)
dims[r'Normalized log(Area)'] = (dims['log(Area)']-dims['log(Area)'].min()
                                )/(dims['log(Area)'].max()-dims['log(Area)'].min())
# 3D Variables
mz, dt, area, = (dims['m/z'], dims['DT'], dims['Area'])
ppmError, dtError, countsError = (dims['m/z Error'], dims['DT Error'], dims['Area Error'])
# 2D Variables
msMass, msCounts, dtTime, dtIntensity = (specData['m/z'], specData['Counts'],
specData['Drift Time'], specData['Intensity'])

## Plotting
def mplDTMS():
    # MPL HEXBIN Plot
    # dtmsMap = plt.figure(figsize=(8, 8), dpi=600, facecolor='k', edgecolor='k')
    dtmsMap = plt.figure(figsize=(8, 8), dpi=600)
    dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')
    dtmsLayer1.set_title('DTMS Map', color='black')

    dtmsLayer1.hexbin(mz, dt,
                        C=area,
                        bins=(np.arange(len(dt))*0.5),  # Change to log for quantitative view
                        # bins='log'
                        gridsize=(250, 500),
                        # xscale='log',
                        # yscale='log'
                        # alpha=0.8,
                        # edgecolor=None
                        cmap='inferno' #'viridis' 'inferno'
                        )

    dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
    dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
    # dtmsLayer1.set(xlim=[150, 3000], ylim=[0, 200]) # No limit
    plt.tight_layout()
    dtmsMap.savefig("D:\Programming\SAMM\SAMMplot\Figure 1\Fig 1 Exports\TTTEST-mplDTMS.png")
    print('MPL Export Complete')

def dsMap():
    # Datashader 3D map
    import datashader as ds, datashader.transfer_functions as tf
    import holoviews as hv
    # from holoviews import opts
    from colorcet import bmw, bkr, bgyw, bkr, bgy, kbc, bmw, bmy, kb, bkr, CET_CBL2, isolum
    from matplotlib.cm import viridis, plasma, magma, inferno, cividis
    from functools import partial
    from datashader.utils import export_image
    from IPython.core.display import HTML, display

    # Create Canvas
    cvs = ds.Canvas(plot_width=1000//2, plot_height=1000//2,
                    x_range=(150, 1500), y_range=(12, 75))
                    # x_axis_type='linear', y_axis_type='linear'

    # Aggregate data

    agg = cvs.points(data, 'm/z', 'DT', ds.mean('Area')) #best respons so far
    # agg = cvs.points(data, 'm/z', 'DT')
    # agg = cvs.points(data, 'm/z', 'DT', ds.var('Area')) #ds.reductions??

    # Shade
    shade = tf.shade(
        agg,
        cmap=CET_CBL2,
        # cmap=bgyw, bmy,CET_CBL2,
        # color_key=None,
        how='eq_hist', # cbrt, log, linear, eq_hist
        # alpha=255,
        min_alpha=100,
        name='DTMS Map',
    )
    #bg colour, spread
    # tf.spread(shade, px=5, shape='circle')
    tf.Images(tf.set_background(shade, 'black'))
    # , tf.spread(shade, px = 10))
    #export figure
    # export = partial(export_image, background='black', export_path='Figure 1 - Data')
    # display(HTML('<style>.container { width:100% !important; }</style>'))
    # export(shade, 'Figure1-ds-simple')
    export_image(shade, filename='TTTESTdsMap', background='black', fmt='.png', export_path='D:\Programming\SAMM\SAMMplot\Figure 1\Fig 1 Exports\\')
    print('Datashader Export Complete')

def mplDTMS2():
    dtmsMap = plt.figure(figsize=(6, 6), dpi=600)
    dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')

    dtmsLayer1.set_title('DTMS Map', color='black')

    dtmsLayer1.hexbin(data['m/z'], data['DT'],
                        C=data['Area'],
                        bins=(np.arange(len(dt))*0.02),  # Change to log for quantitative view
                        # bins='log',
                        gridsize=(250, 500),
                        # xscale='log',
                        # yscale='log'
                        # alpha=0.8,
                        # edgecolor=None
                        cmap='inferno' #'viridis' 'inferno'
                        )

    dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
    dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
    # dtmsLayer1.set(xlim=[150, 3000], ylim=[0, 200]) # No limit
    plt.tight_layout()
    dtmsMap.savefig("D:\Programming\SAMM\SAMMplot\Figure 1\Fig 1 Exports\TTTESTmplDTMS2.png")
    print('MPL Export Complete')

## Plotting Axes (ms)

def mplDTMSaxes():
    # MPL HEXBIN Plot
    # dtmsMap = plt.figure(figsize=(8, 8), dpi=600, facecolor='k', edgecolor='k')
    dtmsMap = plt.figure(figsize=(8, 8), dpi=1200)
    dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')
    dtmsLayer1.set_title('DTMS Map', color='black')

    dtmsLayer1.hexbin([1,2], [1,2], gridsize=(250, 500))

    dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
    dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
    dtRange = ((12*(22.1)/200),(75*(22.1)/200))
    # dtmsLayer1.set(xlim=[150, 3000], ylim=[0, 200]) # No limit
    plt.tight_layout()
    dtmsMap.savefig("D:\Programming\SAMM\SAMMplot\Figure 1\Fig 1 Exports\TTTESTmplDTMSaxes.png")
    print('MPL Export Complete')


##Export Plots:
# Matplotlib hexbin
mplDTMS()
mplDTMS2()
# Datashader plot
dsMap()
# Axis
mplDTMSaxes()

cwd = str(os.getcwd())
print(r'Export Complete to: *-_-_-_-* ' + cwd + ' *-_-_-_-*')
