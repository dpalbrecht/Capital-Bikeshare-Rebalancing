#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 17:13:39 2017

@author: WhoaaaItsDavid
"""

import os
import pandas as pd
from geopy.distance import distance

main_dir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing'
os.chdir(main_dir)

#Open most updated csv file as a df and create a new Distance feature
main_df = pd.read_csv('full_subset_data - V2.csv')
main_df.drop('Unnamed: 0', inplace=True, axis=1)
main_df['Distance'] = main_df.apply(lambda row: distance(row['Start Location'], row['End Location']).miles, axis=1)

#Write new, updated dataframe to a csv file
main_df_csv = open('full_subset_data - V3.csv', 'w')
main_df_csv.write(main_df.to_csv())
main_df_csv.close()
