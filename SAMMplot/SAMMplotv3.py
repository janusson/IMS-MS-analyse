#Two dimensional plotting of Apex3D data

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import plotnine
from plotnine import ggplot, geom_point, aes, theme_bw

#   Import Apex3D data
rawData = pd.read_csv(r'D:\Programming\SAMM\SAMMplot\Test Data\EJ3-57-122-BA7-Sampling-2_Apex3DIons.csv')

# xyzData = rawData[['3D_m_z', '3D_Intensity', '3D_TC']].rename(columns={'3D_m_z': 'm/z', '3D_Intensity': 'Area', '3D_TC': 'Drift Time'}) #note: applicable to APEX outs from Driftscope. Non DS exports use different XYZ headers
xyzData = rawData[['m_z', 'inten', 'area', 'mobility']].rename(columns={'m_z': 'm/z', 'inten': 'Intensity', 'area': 'Area', 'mobility': 'Drift Time'})
#   Import 2D Data
dtData = pd.read_csv(r'S:\S-SAMM Programs\SAMM\SAMMplot\SAMMPlotData\DT_EJ3-52-A2-9-BA7-Sampling.csv', skiprows=[0, 1])
dtData.columns = ["Drift Time", "Intensity"]

mzData = pd.read_csv(r'S:\S-SAMM Programs\SAMM\SAMMplot\SAMMPlotData\MZ_EJ3-52-A2-9-BA7-Sampling.csv', skiprows=[0, 1])
mzData.columns = ["m/z", "Intensity"]

#   Process: Sort all data by X, add Log scale
xyzData.sort_values(["m/z"], inplace=True)
dtData.sort_values(["Drift Time"], inplace=True)
mzData.sort_values(["m/z"], inplace=True)
xyzData["Log Area"] = np.log(xyzData["Area"])

xyzData.head()
mzData.head()
dtData.head()

#   Quickcheck plots
plt.plot(dtData["Drift Time"], dtData["Intensity"])
plt.plot(mzData["m/z"], mzData["Intensity"])
plt.hist2d(xyzData["m/z"], xyzData["Drift Time"], bins = 100)

#   3D ggplot
p = ggplot(xyzData) + geom_point(aes(x = "m/z", y = "Drift Time", color = "Area", size = "Area")) + theme_bw()
p2 = ggplot(xyzData) + geom_point(aes(x = "m/z", y = "Drift Time", color = "Log Area", size = "Area")) + theme_bw()
print(p)
print(p2)

ggplot.save(p2, "BubblePlotTest.png")



# from IPython import get_ipython
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# erics_data = pd.read_csv("BA7-9-output.csv")
# erics_data.head()
# erics_data.sort_values(["intensity"], inplace = True)
# import plotnine
# from plotnine import ggplot, geom_point, aes, theme_bw
# p = ggplot(erics_data) + geom_point(aes(x = "mz", y = "mobility", color = "intensity", size = "area")) + theme_bw()
# p
# erics_data["log intensity"] = np.log(erics_data["intensity"])
# p2 = ggplot(erics_data) + geom_point(aes(x = "mz", y = "mobility", color = "log intensity", size = "area")) + theme_bw()
# p2
# ggplot.save(p, "name.jpeg")