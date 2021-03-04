# Figure6.py
# Plot Z1/Z2 cluster intermediates exhibiting nonlinear morphological growth
# Python 3.7.4
# Eric Janusson
# 150320
import pandas as pd
import matplotlib as mpl
from matplotlib import rcParams
from matplotlib import pyplot as plt

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

    # MPL Settings
    colors = mpl.cycler('color', mSun)  # colors = cycler('color', mSun)
    plt.rc('axes', edgecolor='gray', axisbelow=False,
           grid=False, prop_cycle=colors)
    plt.rc('grid', c='0.5', ls='-', lw=0.1)
    plt.rc('xtick', direction='out', color='gray')
    plt.rc('ytick', direction='out', color='gray')
    plt.rc('patch', edgecolor='#003f5c')
    plt.rc('lines', linewidth=0.18, aa=True)
    font = {'family': 'arial',
            'weight': 'bold',
            'size': 16}
    plt.rc('font', **font)  # pass in the font dict as kwargs

    return(mSun, malDiv, malPal, bojackGrad, colors)

mSun, malDiv, malPal, bojackGrad, colors = setColourScheme()

df = pd.read_csv(
    r'D:\Programming\SAMM\SAMMplot\Figure 6\Data\Figure 6 Data(EJ3-60-90-BA1).csv')
print(df.head())
print('\n Plotting...')

plt.scatter(df['mz'], df['DT'])

# Replot in Altair:
### Add regression lines, local trends/deviations to plot



## Regression analysis
# https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f

# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn import metrics
# %matplotlib inline

# sklearnData = data.drop(columns=['m/z Error', 'DT Error', 'Area Error']).sort_values(by='Area').reset_index()

# sns.distplot(sklearnData['Area'])
# sklearnData.describe()

# x = sklearnData['m/z'].values.reshape(-1, 1)
# y = sklearnData['DT'].values.reshape(-1, 1)
# xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=0)
# regresso = LinearRegression()
# regresso.fit(xTrain, yTrain) #Training the algorithm

# yPred = regresso.predict(xTest)
# df = pd.DataFrame({'Actual': yTest.flatten(), 'Predicted':yPred.flatten()})

# # Residuals
# df1 = df.head(25)
# df1.plot(kind='bar', figsize=(6,4))
# plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
# plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

# plt.scatter(xTest, yTest, color=mSun[0], alpha=0.05, edgecolor=None)
# plt.plot(xTest, yPred, color='red', linewidth=1)
# plt.show()

# print(regresso.intercept_)
# print(regresso.coef_)
# print('Root-Mean-Squared Error: ', np.sqrt(metrics.mean_squared_error(xTest, yPred)))
