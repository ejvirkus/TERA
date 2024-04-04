#!/usr/bin/env python

import pymap3d as pm
import pandas as pd
import csv

data = pd.read_csv("~/OneDrive/Documents/GitHub/TERA/TERA/gps_data.csv", header=0, usecols=['Latitude', 'Longitude', 'Altitude']) # opening gps file for reading

csv_ENU_path = 'gps_ENU.csv' #opening the gps_ENU file for writing new values 
csv_file = open(csv_ENU_path, 'w', newline='')
csv_writer = csv.writer(csv_file)

file = open('gps_ENU.csv', 'r+') #opening and clearing the file
file.truncate(0)

fields = ['X', 'Y', 'Z'] #writing headers
csv_writer.writerow(fields)

lat0, lon0, h0 = 58.3428685594, 25.5692475361, 91.357 #GPS base station coordinates

x, y, z = 0, 0, 0 #initalizing values
    
for i in data.index:
    lat = data.at[i, 'Latitude']
    lon = data.at[i, 'Longitude']
    alt = data.at[i, 'Altitude']
    x, y, z = pm.geodetic2enu(lat, lon, alt, lat0, lon0, h0)
    csv_writer.writerow([x, y, z])