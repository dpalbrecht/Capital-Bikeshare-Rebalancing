#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 14:52:19 2017

@author: WhoaaaItsDavid
"""

import os
from sortedcontainers import SortedList
from collections import Counter

#Set the directory and new file creation
def openfile(directory, file_name):
    os.chdir(directory)
    return open(file_name, 'w')

#Write the file name, feature names, and header information to a file
def create_info_doc(write_to_file, dictionary, delim):
    #Sort the dictionary by key for chronological access
    sorted_full_data_dict = SortedList()
    sorted_full_data_dict.update(list(dictionary.keys()))
    
    for key in sorted_full_data_dict:
        write_to_file.write('File name: ' + key + '\n')
        
        write_to_file.write('Column names: ')
        for feature in dictionary[key].columns:
            write_to_file.write(feature + ', ')

        write_to_file.write('\nDF:\n' + str(dictionary[key].head()))
        write_to_file.write('\n\n' + delim + '\n\n')

#Find the number of unique feature names, counts, and write to file
def write_feature_names_counts(write_to_file, dictionary, feature_list = [], reset=False):
    if reset == True:
        feature_list = []
        
    #Sort the dictionary by key for chronological access
    sorted_full_data_dict = SortedList()
    sorted_full_data_dict.update(list(dictionary.keys()))
    
    for key in list(dictionary.keys()):
        for feature in dictionary[key].columns:
            feature_list.append(feature)
            
    write_to_file.write('Unique column names and counts:\n')
    for counted_col in Counter(feature_list):
        write_to_file.write(counted_col + ': ' + 
                              str(Counter(feature_list)[counted_col]) + '\n')

    write_to_file.write('\n\nColumn names per separate dataframe:')
    for sorted_key in sorted_full_data_dict:
        write_to_file.write('\n' + sorted_key + ': ' + 
                              str(len(dictionary[sorted_key].columns)) + '\n')
        for feature in dictionary[sorted_key].columns:
                write_to_file.write(feature + ', ')
