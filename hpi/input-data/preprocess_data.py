import datetime
import random
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
df = pd.read_parquet('HPI_master.parquet')

mth_qtr_mapping = {1:3,2:6,3:9,4:12}

# Filtering conditions
df = df [ df['frequency'] =='quarterly']
df = df [ df['level'] == 'MSA']
df = df [ df['hpi_type'] == 'traditional']
df = df [ df['hpi_flavor'] == 'all-transactions']

# Added columns, for date changes
df['month'] = df['period'].map(mth_qtr_mapping).astype(str)
df = df.rename(columns={'yr':'year'})
df['year'] = df['year'].astype(str)
df['day'] = '1'
df['Date']= pd.to_datetime(df[['year','month','day']])

# Given data gaps between MSAs, starting from Q4, 2000
df = df.loc [ df['Date'] >= '2000-11-01']

# Drop unneeded columns
df = df.drop(['frequency', 'level', 'hpi_type', 'hpi_flavor','year', 'period','day','month',
    'index_sa', 'place_id'], axis=1)

# Get list of place, and filter for a random sample
place_list = list(df['place_name'].unique())
#print(f" Length of place id list is {len(place_list)}")

def model_chart_sample(df=None,xtype=None, count=None):
    random_sample = random.sample(place_list, count)
    df = df [ df['place_name'].isin(random_sample) ]
    if xtype=='model':
        # Re-format to get 
        dfx = df.pivot_table(index='Date',values='index_nsa', columns='place_name')
        print(dfx.head())
        print(f" Random sample length is {len(dfx)}")
        dfx.to_csv('random_sample.csv')
    elif xtype=='chart':
        dfx = df.pivot_table(index='Date',values='index_nsa', columns='place_name')
        ts = dt.datetime.now().strftime('%s')
        dfx.plot(title=f'Sample of {count} MSAs')
        plt.savefig(f'Sample_of_{count}' + str(ts) + '.png')

#model_chart_sample(df=df, xtype='chart', count=1)
model_chart_sample(df=df, xtype='model', count=5)
