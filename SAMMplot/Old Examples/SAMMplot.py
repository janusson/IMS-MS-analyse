import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#   Specify filepath, set up dataframe
dataImport = pd.read_csv(r'D:\Programming\SAMM\SAMMplot\EJ3-41-RB1_Apex3DIons.csv')
#https://pythonprogramming.net/pandas-column-manipulation-spreadsheet-data/?completed=/pandas-saving-reading-csv-file/
dtmsData = dataImport[['m_z', 'area', 'mobility']].rename(columns={'m_z': 'm/z', 'area': 'Area', 'mobility': 'Drift Time'}).sort_values("m/z")
errorData = dataImport[['m_z','errMzPPM', 'area', 'errArea', 'mobility', 'errMobility']].rename(columns={'m_z': 'm/z', 'area': 'Area', 'mobility': 'Drift Time', 'errMzPPM': "m/z Error (ppm)", "errArea":"Area Error", "errMobility":"Drift Time Error"})
sortedData = dtmsData.sort_values("m/z")


def getStats():
    stats = round(sortedData.describe(), 2) #descriptive states to 2 decimal places
    print(stats)
getStats()

def linePlot(dataset):
    plt.figure(figsize=(16,9))
    plt.title("Peak Area")
    sns.lineplot(data = dataset["Area"], label = "Peak Area")
linePlot(sortedData)

def jointPlot():
    sns.jointplot(sortedData["m/z"], sortedData["Drift Time"], kind = "kde", color="orangered", data=sortedData)
    sns.jointplot(sortedData["m/z"], sortedData["Drift Time"], kind = "resid", color="darkslateblue", data=sortedData)
    sns.jointplot(sortedData["m/z"], sortedData["Drift Time"], kind = "scatter", color="darkviolet", data=sortedData)
jointPlot()

def volumeScatter():
    plt.scatter(sortedData["m/z"], sortedData["Drift Time"], s=sortedData["Area"]*25, 
                alpha=0.4, edgecolors='w')
    plt.xlabel("m/z")
    plt.ylabel("Drift Time")
    plt.title("Mobility Map",y=1.05)
volumeScatter()

def mplSurfPlot():
    from mpl_toolkits.mplot3d import Axes3D
    df = sortedData.unstack().reset_index()
    df.columns = ["X", "Y", "Z"]
    df['X'] = pd.Categorical(df['X'])
    df['X'] = df['X'].cat.codes

    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    ax.plot_trisurf(df["Y"], df["X"], df["Z"], cmap=plt.cm.viridis, linewidth=0.2)
    plt.show()
mplSurfPlot()





#Example of matplotlib's 3D plotting feature:
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
fig = plt.figure()
ax = fig.gca(projection='3d')



# Make data.
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()




#Only show data with m/z over 500
# high_mz = df3[(df3['m/z'] > 500)]
#https://pythonprogramming.net/pandas-column-operations-calculations/?completed=/pandas-column-manipulation-spreadsheet-data/

# #Plot axis histograms
# sortedData.hist(bins=15, color='steelblue', edgecolor='black', linewidth=1.0, xlabelsize=8, ylabelsize=8, grid=False)
# plt.tight_layout(rect=(0,0,1.2,1.2))



#Formatting suggestions:
# fig, ax = plt.subplots(2, 2, figsize=(5, 5))

# ax[0][0].scatter(data['IP'], data['EA'], c=data['S0->S1'])
# ax[0][1].scatter(data['IP'], data['EA'], c=data['S0->S1'])
# ax[1][0].scatter(data['IP'], data['EA'], c=data['S0->S1'])
# ax[1][1].scatter(data['IP'], data['EA'], c=data['S0->S1'])

#Links:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
# https://seaborn.pydata.org/tutorial/relational.html#relating-variables-with-scatter-plots
# https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57
# https://github.com/dipanjanS/practical-machine-learning-with-python/blob/master/bonus%20content/effective%20data%20visualization/Bonus%20-%20Effective%20Multi-dimensional%20Data%20Visualization.ipynb