#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:10:17 2017

@author: WhoaaaItsDavid
"""

import os
import pandas as pd
import numpy as np

main_dir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing'
os.chdir(main_dir)

# Import 4th version of the data
main_df = pd.read_csv('full_subset_data - V4.csv')
main_df.drop('Unnamed: 0', axis=1, inplace=True)

# Mask the data for start or end stations that match #31116
df_31116 = main_df[(main_df['Start Station Number'] == 31116) | (main_df['End Station Number'] == 31116)]
df_31116.drop(['Duration', 'Bike Number', 'Member Type', 'Start Location', 
                    'End Location', 'Distance'], axis=1, inplace=True)
df_31116['Status'] = np.nan
df_31116['Start Date'] = pd.to_datetime(df_31116['Start Date'])
df_31116['End Date'] = pd.to_datetime(df_31116['End Date'])

"""
# Write df_31116 to CSV file for ease of use
reduced_df_csv = open('31116_subset_data.csv', 'w')
reduced_df_csv.write(df_31116.to_csv())
reduced_df_csv.close()
"""

# Split df_31116 into start station dataframe that matches 31116
df_31116_start = df_31116[df_31116['Start Station Number'] == 31116]
df_31116_start.drop(['End Date', 'Start Station Number', 'End Station Number'], axis=1, inplace=True)
df_31116_start['Status'] = 'subtract bike'
df_31116_start.set_index('Start Date', drop=False, inplace=True)

# Split df_31116 into end station dataframe that matches 31116
df_31116_end = df_31116[df_31116['End Station Number'] == 31116]
df_31116_end.drop(['Start Date', 'Start Station Number', 'End Station Number'], axis=1, inplace=True)
df_31116_end.columns = ['Start Date', 'Status']
df_31116_end['Status'] = 'add bike'
df_31116_end.set_index('Start Date', drop=False, inplace=True)

# Import data from CaBi Tracker that shows full, empty notifications over the 2015Q3-2016Q3 timeline
df_31116_full_empty = pd.read_csv('full empty_31116_new.csv')
df_31116_full_empty.drop(['Station Name', 'Duration'], axis=1, inplace=True)

# Split CaBi Tracker data for when an empty notification starts
df_31116_empty_start = df_31116_full_empty.drop(['End'], axis=1)
df_31116_empty_start = df_31116_empty_start[df_31116_empty_start['Status'] == 'empty']
df_31116_empty_start['Status'] = 'start empty'
df_31116_empty_start.columns = ['Station Number', 'Status', 'Start Date']
df_31116_empty_start.set_index('Start Date', drop=False, inplace=True)

# Split CaBi Tracker data for when an empty notification ends
df_31116_empty_end = df_31116_full_empty.drop(['Start'], axis=1)
df_31116_empty_end = df_31116_empty_end[df_31116_empty_end['Status'] == 'empty']
df_31116_empty_end['Status'] = 'end empty'
df_31116_empty_end.columns = ['Station Number', 'Status', 'Start Date']
df_31116_empty_end.set_index('Start Date', drop=False, inplace=True)

# Split CaBi Tracker data for when a full notification starts
df_31116_full_start = df_31116_full_empty.drop(['End'], axis=1)
df_31116_full_start = df_31116_full_start[df_31116_full_start['Status'] == 'full']
df_31116_full_start['Status'] = 'start full'
df_31116_full_start.columns = ['Station Number', 'Status', 'Start Date']
df_31116_full_start.set_index('Start Date', drop=False, inplace=True)

# Split CaBi Tracker data for when a full notification ends
df_31116_full_end = df_31116_full_empty.drop(['Start'], axis=1)
df_31116_full_end = df_31116_full_end[df_31116_full_end['Status'] == 'full']
df_31116_full_end['Status'] = 'end full'
df_31116_full_end.columns = ['Station Number', 'Status', 'Start Date']
df_31116_full_end.set_index('Start Date', drop=False, inplace=True)

# Combine the above, split, 6 dataframes into a single dataframe, full_31116_df, and sort on start datetime
full_31116_df = df_31116_start.append([df_31116_end, df_31116_empty_start, df_31116_empty_end, df_31116_full_start, df_31116_full_end])

full_31116_df['Station Number'] = full_31116_df['Station Number'].astype(str)
full_31116_df['Start Date'] = pd.to_datetime(full_31116_df['Start Date']) 
full_31116_df['Bike Count'] = np.nan
full_31116_df.sort_values(by='Start Date', ascending=True, inplace=True)
full_31116_df.reset_index(drop=True, inplace=True)
full_31116_df = full_31116_df[full_31116_df['Start Date'] >= '2015-07-01 00:00:00']
full_31116_df = full_31116_df[full_31116_df['Start Date'] <= '2016-09-30 23:59:59']
full_31116_df.reset_index(drop=True, inplace=True)

# Iterate over the rows in full_31116_df and create new feature, Bike Count, 
# to keep track of number of bikes at the station at every time stamp
cut_first_empty = 1
for row in full_31116_df.itertuples():
            
    if row[3] == 'end empty' or row[3] == 'start full' or row[3] == 'end full':
        try:
            full_31116_df.set_value(row[0], 'Bike Count', 
                                    full_31116_df.get_value(row[0]-1, 'Bike Count'))
        except:
            full_31116_df.set_value(row[0], 'Bike Count', 0)
  
    elif row[3] == 'start empty':
        full_31116_df.set_value(row[0], 'Bike Count', 0) 
        
        if cut_first_empty == 1:
            full_31116_df.drop(full_31116_df.index[:row[0]], inplace=True)
            cut_first_empty -= 1
    
    elif row[3] == 'add bike':
        try:
            full_31116_df.set_value(row[0], 'Bike Count', 
                                    full_31116_df.get_value(row[0]-1, 'Bike Count')+1)
        except:
            pass
        
    elif row[3] == 'subtract bike':
        try:
            full_31116_df.set_value(row[0], 'Bike Count', 
                                    full_31116_df.get_value(row[0]-1, 'Bike Count')-1)
        except:
            pass
