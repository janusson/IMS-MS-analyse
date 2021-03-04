# Figure4.py
# Python 3.7.4
# Eric Janusson
# 310320
import os
import pandas as pd
import numpy as np
import re
import matplotlib as mpl
from cycler import cycler
import colorcet as cc
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import pyplot as plt
import seaborn as sns

# cMaps
plasma = cm.get_cmap('plasma', 12)
viridis = cm.get_cmap('viridis', 12)
mSun = ['#955196', '#003f5c', '#444e86',  '#dd5182', '#ff6e54', '#ffa600']
malDiv = '#ffa7ef #1e394a #7175ab #cc6200 #ff7087 '.split(' ')
malPal = '#1e394a #414471 #893e78 #c23a53 #cc6200'.split(' ')
bojackGrad = '#D04F6D #84486A #9C4670 #A75C87 #8C5D8B #7088B3 #71B2CA #8EE7F0 #B7F9F9 #A6F5F7'.split(' ')

#   Default MPL Settings
colors = cycler('color', malDiv)
plt.rc('axes', edgecolor='black', axisbelow=False,
       grid=False, prop_cycle=colors)
font = {'family': 'arial',
        # 'weight' : 'bold',
        'size': 16}
plt.rc('font', **font)  # pass in the font dict as kwargs
plt.rc('figure', edgecolor='white')
plt.rc('xtick', direction='out', color='k')
plt.rc('ytick', direction='out', color='k')
plt.rc('grid', c='0.5', ls='-', lw=0.1)

# SAMMtrend Solvent Experiment Data Import
data = pd.read_csv(
    r'D:\Programming\SAMM\SAMMplot\Figure 4\EJ3-57-SAMM2trends.csv', delimiter=',', header='infer')
data.reset_index()

def getSolventsFromID():
    # Organize data by experiment type (solvent used and corresponding solvent)
    pos = list(r'RA, RB, RC, RD, BA, BB, BC, BD, GA, GB, GC, GD'.split(', '))
    solv = list(
        r"H2O MeOH EtOH MeCN D2O_40 D2O_20 D2O_10 D2O_40D D2O_40G MeCNG THFG H2OG".split(' '))
    posSolv = dict(zip(pos, solv))
    exptSolv = []
    exptCond = []
    exptRegex = re.compile(r'-\D\D\d-')
    for i in range(len(data['ID'])):  # For the length of the list of experiments
        # Create regex search for vial position in experiment file titles
        mo = re.search(exptRegex, data['ID'][i])
        vialPos = list(mo.group()[1:3])  # Put positions into list
        # vialPos = vialPos[1:3]
        vialPos = ''.join(vialPos)
        solvent = posSolv[vialPos]  # Conversion to solvents
        exptSolv.append(solvent)

        condNum = int(mo.group()[3])
        exptCond.append(condNum)
    return exptSolv, exptCond

# Add reaction information to dataframe
data['Solvent'], data['Condition'] = getSolventsFromID()
solvents = 'H2O MeOH EtOH MeCN D2O_40 D2O_20 D2O_10 D2O_40D D2O_40G MeCNG THFG H2OG'.split(' ')

# add FRIMS: Z1MS+Z2MS and FRIDT: Z1DT + Z2DT
data['FRIMS'] = data['Z1MS-LWI'] + (data['Z2MS-LWI']/0.5)
data['FRIDT'] = data['Z1MS-LWI'] + (data['Z2DT-LWI'])

data['FRIMS'] = data['FRIMS'].astype(float)
data['FRIDT'] = data['FRIDT'].astype(float)

# Choose solvents to plot below:
solvChoose = data[
    # Aqueous
    (data['Solvent'] == 'H2O')
    # Organics
    | (data['Solvent'] == 'MeOH')
    | (data['Solvent'] == 'EtOH')
    | (data['Solvent'] == 'MeCN')
    # Deuterated Solvents
    | (data['Solvent'] == 'D2O_10')
    | (data['Solvent'] == 'D2O_20')
    | (data['Solvent'] == 'D2O_40')
    # | (data['Solvent'] == 'D2O_40D')
    # | (data['Solvent'] == 'D2O_40G')
    # H3PO4 Template Additive
    # | (data['Solvent'] == 'H2OG')
    # | (data['Solvent'] == 'MeCNG')
    # | (data['Solvent'] == 'THFG')
]



# Select from data containing ID FRIMS FRIDT Solvent and Condition, and bounds of data
friData = pd.DataFrame(deuterated[['FRIMS','FRIDT','ID','Solvent','Condition']])
xMin = friData['FRIMS'].min()
xMax = friData['FRIMS'].max()
yMin = friData['FRIDT'].min()
yMax = friData['FRIDT'].max()

# comparisons
nr = friData[friData['Condition']<3.5]
aqueous = data[data.Solvent.str.contains('H2O')]
organic = data[~data.Solvent.str.contains('2O')]
deuterated = solvChoose[solvChoose.Solvent.str.contains('2O')]
