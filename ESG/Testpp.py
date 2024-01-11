import pandas as pd 
#TODO: Import Dataframe of Each ESG Files
df1 = pd.read_parquet('Hackathon/thai_esg_scores')
df2 = pd.read_parquet('Hackathon/thai_fundamental_data_items')
df3 = pd.read_parquet('Hackathon/thai_fundamentals')
df4 = pd.read_parquet('Hackathon/thai_stocks_eod_price')
df5 = pd.read_parquet('Hackathon/thai_universe')


df_score = df1['SCORE']
print(df_score)
 

multi_index = pd.MultiIndex.from_tuples(df_score, names=['ITEM_NAME', 'ORGPERMID'])

df = pd.DataFrame(index=multi_index, columns=['Value1', 'Value2'])

# ตรวจสอบ ITEM_NAME ที่มีอยู่
item_names = df.index.get_level_values('ITEM_NAME').unique()
print(item_names)


emission_score = df1['SCORE']['ESG Score']
print(emission_score)
#Choose Column 9 which is emission score in 2021
emission_2021 = emission_score.iloc[9]
print(emission_2021)

#Choose Only Top ten in Most highest Emission Score
df_esg_sorted = emission_2021.sort_values(ascending=False).head(11)


'''
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# Assuming df4 contains historical stock prices with stocks as columns
# Select the stocks from your sorted ESG scores
selected_stocks = df4[df_esg_sorted.index]

# Calculate expected returns and the annualized sample covariance matrix
mu = expected_returns.mean_historical_return(selected_stocks)
S = risk_models.sample_cov(selected_stocks)

# Optimize for the maximal Sharpe ratio (risk-adjusted return)
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()

# Print the weights of the portfolio
print(cleaned_weights)

# Get the expected performance of the portfolio
portfolio_performance = ef.portfolio_performance(verbose=True)
'''