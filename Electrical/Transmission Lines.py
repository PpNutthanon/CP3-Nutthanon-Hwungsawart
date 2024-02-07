import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

#* Import CSV Files 
df = pd.read_csv('Electrical/Transmission_Lines.csv')

# Convert 'Year' to datetime and set as index
df['Year'] = pd.to_numeric(df['Year'], errors='coerce') #TODO: Change Year column to int or float types and other types will be Nan
df.dropna(subset=['Year'], inplace=True)  #TODO: Remove Nan Values in Year Column
df['Year'] = df['Year'].astype(int) #TODO: Convert to Integer
df.set_index('Year', inplace=True) #TODO: Set Year to Index so we can specific row in year for instance df.loc[2565]

#* Convert every columns, coercing errors to NaN, then drop rows with NaNs (Do the same as above but in different columnns)
components = ['Total', '69 kV', '115 kV', '132 kV', '230 kV', '300 kV', '500 kV']
for component in components:
    df[component] = pd.to_numeric(df[component], errors='coerce') 
df.dropna(subset=components, inplace=True) #TODO: No need to convert in the integer because some of data is in the float types

#* Ensure the DataFrame is not empty
if df.empty:
    raise ValueError("The DataFrame is empty after removing NaN values.") #TODO: Show this types of error if dataframe is empty (no rows and no columns)

#* Forecasted period based on user input
forecast_years = int(input("Enter the number of years you want to forecast:"))
last_year = df.index[-1]
forecast_index = pd.RangeIndex(start=last_year + 1, stop=last_year + forecast_years + 1, step=1)

#* Define colors for each category and forecast lines
colors = ['black', 'blue', 'green', 'red', 'cyan', 'magenta', 'orange']
forecast_colors = ['grey', 'lightblue', 'lightgreen', 'salmon', 'lightcyan', 'pink', 'lightyellow']

# Plotting the actual and forecasted values for 'Total' and other components
plt.figure(figsize=(14, 8)) #TODO: Width 14, Height 8 inches

#* Loop through each category to plot, fit ARIMA model, forecast, and plot forecast
for i, component in enumerate(components):
    #? Plot actual data
    plt.plot(df.index, df[component], label=f'{component} Actual', color=colors[i], linewidth=2 if component == 'Total' else 1) #TODO: When plot total column linewidth=2 but in the other line width=1
    
    #? Forecasting for all categories
    model = ARIMA(df[component].dropna(), order=(1,1,10))  # Ensure to drop NaNs
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecast_years)
    plt.plot(forecast_index, forecast, linestyle='--', label=f'{component} Forecast', color=forecast_colors[i])

# Set x-axis limits explicitly to include all years and forecasted period
plt.xlim(df.index.min(), forecast_index.max())

# Adding more ticks for clarity if needed
plt.xticks(np.linspace(df.index.min(), forecast_index.max(), num=20, dtype=int), rotation=45)

plt.title('Demand Forecasting Transmission Lines by Time Series Method')
plt.xlabel('Year')
plt.ylabel('Transmission Lines (Circuits-Kilometers)')
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.style.use('ggplot')
plt.show()
