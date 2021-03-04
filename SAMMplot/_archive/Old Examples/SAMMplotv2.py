import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns

df = pd.read_csv(r'D:\Programming\SAMM\SAMMplot\APEX3D-ExampleData\EJ3-57-26-RA4-Sampling-2_Apex3DIons.csv')
#df2 = df[['3D_m_z', '3D_Intensity', '3D_TC']] #Old Apex form (DS 2.2)
df2 = df[['m_z', 'area', 'mobility']]
df3 = df2.rename(columns={'m_z': 'm/z', 'area': 'Area', 'mobility': 'Drift Time'})
plt.hist2d(df3['m/z'], df3['Drift Time'], bins = 250)





# df4 = pd.read_csv(r'S:\Programming\SAMM\SAMMplot\ExportedData\EJ3-52-A2-9-BA7\DT_EJ3-52-A2-9-BA7-Sampling.csv', skiprows=[0, 1])
# df4.columns = ["Drift Time", "Intensity"]

# df5 = pd.read_csv(r'S:\Programming\SAMM\SAMMplot\ExportedData\EJ3-52-A2-9-BA7\MZ_EJ3-52-A2-9-BA7-Sampling.csv', skiprows=[0, 1])
# df5.columns = ["m/z", "Intensity"]
# plt.plot(df4["Drift Time"], df4["Intensity"])
# plt.plot(df5["m/z"], df5["Intensity"])


# plt.hist2d(df3["m/z"], df3["Drift Time"], bins = 100)
plt.hist2d(df3["m/z"], df3["Drift Time"], bins = 100)
