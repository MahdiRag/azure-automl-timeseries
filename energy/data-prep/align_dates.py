# Get datetime properly configured in the CSV file
import pandas as pd

raw_file = './../input-data/energy-train.csv'
processed_file = './../input-data/energy-train-processed.csv'

# Load data, convert Date to datetime, and sort
df = pd.read_csv(raw_file)
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date
df.sort_values(by='Date', ascending=True)

df.to_csv(processed_file,
        date_format='%Y-%m-%dT%H:%M:%S',
        encoding='utf-8',
        index=False
        )
