#Below is taken and modified from: https://kwkelly.com/blog/analyzing-capital-bikeshare-data-with-python-and-pandas/
import os
import urllib.request
import shutil
import xml.etree.ElementTree as et
import pandas as pd

def get_station_xml():
    url = "https://www.capitalbikeshare.com/data/stations/bikeStations.xml"
    download_dir = 'xml_data'
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    file_name = os.path.join(download_dir, 'bike_stations.xml')
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

get_station_xml()

def xml_to_pandas(xml_file):
    tree = et.parse(xml_file)
    root = tree.getroot()

    l = []
    for station in root:
        d = {}
        for attrib in station:
            d[str(attrib.tag)] = str(attrib.text)
        l.append(d)

    df = pd.DataFrame.from_dict(l)
    return df 
 
bike_stations = xml_to_pandas('xml_data/bike_stations.xml')
bike_stations['terminalName'] = bike_stations['terminalName'].astype(int)
bike_stations['lat'] = bike_stations['lat'].astype(float)
bike_stations['long'] = bike_stations['long'].astype(float)
station_locations = bike_stations[['terminalName']]
station_locations['location'] = list(zip(bike_stations['lat'], bike_stations['long']))


#Below is now my code:
main_dir = '/Users/WhoaaaItsDavid/Desktop/Springboard/Bike_Sharing'
os.chdir(main_dir)

#Combine original dataframe with new station lat/long data using a left join on End Station
subset_df = pd.read_csv('full_subset_data.csv')
subset_df.drop('Unnamed: 0', inplace=True, axis=1)

station_locations.columns = ['End Station Number', 'End Location']
subset_df_2 = pd.merge(subset_df, station_locations, how='left', on='End Station Number')

station_locations.columns = ['Start Station Number', 'Start Location']
subset_df_2 = pd.merge(subset_df_2, station_locations, how='left', on='Start Station Number')

#Count the number of missing values in each feature
print('\nMissing values:' )
for column in subset_df_2:
    print(column + ': ', subset_df_2[column].isnull().values.ravel().sum())

# Print out unique station numbers to check which stations do not have associated locations    
start_subset_test = subset_df_2[subset_df_2['Start Location'].isnull()]
print('Start Stations without locations:', start_subset_test['Start Station Number'].unique())
end_subset_test = subset_df_2[subset_df_2['End Location'].isnull()]
print('End Stations without locations:', end_subset_test['End Station Number'].unique())

#Write new, combined dataframe to a csv file
subset_data_csv = open('full_subset_data - V2.csv', 'w')
subset_data_csv.write(subset_df_2.to_csv())
subset_data_csv.close()