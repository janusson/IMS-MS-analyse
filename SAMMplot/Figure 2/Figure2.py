# Figure2.py
# Python 3.7.4
# Eric Janusson
# 150320

import matplotlib.pyplot as plt
import matplotlib as mpl
import mpl_scatter_density
from matplotlib import rcParams
import os
import pandas as pd
import numpy as np
from cycler import cycler

# Figure 2 Default:
userInput = '57-158-BC4'    # Figure 2 uses 57-158-BC4 data
msRange = [780, 1100]
dtRange = [30, 50]
areaMin = 1
dtTime = [num*((22.1)/200) for num in dtRange]  # time in ms

# Custom colour schemes:


def setColourScheme():
    mSun = ['#003f5c', '#444e86', '#955196', '#dd5182', '#ff6e54', '#ffa600']
    malDiv = '#1e394a #7175ab #ffa7ef #ff7087 #cc6200'.split(' ')
    malPal = '#1e394a #414471 #893e78 #c23a53 #cc6200'.split(' ')
    bojackGrad = '#D04F6D #84486A #9C4670 #A75C87 #8C5D8B #7088B3 #71B2CA #8EE7F0 #B7F9F9 #A6F5F7'.split(
        ' ')
    return(mSun, malDiv, malPal, bojackGrad)


mSun, malDiv, malPal, bojackGrad = setColourScheme()


#   Default MPL Settings
colors = cycler('color', mSun)
plt.rc('axes', edgecolor='black', axisbelow=False,
       grid=False, prop_cycle=colors)
font = {'family': 'arial',
        # 'weight' : 'bold',
        'size': 16}
plt.rc('font', **font)  # pass in the font dict as kwargs
plt.rc('figure', edgecolor='white')

# Data import functions (From TWIMExtract and APEX3D Output) customized to user input (default: ID: 57-24-RA2)


def importSAMM2D(file2D):
    # Load 2D CSV files for FR, Z1, Z2
    # print('Enter EJ3-57 Experiment ID (Enter in the form: #-##-##-XX#): \n')
    # userInput = input('Example: 57-158-BC4')
    userInput = str(file2D)
    # CSV file path
    basePath = r'D:\2-SAMM\SAMM - Data Workup Folder\Data Workup (300919)\Experimental Data\3-57-SAMM2\2DExtract(3-57-2)'
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


# Create Dataframes
specData, z1Data, z2Data, fileID = importSAMM2D(userInput)
data = importSAMM3D(userInput)

# Data Processing
dims = data[(data['m/z'] > msRange[0]) & (data['m/z'] < msRange[1]) &
            (data['DT'] > dtRange[0]) & (data['DT'] < dtRange[1])
            & (data['Area'] > areaMin)]
mz, dt, area, = (dims['m/z'], dims['DT'], dims['Area'])

# Scales
dims[r'log(Area)'] = dims['Area'].apply(lambda x: np.log(x))
# dims[r'DT (ms)'] = data['DT'].apply(lambda x: (x*0.1105))

# Sort
# Problem with sorting copy
dims.sort_values('Area', inplace=True, ascending=False)

# Plotting
# Plot scatter density (datashader MPL)


def mplScatDen(apex3Ddata):
    x = apex3Ddata['m/z']
    y = apex3Ddata['DT']
    fig = plt.figure(figsize=(7.23420, 6.34827), dpi=1200)
    # figsize = 48.58 wide x 54.57
    ax = fig.add_subplot(
        1, 1, 1, projection='scatter_density', facecolor='black')

    density = ax.scatter_density(x, y,
                                 downres_factor=4,
                                 c=apex3Ddata[r'log(Area)'],
                                 cmap='magma',
                                 alpha=1
                                 )
    ax.set_xlim(780, 1060)
    ax.set_ylim(30, 50)
    ax.set_title('Figure 2', color='black')
    ax.set_xlabel('$\it{m/z}$', color='black')
    ax.set_ylabel('Drift Time (ms)', color='black')
    # fig.colorbar(apex3Ddata[r'log(Area)'], label='Signal')
    plt.tight_layout()
    # plt.show()
    plt.savefig(
        r'D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 Exports\fig2-scatter-density-mpl.png')
    print('MPL Scatter Export Complete')


# Plotting Axes (ms)
def mplDTMSaxes():
    # MPL HEXBIN Plot
    # dtmsMap = plt.figure(figsize=(8, 8), dpi=600, facecolor='k', edgecolor='k')
    dtmsMap = plt.figure(figsize=(8, 8), dpi=1200)
    dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')
    dtmsLayer1.set_title('Figure 2 Axes', color='black')

    dtmsLayer1.scatter([1, 2], [1, 2])

    dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
    dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
    # dtRange = ((12*(22.1)/200),(75*(22.1)/200))
    dtmsLayer1.set(xlim=msRange, ylim=dtTime)
    plt.tight_layout()
    dtmsMap.savefig(
        'D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 Exports\Figure2-axes.svg')
    print('Axes Export Complete')

# 2D Plotting


def separateData(dataset):
    msData = dataset.drop(['Drift Time', 'Intensity'], axis=1)
    dtData = dataset.drop(['m/z', 'Counts'], axis=1)
    msData = msData[(msData['m/z'] > msRange[0]) &
                    (msData['m/z'] < msRange[1])]
    dtData = dtData[(dataset['Drift Time'] > 3.315) &
                    (dataset['Drift Time'] < 5.525)]
    return msData, dtData


frMS, frDT = separateData(specData)
z1MS, z1DT = separateData(z1Data)
z2MS, z2DT = separateData(z2Data)

# Mass Spectrum


def massSpecerize(dataset):
    cvs = plt.figure(figsize=(7.23420, 2.41140), dpi=1200)
    msLayer1 = cvs.add_axes([0.1, 0.1, 0.8, 0.8])
    # inset = figure1.add_axes([0.55, 0.65, 0.3, 0.2]) # Inset
    # inset.set_title('Mobilogram')
    # inset.plot(dtTime, dtIntensity)
    msLayer1.set_title(str(userInput) + ' Mass Spectrum', color='k')
    msLayer1.plot(dataset['m/z'], dataset['Counts'], lw=0.3)
    msLayer1.fill_between(
        dataset['m/z'], 0, dataset['Counts'], facecolor=str(mSun[0]), alpha=0.1)
    msLayer1.set_xlabel('$\it{m/z}$', color='k')
    msLayer1.set_ylabel('Intensity', color='k')
    plt.locator_params(axis='y', nbins=4)
    plt.xlim(msRange)
    plt.ylim(0)
    plt.tight_layout()
    plt.savefig(r'D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 Exports\\' +
                str(userInput) + "-Mass Spectrum.svg", dpi=1200)

# Mobilogram


def mobilorize(dataset):
    cvs = plt.figure(figsize=(6.34827, 2.11609), dpi=600)
    dtLayer1 = cvs.add_axes([0.1, 0.1, 0.8, 0.8])
    dtLayer1.set_title(str(userInput) + ' Mobilogram', color='k')
    dtLayer1.scatter(dataset['Drift Time'],
                     dataset['Intensity'], color=str(mSun[2]), lw=1)
    # Spline connector
    akimaDF = pd.read_csv(
        'D:\Programming\SAMM\SAMMplot\Figure 2\Misc\spline.csv')
    dtLayer1.plot(akimaDF['DT'], akimaDF['Spline'], color=str(mSun[2]), lw=1)
    # dtLayer1.fill_between(dataset['Drift Time'], 0, dataset['Intensity'], facecolor=str(mSun[2]), alpha=0.2)
    dtLayer1.fill_between(
        akimaDF['DT'], 0, akimaDF['Spline'], facecolor=str(mSun[2]), alpha=0.2)
    dtLayer1.set_xlabel('Drift Time (ms)', color='k')
    dtLayer1.set_ylabel('Intensity', color='k')
    # dtLayer1.yaxis.tick_right()
    plt.locator_params(axis='y', nbins=3)
    plt.xlim(dataset['Drift Time'].max(), dataset['Drift Time'].min())
    plt.ylim(0)
    plt.tight_layout()
    # plt.savefig(r'D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 Exports\\' + "normalSpline-test.svg", dpi=1200)
    plt.savefig(r'D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 Exports\\' +
                str(userInput) + "-Mobilogram.svg", dpi=1200)
    print('Mobilogram Exported')


def hexbin1(dataSet):
    from colorcet import bmw, bkr, bgyw, bkr, bgy, kbc, bmw, bmy, kb, bkr, CET_CBL2, isolum, CET_L8
    from matplotlib.cm import viridis, plasma, magma, inferno, cividis

    dataSet[r'DT'] = dims['DT'].apply(lambda x: x*22.105125/200)
    dtmsMap = plt.figure(figsize=(6, 6), dpi=1200)
    dtmsLayer1 = dtmsMap.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='k')

    dtmsLayer1.set_title('DTMS Map', color='black')

    dtmsLayer1.hexbin(dataSet['m/z'], dataSet['DT'],
                      C=dataSet['Area'],
                      # bins=(np.arange(len(dataSet['DT'])*0.02)),  # Change to log for quantitative view
                      bins='log',
                      gridsize=(300, 500),
                      # gridsize = (500, 1000),
                      linewidths=1,
                      # mincnt = 0,   ### PLAY WITH MIN COUNT AND VMIN TO ADJUST
                      # vmin = 0,
                      # xscale='log',
                      # yscale='log'
                      # alpha=0.8,
                      # edgecolor=None
                      cmap='cet_CET_L8'  # 'viridis' 'inferno'
                      )

    dtmsLayer1.set_xlabel('$\it{m/z}$', color='black')
    dtmsLayer1.set_ylabel('Drift Time (ms)', color='black')
    # dtmsLayer1.set(xlim=msRange, ylim=dtRange)
    plt.tight_layout()
    dtmsMap.savefig(
        r"D:\Programming\SAMM\SAMMplot\Figure 2\Figure 2 Exports\Figure2-Hexbin-CET-L8.svg")
    print('Hexbin Exported')


# Export Plots:
# 2D Data
mobilorize(frDT)
massSpecerize(frMS)
# 3D Data
mplDTMSaxes()
mplScatDen(dims)
hexbin1(dims)

cwd = str(os.getcwd())
print(r'Export Complete to: *-_-_-_-* ' + cwd + ' *-_-_-_-*')