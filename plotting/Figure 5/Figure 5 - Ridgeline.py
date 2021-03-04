# Figure5.py
# Plot Z2 species in H2O vs. D2O reactions
# Python 3.7.4
# https://altair-viz.github.io/gallery/ridgeline_plot.html
# Eric Janusson
# 150320
import os
import pandas as pd
import numpy as np

# data import (opt, user input)
# def importSAMM2D(userInput=None):
#     # Load 2D CSV files for FR, Z1, Z2
#     basePath = r'D:\2-SAMM\SAMM - Data Workup Folder\Data Workup (300919)\Experimental Data\3-57-SAMM2\2DExtract(3-57-2)'
#     frMS = str(basePath + r'\Full Range\MS\EJ3-' + userInput + r'-Sampling-2\MZ_EJ3-' +
#                userInput + r'-Sampling-2_fn-1_#FullRange-POMSolv-Rangefile.txt_raw.csv')
#     frDT = str(basePath + r'\Full Range\DT\EJ3-' + userInput + r'-Sampling-2\DT_EJ3-' +
#                userInput + r'-Sampling-2_fn-1_#FullRange-POMSolv-Rangefile.txt_raw.csv')
#     z1MS = str(basePath + r'\Z1\MS\EJ3-' + userInput + r'-Sampling-2\MZ_EJ3-' +
#                userInput + r'-Sampling-2_fn-1_#POMSolv-Z1-RuleFile.rul_raw.csv')
#     z1DT = str(basePath + r'\Z1\DT\EJ3-' + userInput + r'-Sampling-2\DT_EJ3-' +
#                userInput + r'-Sampling-2_fn-1_#POMSolv-Z1-RuleFile.rul_raw.csv')
#     z2MS = str(basePath + r'\Z2\MS\EJ3-' + userInput + r'-Sampling-2\MZ_EJ3-' +
#                userInput + r'-Sampling-2_fn-1_#POMSolv-Z2-RuleFile.rul_raw.csv')
#     z2DT = str(basePath + r'\Z2\DT\EJ3-' + userInput + r'-Sampling-2\DT_EJ3-' +
#                userInput + r'-Sampling-2_fn-1_#POMSolv-Z2-RuleFile.rul_raw.csv')
#     paths = [frMS, frDT, z1MS, z1DT, z2MS, z2DT]
#
#     # separate data by charge state
#     frScatter = ([pd.read_csv(i, skiprows=1)
#                   for i in paths if os.path.lexists(i) and i[104:106] == r'Fu'])
#     frScatter = pd.concat([frScatter[0], frScatter[1]], axis=1)
#     frScatter.columns = ['m/z', 'Counts', 'Drift Time', 'Intensity']
#
#     z1Scatter = ([pd.read_csv(i, skiprows=1)
#                   for i in paths if os.path.lexists(i) and i[104:106] == r'Z1'])
#     z1Scatter = pd.concat([z1Scatter[0], z1Scatter[1]], axis=1)
#     z1Scatter.columns = ['m/z', 'Counts', 'Drift Time', 'Intensity']
#
#     z2Scatter = ([pd.read_csv(i, skiprows=1)
#                   for i in paths if os.path.lexists(i) and i[104:106] == r'Z2'])
#     z2Scatter = pd.concat([z2Scatter[0], z2Scatter[1]], axis=1)
#     z2Scatter.columns = ['m/z', 'Counts', 'Drift Time', 'Intensity']
#
#     return frScatter, z1Scatter, z2Scatter, userInput
path_name
if os.path.lexists(path_name) and str.pathname[104:106] == r'Fu':
    pd.read_csv(pathname)

pd.read_csv?

pd.read_csv(if os.path.lexists(pathname) and str.pathname[104:106] == r'Fu'])
([pd.read_csv(i, skiprows=1)
              for i in paths if os.path.lexists(i) and i[104:106] == r'Fu'])



# fuunction to pass in some data (full range, or by charge) and plot
def ridgelinePlot(scatterData):
    import altair as alt
    source = scatterData
    mz = source['m/z']
    cnts = source['Counts']
    dt = source['Drift Time']
    intensity = source['Intensity']
    step = 20
    overlap = 1
###
    alt.Chart(source, height=20).transform_timeunit(
        Month='month(date)'
    ).transform_joinaggregate(
        mean_temp='mean(temp_max)', groupby=['Month']
    ).transform_bin(
        ['bin_max', 'bin_min'], 'temp_max'
    ).transform_aggregate(
        value='count()', groupby=['Month', 'mean_temp', 'bin_min', 'bin_max']
    ).transform_impute(
        impute='value', groupby=['Month', 'mean_temp'], key='bin_min', value=0
    ).mark_area(
        interpolate='monotone',
        fillOpacity=0.8,
        stroke='lightgray',
        strokeWidth=0.5
    ).encode(
        alt.X('bin_min:Q', bin='binned', title='Maximum Daily Temperature (C)'),
        alt.Y(
            'value:Q',
            scale=alt.Scale(range=[step, -step * overlap]),
            axis=None
        ),
        alt.Fill(
            'mean_temp:Q',
            legend=None,
            scale=alt.Scale(domain=[30, 5], scheme='redyellowblue')
        )
    ).facet(
        row=alt.Row(
            'Month:T',
            title=None,
            header=alt.Header(labelAngle=0, labelAlign='right', format='%B')
        )
    ).properties(
        title='Seattle Weather',
        bounds='flush'
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    ).configure_title(
        anchor='end'
    )

    print(f'Saving {experiment} plot...')
    # fig5Chart.save(r'D:/Programming/SAMM/SAMMplot/Figure 5/Figure 5.html')

# Create Dataframes
frScatter, z1Scatter, z2Scatter, fileID = importSAMM2D('57-158-BC4')
# frScat2, z1Scat2, z2Scat2, fileID2 = importSAMM2D('57-26-RA4')

ridgelinePlot(frScatter)
