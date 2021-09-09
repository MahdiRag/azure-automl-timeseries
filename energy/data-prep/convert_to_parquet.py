# Convert CSV file to parquet format
import pandas as pd

# Load data, convert Date to datetime, and sort
df = pd.read_csv('./../input-data/energy-train.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.to_parquet('./../input-data/energy-train.parquet')
