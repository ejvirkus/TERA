import csv
from gmplot import GoogleMapPlotter

# Open the CSV file
with open("gps_data_tera.csv", "r") as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    
    # Initialize lists to store latitude and longitude values
    lats = []
    lngs = []
    
    # Read each row of the CSV file
    for row in csv_reader:
        # Assuming the latitude is in the first column and longitude is in the second column
        lats.append(float(row[0]))
        lngs.append(float(row[1]))

# Initialize GoogleMapPlotter object with center coordinates and zoom level
gmap = GoogleMapPlotter(sum(lats) / len(lats), sum(lngs) / len(lngs), 19, map_type='satellite')

# Plot each GPS coordinate as a dot on the map
for lat, lng in zip(lats, lngs):
    gmap.scatter([lat], [lng], color='red', size=0.1, marker=True)

# Save the map to an HTML file
gmap.draw("gps_map_satellite.html")
