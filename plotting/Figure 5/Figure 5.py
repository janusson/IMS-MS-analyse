# Figure5.py
# Plot Z2 species in H2O vs. D2O reactions
# Python 3.7.4
# Eric Janusson
# 150320
import os
import pandas as pd
import numpy as np
# Custom colour schemes:
def setColourScheme():
    # miami sunset
    mSun = ['#003f5c', '#444e86', '#955196', '#dd5182', '#ff6e54', '#ffa600']
    # maliwan divergent
    malDiv = '#1e394a #7175ab #ffa7ef #ff7087 #cc6200'.split(' ')
    # maliwan palette
    malPal = '#1e394a #414471 #893e78 #c23a53 #cc6200'.split(' ')
    # bojack gradient
    bojackGrad = '#D04F6D #84486A #9C4670 #A75C87 #8C5D8B #7088B3 #71B2CA #8EE7F0 #B7F9F9 #A6F5F7'.split(
        ' ')
    return(mSun, malDiv, malPal, bojackGrad)
mSun, malDiv, malPal, bojackGrad = setColourScheme()

# Data import functions (From TWIMExtract and APEX3D Output) customized to user input (default: ID: 57-24-RA2)
def importSAMM2D(userInput=None):
    # Load 2D CSV files for FR, Z1, Z2
    # print('Enter EJ3-57 Experiment ID (Enter in the form: #-##-##-XX#): \n')
    # userInput = input('Example: 57-158-BC4')
    # userInput = '57-158-BC4'
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

# Create Dataframes
frScatter, z1Scatter, z2Scatter, fileID = importSAMM2D('57-158-BC4')
frScat2, z1Scat2, z2Scat2, fileID2 = importSAMM2D('57-26-RA4')

# Data processing
z2Scatter = z2Scatter[
            (z2Scatter['m/z'] > 300) 
            & (z2Scatter['m/z'] < 1100)  
            & (z2Scatter['m/z'] < 1100)]

z2Scat2 = z2Scat2[
            (z2Scat2['m/z'] > 300) 
            & (z2Scat2['m/z'] < 1100)  
            & (z2Scat2['m/z'] < 1100)
            ]


## Plotting
import matplotlib as mpl
from cycler import cycler
from matplotlib import pyplot as plt

msRange = (300, 1100)

#   Default MPL Settings
colors = cycler('color', mSun)

from matplotlib import rcParams
plt.rc('axes', edgecolor='gray', axisbelow=False, grid=False, prop_cycle=colors)
plt.rc('grid', c='0.5', ls='-', lw=0.1)
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#003f5c')
plt.rc('lines', linewidth=0.18, aa=True)
font = {'family' : 'arial',
        'weight' : 'bold',
        'size'   : 16}
plt.rc('font', **font)  # pass in the font dict as kwargs

def plotMS(scatterData, scatterData2, titleCharge):
    fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False, figsize=(8,8), dpi=600)
    charge = titleCharge

    ax[0].plot(scatterData['m/z'], scatterData['Counts'], color=mSun[0])
    ax[0].fill_between(scatterData['m/z'], 0, scatterData['Counts'], facecolor=mSun[0])
    ax[0].set_title('Figure 5')
    ax[0].set_ylabel('Intensity (1e5)', color='gray')
    ax[0].set_title(charge + ' Mass Spectrum of ' + fileID, color='gray')
    ax[0].set_ylim(bottom=0)

    ax[1].plot(scatterData2['m/z'], scatterData2['Counts'], color=mSun[3])
    ax[1].fill_between(scatterData2['m/z'], 0, scatterData2['Counts'], facecolor=mSun[3])
    ax[1].set_title(charge + ' Mass Spectrum of ' + fileID2, color='gray')
    ax[1].set_xlabel('$\it{m/z}$', color='gray')
    ax[1].set_ylabel('Intensity (1e5)', color='gray')
    ax[1].invert_yaxis()
    ax[1].set_ylim(top=0)

    plt.xlim(msRange)

    ax[0].legend([None, str(fileID)])
    ax[1].legend([None, str(fileID2)])

    ax[0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.tight_layout()

    # plt.gcf().subplots_adjust(bottom=0.15, right = 0.3)
    plt.savefig("D:\Programming\SAMM\SAMMplot\Figure 5\Figure5.png", dpi=600)
    print('Figure exported as: D:\Programming\SAMM\SAMMplot\Figure 5\Figure5.png')

    # plt.savefig("Figure5-MS-" + charge + "-" + fileID + ' and ' + fileId2 + ".png", dpi=600)


plotMS(z2Scatter, z2Scat2, 'Z2')