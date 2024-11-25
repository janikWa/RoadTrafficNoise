#  Packages
import pandas as pd 
import numpy as np 
from collections import Counter 
#################################

# import data
df = pd.read_excel('SoundData.xlsx')
df.to_csv("SoundData.csv", index=False)

# overview data structure
print(df.info())         # shows columns, number of entries and variable type
print('-'*30)
print(df.columns)        # shows colum names
print('-'*30)
print(df.isnull().sum()) # shows number of NULL entries 

### cleaning step 1: drop unneeded columns ###

df = df.drop(columns=['file', 'sample_pos', 'channel', 'date_time', 'daytime']) 
# save clean data
df.to_csv('CleanData.csv', index=False)  # Überschreibt die bestehende Datei ohne Indexspalte

# create correct daytime
split_cols = df['date_time'].str.split('-', expand=True)
df['hour'] = split_cols[3]
df['minute'] = split_cols[4]

df['time'] = df['hour'] + ':' + df['minute']
df['daytime_corrected'] = df['hour'].astype(int).apply(lambda x: 'M' if 0 <= x < 12 else 'A')
df.drop(columns=['hour', 'minute', 'date_time'], inplace=True)

print('-'*30)
print(df["daytime_corrected"].value_counts())
print(df.columns)





#print(rtn_data["weather"].value_counts())
#print(rtn_data["vehicle"].value_counts())
#print(rtn_data["source_direction"].value_counts())
