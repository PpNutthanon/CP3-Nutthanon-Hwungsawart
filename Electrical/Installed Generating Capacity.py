import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Read the data
df = pd.read_csv('Electrical/Installed_Generating.csv')

# Convert 'Year' to datetime and set as index
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df.dropna(subset=['Year'], inplace=True)  # Drop rows where 'Year' could not be converted
df['Year'] = df['Year'].astype(int)
df.set_index('Year', inplace=True)

# Convert 'Total' and other components to numeric, coercing errors to NaN, then drop rows with NaNs
components = ['Total', 'Thermal', 'Hydropower', 'Gas Turbine', 'Combined Cycle', 'Diesel', 'Renewable Energy', 'Purchase']
for component in components:
    df[component] = pd.to_numeric(df[component], errors='coerce')
df.dropna(subset=components, inplace=True)

# Ensure the DataFrame is not empty
if df.empty:
    raise ValueError("The DataFrame is empty after removing NaN values.")

# Generate a new index for the forecasted period based on user input
forecast_years = int(input("Enter the number of years you want to forecast:"))
last_year = df.index[-1]
forecast_index = pd.RangeIndex(start=last_year + 1, stop=last_year + forecast_years + 1, step=1)

# Define colors for each category and forecast lines
colors = ['black', 'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange']
forecast_colors = ['grey', 'lightblue', 'lightgreen', 'salmon', 'lightcyan', 'pink', 'lightyellow', 'peachpuff']

# Plotting the actual and forecasted values for 'Total' and other components
plt.figure(figsize=(14, 8))

# Loop through each category to plot, fit ARIMA model, forecast, and plot forecast
for i, component in enumerate(components):
    # Plot actual data
    plt.plot(df.index, df[component], label=f'{component} Actual', color=colors[i], linewidth=2 if component == 'Total' else 1)
    
    # Forecasting for all categories
    model = ARIMA(df[component].dropna(), order=(1,1,10))  # Ensure to drop NaNs
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_years)
    plt.plot(forecast_index, forecast, linestyle='--', label=f'{component} Forecast', color=forecast_colors[i])

# Set x-axis limits explicitly to include all years and forecasted period
plt.xlim(df.index.min(), forecast_index.max())

# Adding more ticks for clarity if needed
plt.xticks(np.linspace(df.index.min(), forecast_index.max(), num=20, dtype=int), rotation=45)

plt.title('Demand Forecasting Installed Generating Capacity by Time Series Method')
plt.xlabel('Year')
plt.ylabel('Installed Generating Capacity (MW)')
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
