#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:40:54 2017

@author: WhoaaaItsDavid
"""

import os
import re
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
rootdir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing/Capital Bikeshare Data'
main_dir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing'
bar_delim = '================================================'
os.chdir(main_dir)
from Bike_Functions import *

# Read in subset of bike share data and create a dictionary to hold all dataframes
subset = ['2015-Q3', '2015-Q4', '2016-Q1', '2016-Q2', '2016-Q3-1', '2016-Q3-2']
subset_data_dict = {}
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        os.chdir(subdir)
        if not file.startswith('.'):
            name = re.findall(r'([0-9]+[-][Q][0-9])', file)[0]
            version = re.findall(r'([-][1-2])', file)
            if len(version) > 0:
                name += version[0]
            if name in subset:
                subset_data_dict[name] = pd.read_csv(file)
                print(file)

            
# Standardize feature names across subset of data                
new_feature_names = ['Duration', 'Start Date', 'End Date', 'Start Station Number', 'Start Station', 'End Station Number', 'End Station', 'Bike Number', 'Member Type']

count = 0
for file_name in subset_data_dict:
    count += 1
    subset_data_dict[file_name].columns = new_feature_names
    print(file_name, '-', count)


# Create the fourth file, 'subset_data_dict info.txt', and write to it
subset_data_dict_file = openfile(main_dir, 'subset_data_dict info.txt')
create_info_doc(subset_data_dict_file, subset_data_dict, bar_delim) 
write_feature_names_counts(subset_data_dict_file, subset_data_dict, reset=True)
subset_data_dict_file.close()


#Count the number of missing values in each dataframe
print('\nMissing values:' )
for file in subset_data_dict:
    print(file + ': ', subset_data_dict[file].isnull().values.ravel().sum())

# Combine the entire subset into one dataframe
subset_df = subset_data_dict[subset[0]].append(subset_data_dict[subset[1]]).append(subset_data_dict[subset[2]]).append(subset_data_dict[subset[3]]).append(subset_data_dict[subset[4]]).append(subset_data_dict[subset[5]])

# Write new, combined dataframe to a csv file
subset_data_csv = open('full_subset_data.csv', 'w')
subset_data_csv.write(subset_df.to_csv())
subset_data_csv.close()
