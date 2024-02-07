import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Read the data
df = pd.read_csv('Electrical/Resevior_Operation.csv')

# Convert 'Year' to datetime and set as index
df['Year'] = df['Year'].astype(int)
df.set_index('Year', inplace=True)

# Convert 'Total' and other components to numeric, coercing errors to NaN, then drop rows with NaNs
components = ['Total water inflow']
for component in components:
    df[component] = pd.to_numeric(df[component], errors='coerce')
df.dropna(subset=components, inplace=True)

# Ensure the DataFrame is not empty
if df.empty:
    raise ValueError("The DataFrame is empty after removing NaN values.")


#TODO: Generate a new index for the forecasted period
Year = int(input("Enter the year you want to forecasting:"))
last_year = df.index[-1]
forecast_index = pd.RangeIndex(start=last_year+1, stop=last_year+Year+1, step=1)

# Define colors for each category and forecast lines
colors = ['black']
forecast_colors = ['lightblue']

# Plotting the actual and forecasted values for 'Total' and other components
plt.figure(figsize=(14, 8))
#TODO: plt.style.use('ggplot')

# Loop through each category to plot, fit ARIMA model, forecast, and plot forecast
for i, column in enumerate(components):
    # Plot actual data
    plt.plot(df.index, df[column], label=f'{column} Actual', color=colors[i], linewidth=2 if column == 'Total water inflow' else 1)
    
    if column != 'Total water inflow':  # Forecasting for categories other than 'Total'
        # Fit ARIMA model
        model = ARIMA(df[column].dropna(), order=(1,1,1))  # Ensure to drop NaNs in each category
        model_fit = model.fit()
        # Forecast
        forecast = model_fit.forecast(steps=Year)
        # Plot forecasted data
        plt.plot(forecast_index, forecast, linestyle='--', label=f'{column} Forecast', color=forecast_colors[i])

# Special handling for 'Total' forecast to ensure it's plotted last
model_total = ARIMA(df['Total water inflow'], order=(1,1,10))
model_fit_total = model_total.fit()
forecast_total = model_fit_total.forecast(steps=Year)  # Forecasting the next 5 periods
plt.plot(forecast_index, forecast_total, 'r--', label='Total Forecasted', color='grey')

plt.title('Demand Forecasting Total Water in Flow by Time Series Method')
plt.xlabel('Year')
plt.ylabel('Water Inflow (Million Cubic Meter)')
plt.legend()
plt.xticks(np.append(df.index.values, forecast_index), rotation=90)  # Ensure all x-ticks are shown
plt.tight_layout()
plt.show()