#https://colab.research.google.com/drive/11f-RzjXUiIz-T11AlEylMCsVNIb4GuDC#scrollTo=-lgqZtNW7qPR


#Visualization: Linked Scatter-Plot and Histogram in Altair

# load an example dataset
from vega_datasets import data
cars = data.cars()

import altair as alt

interval = alt.selection_interval()

points = alt.Chart(cars).mark_point().encode(
  x='Horsepower',
  y='Miles_per_Gallon',
  color=alt.condition(interval, 'Origin', alt.value('lightgray'))
).properties(
  selection=interval
)

histogram = alt.Chart(cars).mark_bar().encode(
  x='count()',
  y='Origin',
  color='Origin'
).transform_filter(interval)

points & histogram




#Visualization: Bar Plot in Altair

# load an example dataset
from vega_datasets import data
cars = data.cars()

# plot the dataset, referencing dataframe column names
import altair as alt
alt.Chart(cars).mark_bar().encode(
  x='mean(Miles_per_Gallon)',
  y='Origin',
  color='Origin'
)


#Visualization: Interactive Scatter Plot in Altair

# load an example dataset
from vega_datasets import data
cars = data.cars()

# plot the dataset, referencing dataframe column names
import altair as alt
alt.Chart(cars).mark_point().encode(
  x='Horsepower',
  y='Miles_per_Gallon',
  color='Origin'
).interactive()


#Visualization: Time Series Line Plot in Altair

from vega_datasets import data
stocks = data.stocks()

import altair as alt
alt.Chart(stocks).mark_line().encode(
  x='date:T',
  y='price',
  color='symbol'
).interactive(bind_y=False)

#Visualization: Scatter Plot with Rolling Mean in Altair

# load an example dataset
cars = data.cars()


points = alt.Chart(cars).mark_point().encode(
    x='Year:T',
    y='Miles_per_Gallon',
    color='Origin'
).properties(
    width=800
)

lines = alt.Chart(cars).mark_line().encode(
    x='Year:T',
    y='mean(Miles_per_Gallon)',
    color='Origin'
).properties(
    width=800
).interactive(bind_y=False)

points + lines


#Visualization: Interactive Brushing in Altair
# load an example dataset
cars = data.cars()


interval = alt.selection_interval()

alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color=alt.condition(interval, 'Origin', alt.value('lightgray'))
).properties(
    selection=interval
)

# Visualization: Histogram in Altair

# load an example dataset
cars = data.cars()

# plot the dataset, referencing dataframe column names
alt.Chart(cars).mark_bar().encode(
    x=alt.X('Miles_per_Gallon', bin=True),
    y='count()',
)

#Visualization: Stacked Histogram in Altair

# load an example dataset
from vega_datasets import data
cars = data.cars()

# plot the dataset, referencing dataframe column names
import altair as alt
alt.Chart(cars).mark_bar().encode(
  x=alt.X('Miles_per_Gallon', bin=True),
  y='count()',
  color='Origin'
)