import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import plotly.express as px
import plotly.graph_objects as go
#TODO: Import Dataframe of Each Parquet Files
df1 = pd.read_parquet('ESG/thai_esg_scores')
df2 = pd.read_parquet('ESG/thai_fundamental_data_items')
df3 = pd.read_parquet('ESG/thai_fundamentals')
df4 = pd.read_parquet('ESG/thai_stocks_eod_price')
df5 = pd.read_parquet('ESG/thai_universe')
df6 = pd.read_csv('ESG/thai_universe_filter.csv')

df_score = df1['SCORE']
multi_index = pd.MultiIndex.from_tuples(df_score, names=['ITEM_NAME', 'ORGPERMID'])

df = pd.DataFrame(index=multi_index, columns=['Value1', 'Value2'])

# ตรวจสอบ ITEM_NAME ที่มีอยู่
item_names = df.index.get_level_values('ITEM_NAME').unique()
#TODO: Change this Lines
df_esg = df1['SCORE']['Workforce Score']
df_esg2022 = df_esg.iloc[10]
df_esg_sorted = df_esg2022.sort_values(ascending=False).head(10)
df_result = pd.DataFrame(list(df_esg_sorted.items()), columns=['SYM_INST_ORGPERMID', 'Score'])
#TODO:
df6 = df6.dropna(subset=['SYM_INST_ORGPERMID'])

# Convert to integer after replacing 'nan' with 0
df6['SYM_INST_ORGPERMID'] = df6['SYM_INST_ORGPERMID'].replace('nan', 0).astype(float).astype(int)
# Drop rows with NaN values in 'SYM_INST_ORGPERMID'
df6 = df6.dropna(subset=['DS_IS_PRIMQT'])

# Convert to integer after replacing 'nan' with 0
df6['DS_IS_PRIMQT'] = df6['DS_IS_PRIMQT'].replace('nan', 0).astype(float).astype(int)

# แปลงประเภทของคอลัมน์เป็น int64
df_result['SYM_INST_ORGPERMID'] = df_result['SYM_INST_ORGPERMID'].astype('str')
df6['SYM_INST_ORGPERMID'] = df6['SYM_INST_ORGPERMID'].astype('str')
df6['DS_IS_PRIMQT'] = df6['DS_IS_PRIMQT'].astype('str')
result_inner = pd.merge(df_result, df6, on='SYM_INST_ORGPERMID', how='left')

# ลบแถวที่มีค่า 'nan' ใน DataFrame ทั้งหมด
result_inner = result_inner.dropna()
#TODO:
top20_2022 = result_inner[['DS_QT_NAME','security','Score','Industry Group','Sector']]
top20_2022 = top20_2022.tail(10)

# ใช้ .to_numpy()
security_array = top20_2022['security'].to_numpy()

# หรือใช้ .values
security_array = top20_2022['security'].values

# ลองแสดงผล array
print(security_array)
df_top_20 = security_array
df2018 = df4.loc['2022-1-1':'2022-12-31']
dftest = df2018[df_top_20]
missing_values = dftest.isnull().sum()
total_missing_values = dftest.isnull().sum().sum()
missing_data = dftest.isnull().sum()
# เติมข้อมูลที่หายไปด้วยค่าเฉลี่ย
dftest.fillna(dftest.mean(), inplace=True)
#remove the first row of the dataframe
df4_return1 =dftest.drop(dftest.index[0])
#remove the last row of the dataframe
df4_return2 = dftest.drop(dftest.index[-1])
#calculate the log return as defined
R_t = pd.DataFrame(np.log(df4_return1.values/df4_return2.values), columns = dftest.columns.tolist(), index = dftest.index.tolist()[1:])
R_t = R_t.rename_axis('date')
df_resampled = R_t.resample('M').sum()


df_resampled.plot(kind='line', marker='o', title='Line Plot')
plt.xlabel('Month')
plt.ylabel('Total Value')
plt.show()
mu_d = np.asarray(np.mean(R_t.values.T, axis = 1)) # daily
Sigma_d = np.asmatrix(np.cov(R_t.values.T)) # daily

#scale daily mu and Sigma to 30 days
mu = mu_d*30 # 30 days
Sigma = Sigma_d*30 # 30 days

#create the decision variable x with lenth equals the length of mu
X = cp.Variable(len(mu))
#define the required return (3 percent per month in this example)
r = 0.0083

#define the objective function
Portfolio_Risk = cp.quad_form(X,Sigma)
Objective = cp.Minimize(Portfolio_Risk)

#define constraints
Portfolio_Return = X.T*mu
Constraints = [Portfolio_Return >= r,sum(X)==1, X>= 0]

#solve the optimization problem
cp.Problem(Objective, Constraints).solve()

#extract the optimal portfolio
optimal_Portfolio = X.value

#display the optimal portfolio
print(optimal_Portfolio)
name_of_asset_list = df_top_20

#plot the optimal portfolio
fig = px.bar(x = name_of_asset_list, y = optimal_Portfolio, text_auto = '.4')
fig.update_layout(xaxis_title = 'Asset', yaxis_title = 'Proportion', title = 'Portfolio Proportion')
fig.show()

#display portfolio return and risk
Portfolio_Risk_Base = Portfolio_Risk.value
print(Portfolio_Return.value)
print(Portfolio_Risk.value)