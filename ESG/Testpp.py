import pandas as pd 
#TODO: Import Dataframe of Each Parquet Files
df1 = pd.read_parquet('ESG/thai_esg_scores')
df2 = pd.read_parquet('ESG/thai_fundamental_data_items')
df3 = pd.read_parquet('ESG/thai_fundamentals')
df4 = pd.read_parquet('ESG/thai_stocks_eod_price')
df5 = pd.read_parquet('ESG/thai_universe')


df_score = df1['SCORE']
#print(df_score)
 

multi_index = pd.MultiIndex.from_tuples(df_score, names=['ITEM_NAME', 'ORGPERMID'])

df = pd.DataFrame(index=multi_index, columns=['Value1', 'Value2'])

#TODO: ตรวจสอบ ITEM_NAME ที่มีอยู่
item_names = df.index.get_level_values('ITEM_NAME').unique()
print(item_names)

#TODO: Categorized All of Index in each Categories
emission_score = df1['SCORE']['Emissions Score']
csr_strategy_score = df1['SCORE']['CSR Strategy Score']
community_score = df1['SCORE']['Community Score']
esg_combined_score = df1['SCORE']['ESG Combined Score']
esg_controversies_score = df1['SCORE']['ESG Controversies Score']
esg_score = df1['SCORE']['ESG Score']
environment_pillar_score = df1['SCORE']['Environment Pillar Score']
environmental_innovation_score = df1['SCORE']['Environmental Innovation Score']
governance_pillar_score = df1['SCORE']['Governance Pillar Score']
human_rights_score = df1['SCORE']['Human Rights Score']
management_score = df1['SCORE']['Management Score']
product_responsibility_score = df1['SCORE']['Product Responsibility Score']
resource_use_score = df1['SCORE']['Resource Use Score']
shareholders_score = df1['SCORE']['Shareholders Score']
social_pillar_score = df1['SCORE']['Social Pillar Score']
workforce_score = df1['SCORE']['Workforce Score']


#TODO:Choose Column 10 which is latest score in 2022
emission_2022 = emission_score.iloc[10]


#TODO: Choose Only Top ten in Most highest selected score
esg_sorted = emission_2022.sort_values(ascending=False).head(11)
print(esg_sorted)

df_result = pd.DataFrame(list(esg_sorted.items()), columns=['SYM_INST_ORGPERMID', 'Score'])
df_result['SYM_INST_ORGPERMID'] = df_result['SYM_INST_ORGPERMID'].astype('str')
df5['SYM_INST_ORGPERMID'] = df5['SYM_INST_ORGPERMID'].astype('str')
result_inner = pd.merge(df_result, df5, on='SYM_INST_ORGPERMID', how='inner')
print(result_inner)

filtered_result = result_inner[(result_inner['DS_IS_PRIMQT'] == 1) & (result_inner['DS_SECTYPE'] == 'Ordinary Share') & (~result_inner['DS_QT_NAME'].str.endswith('NVDR'))]
print(filtered_result)
top20_2022 = filtered_result[['DS_QT_NAME','security','Score']]
print(top20_2022)