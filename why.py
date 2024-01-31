from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Function to fit ARIMA model and forecast
def forecast_arima(series, steps=5):
    model = ARIMA(series, order=(1,1,1))  # Adjust ARIMA parameters as needed
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    return forecast

# Plotting function with color parameter
def plot_series_with_forecast(df, column, forecast, forecast_index, color):
    plt.plot(df.index, df[column], label=column)
    plt.plot(forecast_index, forecast, linestyle='--', color=color, label=f'{column} Forecast')

# Read your data
df = pd.read_csv('Energy_Sales.csv')
# Assuming 'Year' is already converted to a suitable format and set as index

# Forecasting and plotting
plt.figure(figsize=(14, 10))

# List of columns to forecast
columns_to_forecast = ['MEA', 'PEA', 'EDL', 'Malaysia', 'Cambodia', 'Direct customers', 'Others', 'Total']

# Define a list of colors for the forecasts
colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray']

last_year = df.index[-1]
forecast_index = pd.RangeIndex(start=last_year+1, stop=last_year+6, step=1)

for i, column in enumerate(columns_to_forecast):
    forecast = forecast_arima(df[column])
    plot_series_with_forecast(df, column, forecast, forecast_index, colors[i])

plt.title('Energy Sales Forecast by Source and Total')
plt.xlabel('Year')
plt.ylabel('Energy Sales (Million kWh)')
plt.legend()
plt.xticks(np.append(df.index, forecast_index), rotation=90)  # Ensure all x-ticks are shown
plt.tight_layout()
plt.show()
