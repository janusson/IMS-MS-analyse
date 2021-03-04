import os
from plotnine import *
import pandas as pd
import numpy as np
import seaborn as sns
from math import log

# Load dataset

# Method 1 (Paste location):
print("Enter file name in Figure 1 Data Folder: ")
# dataPath = input()

# Method 2 (in CWD):
dataPath = r"D:\Programming\SAMM\SAMMplot\Experiments\EJ3-57-26-RA4-Sampling-2_Apex3DIons.csv"
apex3Ddf = pd.read_csv(dataPath)
print("Fetching data from: ")
print(dataPath.split("\\")[5].split("_")[0])

plotTitle = "DTMS Map for " + dataPath.split("\\")[5].split("_")[0]

# Define Variables
xScale, yScale = [0, 10], [150, 1500]
x, y, z, xyRatio = (
    list(apex3Ddf["m_z"]),
    list(apex3Ddf["mobility"] * 0.16),
    list(apex3Ddf["area"]),
    list(apex3Ddf["m_z"] / apex3Ddf["mobility"]),
)
xError, yError, zError = (
    list(apex3Ddf["errMzPPM"]),
    list(apex3Ddf["errArea"]),
    list(apex3Ddf["errMobility"]),
)
plotdf = pd.DataFrame(
    zip(x, y, z, xError, yError, zError),
    columns=["m/z", "DT", "Area", "m/z Error", "DT Error", "Area Error"],
)

logArea = np.log(z)
sqrtArea = np.sqrt(z)
expArea = np.exp(z)

####################################

#     # MPL Scatterplot
# from matplotlib import pyplot as plt

# mplScatter = plt.scatter(
#     x,
#     y,
#     s=logArea,
#     c=sqrtArea,
#     # edgecolor="Black",
#     cmap="plasma",
#     linewidth=1,
#     alpha=0.2,
# )
# plt.style.use("seaborn")

# funScatter = plt.scatter(x, y, s=z, c=logArea, edgecolor='black', cmap='plasma', linewidth=1, alpha=0.5)
# cBar = plt.colorbar()
# cBar.set_label("Signal Area")
# # plot labels
# plt.title("DTMS Plot for " + plotTitle)
# plt.xlabel("m/z")
# plt.ylabel("Drift Time (ms)")
# plt.tight_layout()
# # plt.xscale('log')
# # plt.yscale('log')
# plt.show()

# ####################################

#     # MPL Fig in fig Example
# import matplotlib.pyplot as plt
# import numpy as np

# x1 = np.random.randint(-5, 5, 50)
# x2 = np.random.randn(20)

# fig = plt.figure(figsize=(10,10))  # sets the window to 8 x 6 inches

# # left, bottom, width, height (range 0 to 1)
# # so think of width and height as a percentage of your window size
# big_ax = fig.add_axes([0.1, 0.1, 0.8, 0.8]) 
# small_ax = fig.add_axes([0.52, 0.15, 0.3, 0.3]) # left, bottom, width, height (range 0 to 1)

# big_ax.fill_between(np.arange(len(x1)), x1, color='green', alpha=0.3)
# small_ax.stem(x2)

# plt.setp(small_ax.get_yticklabels(), visible=False)
# plt.setp(small_ax.get_xticklabels(), visible=False)
# plt.show()

# ####################################

    # Plotnine points
cMapLog = np.log(z)
pointSize = np.sqrt(z)

p9point = (
    ggplot(plotdf)
    + geom_point(
        aes(x="m/z", y="DT", alpha=1/10, cmap=0, color=cMapLog, size=pointSize)
    )
    + labs(title=plotTitle, x="m/z", y="DT (ms)")
)
ggplot.save(p9point, plotTitle + ".png")

####################################

    # Plotnine Annotated Heatmap

# Periodic table example https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.geom_tile.html#annotated-heatmap

# A smoothed conditional mean
# https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.geom_smooth.html#smoothed-conditional-means

# Line segments (for weighting)
# https://plotnine.readthedocs.io/en/stable/generated/plotnine.geoms.geom_segment.html#ranges-of-similar-variables

####################################

#     # Seaborn
# sns.set(style="ticks")

# # # Show the results of a linear regression within each dataset
# sns.lmplot(x="m/z", y="DT", col="Area", hue="Area", data=plotdf,
#            col_wrap=2, ci=None, palette="muted", height=4,
#            scatter_kws={"s": 50, "alpha": 1})
