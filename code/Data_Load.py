#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:12:40 2017

@author: WhoaaaItsDavid
"""

import os
import re
import pandas as pd
from sortedcontainers import SortedList
from collections import Counter


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
rootdir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing/Capital Bikeshare Data'
main_dir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing'
bar_delim = '================================================'
os.chdir(main_dir)
from Bike_Functions import *

full_data_dict = {}
#Read in bike share data and create a dictionary to hold all dataframes
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        os.chdir(subdir)
        if not file.startswith('.'):
            name = re.findall(r'([0-9]+[-][Q][0-9])', file)[0]
            version = re.findall(r'([-][1-2])', file)
            if len(version) > 0:
                name += version[0]
            full_data_dict[name] = pd.read_csv(file)
            print(file)


#Create the first file, 'full_data_dict info - ORIGINAL.txt', and write to it
full_data_dict_file = openfile(main_dir, 'full_data_dict info - ORIGINAL.txt')
create_info_doc(full_data_dict_file, full_data_dict, bar_delim)
write_feature_names_counts(full_data_dict_file, full_data_dict)
full_data_dict_file.close()


#Create a dictionary copy for further edits
full_data_dict_edit = full_data_dict.copy()

#Partition the file names to access different dataframes independently and rename feature names
good_file_names = ['2010-Q4', '2011-Q1', '2011-Q2', '2011-Q3', '2011-Q4', '2012-Q1', '2012-Q2', '2012-Q3', '2012-Q4', '2013-Q1', '2013-Q2', '2013-Q3']
global_good_feature_names = ['Duration', 'Start Date', 'End Date', 'Start Station', 'End Station', 'Bike Number', 'Member Type']

switched_file_names = ['2013-Q4', '2014-Q1', '2014-Q2', '2014-Q3', '2014-Q4', '2015-Q1', '2015-Q2']
global_switched_feature_names = ['Duration', 'Start Date', 'Start Station', 'End Date', 'End Station', 'Bike Number', 'Member Type']

additional_features_file_names = ['2015-Q3', '2015-Q4', '2016-Q1', '2016-Q2', '2016-Q3-1', '2016-Q3-2']
global_additional_features_file_names = ['Duration', 'Start Date', 'End Date', 'Bike Number', 'Member Type', 'Start Station', 'End Station']

#Change the feature names based on partitions above
count = 0
for file_name in full_data_dict_edit:
    if file_name in good_file_names:
        count += 1
        full_data_dict_edit[file_name].columns = global_good_feature_names
        print(file_name, '-good-', count)                   
    elif file_name in switched_file_names:
        count += 1
        full_data_dict_edit[file_name].columns = global_switched_feature_names
        print(file_name, '-switched-', count)                   
    elif file_name in additional_features_file_names:
        count += 1
        full_data_dict_edit[file_name]['Start Station_Number'] = full_data_dict_edit[file_name]['Start station'] + ' (' + full_data_dict_edit[file_name]['Start station number'].astype(str) + ')'
        print(file_name, '-additional-', count)                   
        full_data_dict_edit[file_name].drop(['Start station', 'Start station number'], inplace=True, axis=1)
                      
        full_data_dict_edit[file_name]['End Station_Number'] = full_data_dict_edit[file_name]['End station'] + ' (' + full_data_dict_edit[file_name]['End station number'].astype(str) + ')'
        print(file_name, '-additional-', count)                   
        full_data_dict_edit[file_name].drop(['End station', 'End station number'], inplace=True, axis=1)

        full_data_dict_edit[file_name].columns = global_additional_features_file_names


#Create the second file, 'full_data_dict info - EDIT.txt', and write to it
full_data_dict_file = openfile(main_dir, 'full_data_dict info - EDIT.txt')
create_info_doc(full_data_dict_file, full_data_dict_edit, bar_delim) 
write_feature_names_counts(full_data_dict_file, full_data_dict_edit, reset=True)
full_data_dict_file.close()


#Create a mapable regex function to find zipcodes in station features
find_zip = lambda x: re.findall(r'[0-9]+', x)

#Create new features in each data frame for Start Zip and End Zip
sorted_full_data_dict_edit = SortedList()
sorted_full_data_dict_edit.update(list(full_data_dict_edit.keys()))
count=0
for file in sorted_full_data_dict_edit:
    count += 1
    for feature in full_data_dict_edit[file]: 
        if feature == 'Start Station':
            full_data_dict_edit[file]['Start Zip'] = full_data_dict_edit[file][feature].astype(str).map(find_zip)
            print(file, '-start-', count)
            
        elif feature == 'End Station':
            full_data_dict_edit[file]['End Zip'] = full_data_dict_edit[file][feature].astype(str).map(find_zip)
            print(file, '-end-', count)


#Create the third file, 'Create Zipcodes.txt', and write to it
create_zip_file = openfile(main_dir, 'Create Zipcodes.txt')
create_info_doc(create_zip_file, full_data_dict_edit, bar_delim) 
write_feature_names_counts(create_zip_file, full_data_dict_edit, reset=True)
create_zip_file.close()






