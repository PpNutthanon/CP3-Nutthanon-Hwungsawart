import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

# Ensure that the plots are displayed inline in Jupyter Notebooks

# Read the data
df = pd.read_csv('Energy_Sales.csv')

# Convert 'Year' to datetime and set as index
df['Year'] = df['Year'].astype(int)
df.set_index('Year', inplace=True)

# Convert 'Total' to numeric, coercing errors to NaN, then drop rows with NaNs
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
df.dropna(subset=['Total'], inplace=True)

# Check the DataFrame to ensure it's not empty and view the first few rows
if df.empty:
    raise ValueError("The DataFrame is empty after removing NaN values.")
else:
    print(df.head())

# Decompose the time series
result = seasonal_decompose(df['Total'], model='additive', period=1)

# Plotting the components of seasonal decomposition
plt.figure(figsize=(12, 8))

# Plot observed
plt.subplot(411)
plt.plot(result.observed, label='Observed')
plt.title('Observed')
plt.legend(loc='upper left')

# Plot trend
plt.subplot(412)
plt.plot(result.trend, label='Trend')
plt.title('Trend')
plt.legend(loc='upper left')

# Plot seasonal
plt.subplot(413)
plt.plot(result.seasonal, label='Seasonal')
plt.title('Seasonal')
plt.legend(loc='upper left')

# Plot residual
plt.subplot(414)
plt.plot(result.resid, label='Residual')
plt.title('Residual')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()

# Perform Augmented Dickey-Fuller test on the original data
adf_test = adfuller(df['Total'])
print('ADF Statistic: %f' % adf_test[0])
print('p-value: %f' % adf_test[1])

# Plot ACF and PACF on the original data
plot_acf(df['Total'], lags=10)
plt.show()

plot_pacf(df['Total'], lags=10)
plt.show()

# Assuming the data needs to be differenced once based on ADF test
# Fit the ARIMA(1,1,1) model on the original data
model = ARIMA(df['Total'], order=(1,1,1))
model_fit = model.fit()


# Forecast
forecast = model_fit.forecast(steps=5)  # Forecasting the next 5 periods

# Generate a new index for the forecasted period
last_year = df.index[-1]
forecast_index = pd.RangeIndex(start=last_year+1, stop=last_year+6, step=1)

# Plot the actual data
plt.figure(figsize=(12, 8))
plt.plot(df.index, df['Total'], label='Actual Energy Sales')

# Plot the forecasted data
plt.plot(forecast_index, forecast, 'r--', label='Forecasted Energy Sales')
plt.title('Energy Sales Forecast')
plt.xlabel('Year')
plt.ylabel('Total Energy Sales (Million kWh)')
plt.legend()

# Prepare the text for forecasted values
forecast_text = '\n'.join([f'{year}: {value:.2f} Million kWh' for year, value in zip(forecast_index, forecast)])

# Position for the annotation box
text_x = plt.xlim()[1] * 0.6  # Adjust these values as needed to fit your plot
text_y = plt.ylim()[1] * 0.9  # Adjust these values as needed to fit your plot

# Annotate forecasted values inside the plot
plt.text(text_x, text_y, forecast_text, fontsize=9, bbox=dict(facecolor='white', alpha=0.5))

plt.xticks(np.append(df.index, forecast_index), rotation=90)  # Ensure all x-ticks are shown
plt.tight_layout()
plt.show()

#TODO:
# Plot the individual components
plt.figure(figsize=(14, 8))

# List of columns to plot
columns_to_plot = ['MEA', 'PEA', 'EDL', 'Malaysia', 'Cambodia', 'Direct customers', 'Others']

for column in columns_to_plot:
    plt.plot(df.index, df[column], label=column)

# Plot the Total column
plt.plot(df.index, df['Total'], label='Total', linewidth=2, linestyle='--', color='black')

plt.title('Energy Sales by Source and Total')
plt.xlabel('Year')
plt.ylabel('Energy Sales (Million kWh)')
plt.legend()

# Adjust the plot as needed
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
