#  Packages
import pandas as pd 
import numpy as np 
from collections import Counter 
#################################

# import data
df = pd.read_excel('SoundData.xlsx')
#df.to_csv("SoundData.csv", index=False)

# overview data structure
print(df.info())         # shows columns, number of entries and variable type
print('-'*30)
print(df.columns)        # shows colum names
print('-'*30)

#################################
### cleaning step 1: drop unneeded columns ###
columns_to_drop = ['file', 'sample_pos', 'channel', 
                   'date_time', 'daytime', 'Index']
df_1 = df.drop(columns=columns_to_drop)

#################################
### cleaning step 2: check remaining data points for NULL-values ###

#overview 0-entries
print(df_1.isnull().sum()) # shows number of NULL entries 
print('-'*30)

# check root of NULL-problem

print(df_1[df_1['vehicle'].isna()])
print(df_1[df_1['vehicle'].isna() & (df_1['is_background'] == True )])

print(df_1[df_1['weather'].isna()])
print(df_1[df_1['weather'].isna() & (df_1['is_background'] == True )])

quote = 100 * (len(df_1[df_1['weather'].isna() & (df_1['is_background'] == True )]) / len(df_1[df_1['weather'].isna()])) 
print( f"{quote:.2f}% of NULL-values are in the same row with the feature is_background == true")

# drop rows with is_background == true

df_2 = df_1[df_1['is_background'] != True]


### cleaning step 3: check remaining data points for conspicousness ###

# overview crucial columns
print("Possible values of speed are: " , df_2['speed_kmh'].unique())
print("Possible values of vehicle type are: " ,df_2['vehicle'].unique())
print("Possible values of location are: " ,df_2['location'].unique())
print('-'*30)

# show all values of "speed" pro "location"
print(df_2.groupby('location')['speed_kmh'].apply(list))
print('-'*30)
# values for "Hohenwarte"
print(df_2[df_2['location'] == 'Hohenwarte']['speed_kmh']) 
print("Number of unlabeled Data regarding speed: ", len(df_2[df_2['location'] == 'Hohenwarte']))

# drop rows of unlabeled speed data 

df_3 = df_2[~((df_2['location'] == 'Hohenwarte') 
              & (df_2['speed_kmh'] == "UNK"))]

# drop low quality microphone??


### Final: Save clean data with index=False to preserve proper formatting
df_3.to_csv('CleanData.csv', index=False, sep=",")


