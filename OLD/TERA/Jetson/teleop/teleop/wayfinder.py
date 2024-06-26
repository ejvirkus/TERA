from gps import GpsPublisher
import math
import pandas as pd
from numpy import genfromtxt
import numpy as np

data = pd.read_csv(r'/home/tera/TERA/TERA/Jetson/GPS_utils/gps_ENU.csv', header=0, usecols=['X', 'Y'])

data_array = genfromtxt(data, delimiter=',')
data_array = np.round(data_array, 3)

i = 0

def get_target_location(): # Acquiring the closest or next point to which to move
    if target_location == []: # If there is no target location, the program finds the closest point to the robot.
        for x in data_array.index:
            current_min_dist = math.dist(data_array.at[x], GpsPublisher.get_gps_ENU()[0, 1]) # Iterating through all points
            i += 5

            if target_location == None or current_min_dist < target_location: # Assigning closest point
                target_location = current_min_dist
    else:
        target_location = data.at[i+5]
        i += 5
    return target_location