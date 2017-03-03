#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 10:29:11 2017

@author: WhoaaaItsDavid
"""

import os
import pandas as pd

main_dir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing'
os.chdir(main_dir)

# Import the 3rd version of the data
full_df = pd.read_csv('full_subset_data - V3.csv')
full_df.drop(['Unnamed: 0', 'Duration', 'Start Date', 'End Date',
               'Bike Number', 'Member Type', 'Distance'], 
                axis=1, inplace=True)

# Create functions that can deal with splits and NaNs for making latitude/longitude features
def lat_split(location):
    if pd.notnull(location):
        location = str(location).split(', ')[0].lstrip('(')
    return location

def long_split(location):
    if pd.notnull(location):
        location = str(location).split(', ')[1].rstrip(')')
    return location

# Split the original data into a dataframe that shows only the start location information
start_df_counts = pd.DataFrame(full_df['Start Location'].value_counts(dropna=False))
start_df_counts.reset_index(drop=False, inplace=True)
start_df_counts.columns = ['Start Location', 'Counts']
start_df_counts = start_df_counts.merge(full_df[['Start Location', 'Start Station Number', 'Start Station']], how='left', on='Start Location')
start_df_counts.drop_duplicates(inplace=True)
start_df_counts['Start Location Lat'] = start_df_counts['Start Location'].map(lambda x: lat_split(x))
start_df_counts['Start Location Long'] = start_df_counts['Start Location'].map(lambda x: long_split(x))
start_df_counts.drop('Start Location', axis=1, inplace=True)
start_df_counts.reset_index(drop=True, inplace=True)

# Split the original data into a dataframe that shows only the end location information
end_df_counts = pd.DataFrame(full_df['End Location'].value_counts(dropna=False))
end_df_counts.reset_index(drop=False, inplace=True)
end_df_counts.columns = ['End Location', 'Counts']
end_df_counts = end_df_counts.merge(full_df[['End Location', 'End Station Number', 'End Station']], how='left', on='End Location')
end_df_counts.drop_duplicates(inplace=True)
end_df_counts['End Location Lat'] = end_df_counts['End Location'].map(lambda x: lat_split(x))
end_df_counts['End Location Long'] = end_df_counts['End Location'].map(lambda x: long_split(x))
end_df_counts.drop('End Location', axis=1, inplace=True)
end_df_counts.reset_index(drop=True, inplace=True)

# Print out descriptive stats to see if anything is wrong in the data
print('Unique Start Station Lat/Long:', len(list(full_df['Start Location'].unique())))
print('Unique Start Station Numbers:', len(list(start_df_counts['Start Station Number'].unique())))
print('Unique Start Stations:', len(list(start_df_counts['Start Station'].unique())))
print('Unique End Station Lat/Long:', len(list(full_df['End Location'].unique())))
print('Unique End Station Numbers:', len(list(end_df_counts['End Station Number'].unique())))
print('Unique End Stations:', len(list(end_df_counts['End Station'].unique())))

# Based on the above print results, determine where exactly there are issues in the start dataframe
for row in start_df_counts.itertuples():
    try:
        if start_df_counts.get_value(row[0], 'Start Station Number') == start_df_counts.get_value(row[0]-1, 'Start Station Number'):
            print('Start Station Number:', start_df_counts.get_value(row[0]-1, 'Start Station Number'), 
                  '\nStart Station Name:', start_df_counts.get_value(row[0]-1, 'Start Station'), 
                  '\nCount:', start_df_counts.get_value(row[0]-1, 'Counts'),
                  'Lat:', start_df_counts.get_value(row[0]-1, 'Start Location Lat'),
                  'Long:', start_df_counts.get_value(row[0]-1, 'Start Location Long'))
            print('Start Station Number:', start_df_counts.get_value(row[0], 'Start Station Number'), 
                  '\nStart Station Name:', start_df_counts.get_value(row[0], 'Start Station'), 
                  '\nCount:', start_df_counts.get_value(row[0], 'Counts'),
                  'Lat:', start_df_counts.get_value(row[0], 'Start Location Lat'),
                  'Long:', start_df_counts.get_value(row[0], 'Start Location Long'), end='\n\n')
    except:
        pass

# Based on the above print results, determine where exactly there are issues in the end dataframe
for row in end_df_counts.itertuples():
    try:
        if end_df_counts.get_value(row[0], 'End Station Number') == end_df_counts.get_value(row[0]-1, 'End Station Number'):
            print('End Station Number:', end_df_counts.get_value(row[0]-1, 'End Station Number'), 
                  '\nEnd Station Name:', end_df_counts.get_value(row[0]-1, 'End Station'), 
                  '\nCount:', end_df_counts.get_value(row[0]-1, 'Counts'),
                  'Lat:', end_df_counts.get_value(row[0]-1, 'End Location Lat'),
                  'Long:', end_df_counts.get_value(row[0]-1, 'End Location Long'))
            print('End Station Number:', end_df_counts.get_value(row[0], 'End Station Number'), 
                  '\nEnd Station Name:', end_df_counts.get_value(row[0], 'End Station'), 
                  '\nCount:', end_df_counts.get_value(row[0], 'Counts'),
                  'Lat:', end_df_counts.get_value(row[0], 'End Location Lat'),
                  'Long:', end_df_counts.get_value(row[0], 'End Location Long'), end='\n\n')
    except:
        pass


# Drop the Start and End Station names from the original dataframe
# Write new, updated dataframe to a csv file
new_df = pd.read_csv('full_subset_data - V3.csv')
new_df.drop(['Unnamed: 0', 'Start Station', 'End Station'], 
                axis=1, inplace=True)
new_df_csv = open('full_subset_data - V4.csv', 'w')
new_df_csv.write(new_df.to_csv())
new_df_csv.close()