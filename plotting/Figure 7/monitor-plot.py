# monitor-plot.py
import os
import numpy as np
import pandas as pd
import altair as alt

# data_dir = input('enter SAMMmonitor output .csv path: ')
data_dir = r'D:\2-SAMM\Programs\SAMM\SAMMmonitor\out\apex-out.csv'
dataset = pd.read_csv(data_dir, header=0, names = [
        'Exp. ID', 'Inj.#', 'Exp.#', 'Ion', 'Base Peak Area'])

dataset.head()
dataset.info()

# filter by experiment id
dataset.groupby(['BB4'])

# dataset['Ion'][0]


# Exp. ID,Inj.#,Exp.#,Ion,Base Peak Area
# importing samm monitor data with settings 1 amu and  5% dt tolerance

# filter_data = ['']
# data[0]



def time_series_plot(data):
    source = data # columnar data

    chart = alt.Chart(source).mark_point().encode(
        alt.X('Injection Number', 
        type='N', # ordinal?
        title='$\it{inj. number}$'),

        alt.Y('Base Peak Area', 
        type='quantitative', 
        aggregate='average', 
        title='Drift Time (ms)'),

        color='Area:Q',
        size='Area:Q',
        # fill='Solvent:N',
        # color='inj#:O', # ordinal
        # tooltip='ID',
    )
    # data, 'm/z', 'DT', ds.mean('Area')
    chart.save(cwd+r'\\monitor-plot.jpg')
    # file:///D:/Programming/SAMM/SAMMplot/Figure%204/Figure%204.html
    return print(f'plot saved to {cwd}.')
