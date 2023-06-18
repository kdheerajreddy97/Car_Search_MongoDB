import pandas as pd
import requests

df = pd.read_csv('/Users/shreyapramod/Desktop/RIT Courses/ISTE610/XML/vehicles.csv')
df_updated = pd.DataFrame()

print("Original columns:")
print (df.columns)
print(df.isnull().sum())

df = df.drop(['url', 'region_url', 'fuel', 'title_status', 'VIN', 'drive', 'size', 'posting_date', 'county'], axis=1)
print("New columns with removed columns:")
print (df.columns)
print(df.isnull().sum())

df = df.dropna(subset=['lat', 'long', 'image_url', 'description'])

df.to_csv('craigslist.csv', index=False)