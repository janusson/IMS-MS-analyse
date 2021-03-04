# Figure4.py
# Python 3.7.4
# Eric Janusson
# 310320
import os
import pandas as pd
import re

# SAMMtrend Solvent Experiment Data Import
experiment = 'EJ3-57'
pathName = r'D:\Programming\SAMM\SAMMplot\Figure 4\EJ3-57-SAMM2trends.csv'
data = pd.read_csv(pathName, delimiter=',', header='infer')
data.reset_index()

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

print(f'Adding {experiment} Information...\n')
data['Solvent'], data['Condition'] = getSolventsFromID()
solvents = 'H2O MeOH EtOH MeCN D2O_40 D2O_20 D2O_10 D2O_40D D2O_40G MeCNG THFG H2OG'.split(' ')

print(f'Collecting Weighted Charge Area from {experiment}: Z1MS+Z2MS and FRIDT: Z1DT + Z2DT...\n')

# Do not use FRIMS for charge separation
# Total area of integrated cluster masses
data['FRIMS'] = data['Z1MS-LWI'] + data['Z2MS-LWI']
data['FRIDT'] = data['Z1DT-LWI'] + data['Z2DT-LWI']
#Fix FRIMS/DT data as floats
data['FRIMS'] = data['FRIMS'].astype(float)
data['FRIDT'] = data['FRIDT'].astype(float)
                                     
# Choose solvents to plot below:
# solvChoose = data[
    # Aqueous
    # (data['Solvent'] == 'H2O')
    # Organics
    # | (data['Solvent'] == 'MeOH')
    # | (data['Solvent'] == 'EtOH')
    # | (data['Solvent'] == 'MeCN')
    # Deuterated Solvents
    # | (data['Solvent'] == 'D2O_10')
    # | (data['Solvent'] == 'D2O_20')
    # | (data['Solvent'] == 'D2O_40')
    # | (data['Solvent'] == 'D2O_40D')
    # | (data['Solvent'] == 'D2O_40G')
    # H3PO4 Template Additive
    # | (data['Solvent'] == 'H2OG')
    # | (data['Solvent'] == 'MeCNG')
    # | (data['Solvent'] == 'THFG')]

# Select from data containing ID FRIMS FRIDT Solvent and Condition, 
# and bounds of data (if required for SEABORN or MPL)
# friData = pd.DataFrame(solvChoose[['FRIMS','FRIDT','ID','Solvent','Condition']])
# xMin, xMax, yMin, yMax = friData['FRIMS'].min(), friData['FRIMS'].max(), friData['FRIDT'].min(), friData['FRIDT'].max()

    # Variables
print(f'Grouping plot by experiment')
nonRed = data[data['Condition']<4.5]
redCon = data[data['Condition']>3.5]
aqueous = data[data.Solvent.str.contains('H2O')]
organic = data[~data.Solvent.str.contains('2O')]
deuterated = data[data.Solvent.str.contains('D2O')]
# [data[data.Solvent.str.contains(i)] for i in solvents]

data.to_csv('Figure4-ProcessedSolventData(3-58).csv', index=False, encoding='UTF-8')


# Altair Bubble Scatter
print(f'Plotting {experiment} cluster mass vs. shape...')

import altair as alt

source = nonRed[nonRed.Solvent.str.endswith('H2O') | nonRed.Solvent.str.contains('D2O')]

fig4Chart = alt.Chart(source).mark_point().encode(
    alt.X('Z1MS-LWI', type='quantitative', title='Z1MS-LWI'),
    alt.Y('Z1DT-LWI', type='quantitative', aggregate='average', title='Z1DT-LWI'),
    color='Solvent:N',
    size='Condition:O',
    # shape='Solvent:N',
    # fill='Solvent:N',
    # color='Solvent:O', # solvent as an Ordinal dataset
    tooltip='ID',
)

fig4Chart.configure_axis(labelFontSize=16, titleFontSize=16)

# ).interactive()

# size based on condition, condition list in init files, resize text, legend

print(f'Saving {experiment} cluster mass vs. shape plot...')
fig4Chart.save(r'D:/Programming/SAMM/SAMMplot/Figure 4/Figure 4.html')

print('\n\aEnd o7\a')





















































### END OF WORKING STATE

    #   Default MPL/Seaborn Settings
# import matplotlib as mpl
# import seaborn as sns
# from cycler import cycler
# import colorcet as cc
# from matplotlib import cm
# from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# from matplotlib import pyplot as plt
# colors = cycler('color', malDiv)
# plt.rc('axes', edgecolor='black', axisbelow=False,
#        grid=False, prop_cycle=colors)
# font = {'family': 'arial',
#         # 'weight' : 'bold',
#         'size': 16}
# plt.rc('font', **font)  # pass in the font dict as kwargs
# plt.rc('figure', edgecolor='white')
# plt.rc('xtick', direction='out', color='k')
# plt.rc('ytick', direction='out', color='k')
# plt.rc('grid', c='0.5', ls='-', lw=0.1)
    # cMaps
# plasma = cm.get_cmap('plasma', 12)
# viridis = cm.get_cmap('viridis', 12)
# mSun = ['#955196', '#003f5c', '#444e86',  '#dd5182', '#ff6e54', '#ffa600']
# malDiv = '#ffa7ef #1e394a #7175ab #cc6200 #ff7087 '.split(' ')
# malPal = '#1e394a #414471 #893e78 #c23a53 #cc6200'.split(' ')
# bojackGrad = '#D04F6D #84486A #9C4670 #A75C87 #8C5D8B #7088B3 #71B2CA #8EE7F0 #B7F9F9 #A6F5F7'.split(' ')

    # Seaborn
# mpl-seaborn scatter plot settings
# sns.lmplot('FRIMS', 'FRIDT', data=friData, hue='Solvent', fit_reg=False)
# sns.scatterplot('FRIMS', 'FRIDT', data=friData, size='Solvent', hue='Condition')
# plt.legend(labels=friData['Solvent'])
# plt.title('Solvent and Condition Effects', size=16)
# plt.xlabel('FRIMS', size=18)
# plt.ylabel('FRIDT', size=18);
# plt.xlim((xMin, xMax))
# plt.ylim((yMin, yMax))

# Plotting tests
# Seaborn regression plot for charge vs solvent
# aq = sns.regplot(x='Z2MS-LWI', y='Z2DT-LWI', data=aqueous)  # High aquous variability - single solvent variable with regplot
# allSolvents = sns.lmplot(x='Z2MS-LWI', y='Z2DT-LWI', data=organic, hue='Solvent', palette='viridis')

# Z1 Top plot of water and deuterated solvents
# cmap = [bojackGrad[0], bojackGrad[2], bojackGrad[7], bojackGrad[9]]
# z1Plot = sns.lmplot(x='Z2MS-LWI', y='Z2DT-LWI',
#                     data=solvents, hue='Solvent', palette=cmap)
# Save figure
# figure4.savefig('D:\Programming\SAMM\SAMMplot\Figure 4\Figure4pair.png')

# sns.dogplot()