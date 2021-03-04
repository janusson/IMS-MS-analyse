# SAMMPlot.py
# Python 3.7.4 
# Eric Janusson 
# 270320
import os
import pandas as pd
import numpy as np
# %matplotlib inline

    ### Seaborn Style 
# import matplotlib.pyplot as plt
# import seaborn as sns

#Dist and joint plot
# sns.distplot(data['DT'], kde=True, bins=300)
# sns.jointplot(x='m/z', y='DT', data=data, kind='reg')

# sns.set(style='ticks')
# cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)
# ax = sns.scatterplot(x='m/z', 
#                 y='DT',
#                 data=dims,
#                 hue='Area',
#                 # hue_norm=(0, 100),
#                 size='Area',
#                 sizes=(20, 200),
#                 linewidth=0,
#                 edgecolor=None,
#                 alpha=0.60,
#                 palette=cmap
#                 )

# plt.xlabel('$\it{m/z}$')
# plt.ylabel('Drift Time (ms)')
# plt.show()

    #Extra parameters:
                # style=area,
                # hue=area, 
                # size=None, 
                # data=trimData, 
                # palette=None, 
                # hue_order=None, 
                # hue_norm=None, 
                # sizes=None, 
                # size_order=None, 
                # size_norm=None, 
                # markers=True, 
                # style_order=None, 
                # x_bins=None, 
                # y_bins=None, 
                # units=None, 
                # estimator=None, 
                # ci=95, 
                # n_boot=1000, 
                # alpha="auto", 
                # x_jitter=None, 
                # y_jitter=None, 
                # legend="brief", 
                # ax=None



# fig, ax = plt.subplots(figsize = (6, 6))
# sns.scatterplot(x= 'm/z', 
#             y = 'DT', 
#             data = data,
#             # hue = 'Area',
#             # size = 'Area Error',
#             # palette = {},
#             # xlim=(150, 1500),
#             # ylim=(1,10),
#             )
# plt.xlim(150, 1500)
# plt.ylim(2, 10)



    ## MPL Style
    
# Basic plotting   
# fig = plt.figure() #Create a canvas
# axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# axes.plot(specData['m/z'], specData['Counts'])
# axes.set_xlabel('$\it{m/z}$', size=16)
# axes.set_ylabel('Intensity', size=16)
# axes.set_title("Title")
#plt.show()



import matplotlib.pyplot as plt


import matplotlib as mpl
from cycler import cycler
from matplotlib import pyplot as plt
# %matplotlib inline

colors = cycler('color', malDiv)
plt.rc('axes', facecolor='w', edgecolor='k',
       axisbelow=False, grid=False, prop_cycle=colors)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#003f5c')
plt.rc('lines', linewidth=2)

# Subplots
figure1 = plt.figure()
layer1 = figure1.add_axes([0.1, 0.1, 0.8, 0.8])
layer2 = figure1.add_axes([0.55, 0.65, 0.3, 0.2])
layer1.set_title('Mass Spectrum')
layer2.set_title('Mobilogram')
layer1.plot(msMass, msCounts)
layer2.plot(dtTime, dtIntensity)

#SUBPLOTS IS LIKE AN AXES MANAGER
fig, axes = plt.subplots(1, 2, sharey=False, figsize=(8, 4.5), dpi=600)
axes[0].plot(msMass, msCounts)
axes[1].plot(dtTime, dtIntensity)

axes[0].set_title('Mass Spectrum')
axes[0].set_xlabel('$\it{m/z}$')
axes[0].set_ylabel('Intensity')


axes[1].set_title('Mobilogram')
axes[1].set_xlabel('DT (ms)')
axes[1].set_ylabel('')

# fig.legend()
plt.tight_layout()
plt.show()

# fig.savefig("filename.png", dpi=200)




## Standard plot: 
# ax.set_title('Drift Time of Mo Ions')
# ax.set_xlabel('Drift Time (ms)')
# ax.set_ylabel('Intensity')
#     dt data
# ax[0].plot(specData['Drift Time'].index, 
#         specData['Intensity'],
#         # marker='v',
#         linestyle = '--',
#         color = mSun[1]
#         )
# ax[0].set_title('Drift Time of Mo Ions')
# ax[0].set_xlabel('Drift Time (ms)')
# ax[0].set_ylabel('Intensity')
#     # ms data
# ax[1].plot(specData['m/z'], 
#         specData['Counts'],
#         color = mSun[4]
#         )
# ax[1].set_title('Mass Spectrum Mo Ions')
# ax[1].set_xlabel('m/z')
# ax[1].set_ylabel('Counts')
# plt.show()

# fig2, ax2 = plt.supplots()
# ax2.plot(specData['m/z'], 
#         specData['Counts'],
#         color = mSun[4]
#         )





    ### ggplot Style
# import plotnine
# from plotnine import ggplot, geom_point, aes, theme_bw
# ax = ggplot(dims) + geom_point(aes(x = "m/z", y = "DT", color = r"log(Area)", size = "Area")) + theme_bw()
# print(ax)

### Plotly
# import plotly.graph_objects as go
# trace1 = go.Scatter(x=mz, y=dt, mode='markers', marker=dict(size=dims['log(Area)'],
#                     color=dims['log(Area)']),
#                     # colorscale = 'Viridis',
#                     # showscale=True
#                     )

# print(trace1)

# trace2 = go.Histogram2dcontour(x=mz, y=dt, name='density', ncontours=20,
#     colorscale='Hot', reversescale=True, showscale=False
#     )

# trace3 = go.Histogram(x=mz, name=r'm/z Density',
#     marker=dict(color='rgb(102,0,0)'),
#     yaxis='y2'
#     )

# trace4 = go.Histogram(
#     y=dt, name='DT Density', marker=dict(color='rgb(102,0,0)'),
#     xaxis='x2'
#     )
