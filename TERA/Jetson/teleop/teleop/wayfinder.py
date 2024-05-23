from gps import get_gps_ENU
import math
import pandas as pd
#from numpy import genfromtxt
import numpy as np

data = pd.read_csv(r'/home/ejvirkus/TERA/TERA/Jetson/GPS_utils/gps_ENU.csv', header=0, usecols=['X', 'Y'])

data_array = np.array(data)

i = 0

def get_target_location(): # Acquiring the closest or next point to which to move
    for x in data_array.index:
        current_min_dist = math.dist(data.at[x], get_gps_ENU()[0, 1]) # Iterating through all points
        i += 1

        if target_location == None or current_min_dist < target_location: # Assigning closest point
            target_location = current_min_dist
    return target_location