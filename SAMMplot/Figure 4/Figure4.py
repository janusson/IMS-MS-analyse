# Figure4.py
# Plot results of polyoxomolybdate formation under screened reaction conditions
# "How does the relationship between these two variables change as a function of a third variable?”
# Python 3.7.4
# Eric Janusson
# 310320
import os
import pandas as pd
import numpy as np
import re

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

## Data Import
# userInput = input('Input path of CSV File: ')
# data = pd.read_csv(userInput)
data = pd.read_csv(
    r'D:\Programming\SAMM\SAMMplot\Figure 4\EJ3-57-SAMM2trends.csv', delimiter=',', header='infer')
data.reset_index()
data.set_index("ID")

def getSolventsFromID():
    #Organize data by experiment type (solvent used and corresponding solvent)
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
data['Solvent'], data['Condition'] = getSolventsFromID()

# def spotCheck():
# # Manual Spot Check:
#     for num in range(len(data['Solvent'])):
#         print('')
#         print('Row: ' + str(data['ID'].iloc[num])[12:18])
#         print('Solvent: ' + data['Solvent'][num])
#         print('')

### Plotting
import matplotlib as mpl
from cycler import cycler
import colorcet as cc
from matplotlib import pyplot as plt
import seaborn as sns

#   Default MPL Settings
colors = cycler('color', malPal)
# plt.rc('figure', edgecolor='k')
plt.rc('axes', edgecolor='gray', axisbelow=False, grid=False, prop_cycle=colors)
plt.rc('grid', c='0.5', ls='-', lw=0.1)
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#003f5c')
plt.rc('lines', linewidth=0.1, aa=True)

## Data Processing
# List of solvents: H2O MeOH EtOH MeCN D2O_40 D2O_20 D2O_10 D2O_40D D2O_40G MeCNG THFG H2OG
solventPlot = data[
            (data['FRMS'] > 0) & ( 
            (data['Solvent'] == 'H2O') 
            | (data['Solvent'] == 'MeOH')
            | (data['Solvent'] == 'EtOH')
            | (data['Solvent'] == 'MeCN')
            ## Deuterated Solvents
            # | (data['Solvent'] == 'D2O_10')
            # | (data['Solvent'] == 'D2O_20')
            # | (data['Solvent'] == 'D2O_40')
            # | (data['Solvent'] == 'D2O_40D')
            # | (data['Solvent'] == 'D2O_40G')
            ## H3PO4 Conditions
            # | (data['Solvent'] == 'H2OG')
            # | (data['Solvent'] == 'MeCNG')
            # | (data['Solvent'] == 'THFG')
            )
            ]
## Scales
# dims[r'log(Area)'] = dims['Area'].apply(lambda x: np.log(x))

## Sort
# solventPlot.sort_values(solventPlot['FRMS'], inplace=True)

## Normalize
# dims[r'Normalized log(Area)'] = (dims['log(Area)']-dims['log(Area)'].min()
#                                  )/(dims['log(Area)'].max()-dims['log(Area)'].min())

## Figure 4 Plot
figure4 = sns.pairplot(
    data=solventPlot,
    hue='Solvent',
    # hue_order='Condition',
    # palette='magma',
    palette='magma',
    vars=['Z2MS','Z2DT'],
    # x_vars='Z2MS',
    # y_vars='Z2DT',
    kind='reg',
    # diag_kind='hist',
    # markers=None,
    height=3,
    # col='Solvent',
    # col_wrap=3,
    aspect=1,
    dropna=True,
    # size='Condition',
)
#Change alpha
plt.tight_layout()
# plt.plot()
figure4.savefig('Figure4-a.png') # Save figure
print('Figure file exported as Figure4.png')


## Annotation and descriptive stats:
# https://www.statsmodels.org/stable/index.html

## Supporting Info
# df = solventPlot[['FRMS', 'FRDT', 'Solvent']]
# df.sort_values(by='Solvent', ascending=True, kind='quicksort', inplace=True)
# fig4SI = sns.pairplot(data=df, hue='Solvent', hue_order=None, palette=None, vars=None, x_vars=None, y_vars=None, kind="scatter",
#              diag_kind="auto", markers=None, height=2.5, aspect=1, dropna=True, plot_kws=None, diag_kws=None, grid_kws=None, size=None)

# sns.pairplot(
#     solventPlot,
#     # markers = ["o", "s"],
#     x_vars = ['Z1MS-LWI', 'Z2MS-LWI'],
#     y_vars = ['Z1DT-LWI', 'Z2DT-LWI'],
#     kind='reg',
#     height=6,
#     aspect=1,
#     dropna=True,
#     hue='Solvent',
#     # hue_order= ['Solvent']
#     # xlim=(int(solventPlot['Z2MS-LWI'].min())*-1, int(solventPlot['Z2MS-LWI'].max())*1.1),
#     # ylim=(int(solventPlot['Z2DT-LWI'].min())*-1, int(solventPlot['Z2DT-LWI'].max())*1.1)
# )
# plt.show()