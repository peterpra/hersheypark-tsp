# -*- coding: utf-8 -*-
"""
@author: Peter Pranata
"""
# Imports necessary modules and packages
import pandas as pd
from opencage.geocoder import OpenCageGeocode
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from amusement.parks.HersheyPark import HersheyPark

# Assigns the API key for geocoder API
# You will need to obtain the API key from: https://opencagedata.com/users/sign_in
key = 'YourOpenCageAPIKey'
geocoder = OpenCageGeocode(key)
# Log-in to plotly using the follow command:
# You need to first register and get the API key from the website
plotly.tools.set_credentials_file(username='YourPlotlyUserID', api_key='YourPlotlyAPIKey')

# Make sure to connect your Mapbox token to your Plotly account
mapbox_access_token = 'YourMapBoxAccessToken'

# Extracts the live data from HersheyPark for all attractions
hp = HersheyPark()
hpl = hp.rides() # Shows the entire data for taken from HersheyParks


# This is a dummy listed dictionary that is used to build the code
# The structure is the same as the data extracted from HersheyPark
# We will use this for practice building the code
#status = [{'name': 'Carrousel', 'wait': 0, 'isOpen': True, 'single_rider': None},
# {'name': 'Balloon Flite', 'wait': 0, 'isOpen': True, 'single_rider': None},
# {'name': 'Skyrush', 'wait': 0, 'isOpen': False, 'single_rider': None},
# {'name': 'SooperDooperLooper',
#  'wait': 5,
#  'isOpen': True,
#  'single_rider': None},
# {'name': 'Fahrenheit', 'wait': 20, 'isOpen': True, 'single_rider': None},
# {'name': 'Dummy', 'wait': 0, 'isOpen': False, 'single_rider': None}]

# This loop filters out all the attraction that is not open
#for i in status:
#	if i['isOpen']: # The values of the key is boolean
#		print(i)

# Initiates user input for customization
		# User needs to input their starting location and the unit of measurement to be used
ride = input('What is your starting location?\nPlease insert the name of the closest attraction: ')
metric = input('What unit of measurement do you prefer? (Meters or Feet): ')

# This will set the multiplier for the total distance taken by the route
if metric == 'Meters':
	unit = 1609.34
elif metric == 'Feet':
	unit = 5280
else:
	print('Please input the appropriate unit of measurement (Meters or Feet)')

# Sets the initial ride as the 1st value in the final route list
initial_ride = ride

# Creates empty list for each of the values in the original data
name = list()
wait = list()
lat = list()
long = list()

# Loops through every row in the listed dictionary (the original data) and appends each value to the empty list
for k in range(len(hpl)):
	try:
		name.append(hpl[k]['name'])
		wait.append(hpl[k]['wait'])
		# Utilize geocoder from opencage to get their coordinates
		results = geocoder.geocode('%s, Hershey Park Dr' % (hpl[k]['name']))
		lat.append(results[0]['geometry']['lat'])
		long.append(results[0]['geometry']['lng'])
# For attractions that has no coordinates, we will append a value of 0 for both latitude and longitude
	except IndexError:
		lat.append(0)
		long.append(0)


# Creates a dataframe containing the waiting times, latitude, and longitude of all open rides
df = pd.DataFrame(list(zip(wait, lat, long)), columns = ['Waiting Times', 'Latitude', 'Longitude'], index = name)

# Filters out and creates a dataframe containing only coordinates of the ride
coor = pd.DataFrame(list(zip(lat, long)), columns = ['Latitude', 'Longitude'], index = name)

# Filters out any rows that contains ride that are not listed on Google maps (lat and long of zero)
coor = coor.loc[~((df['Latitude'] == 0))] # Source: https://stackoverflow.com/questions/49841989/python-drop-value-0-row-in-specific-columns?answertab=active#tab-top

# Taken from: https://stackoverflow.com/questions/19413259/efficient-way-to-calculate-distance-matrix-given-latitude-and-longitude-data-in
# This function calculates the distance between two coordinates
def spherical_dist(pos1, pos2, r=3958.75):
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))

route = [] # Initialize list for optimal route
total_distance = 0 # Initilizes the total distance by setting it as 0

'''
Below is a loop to find the shortest distance via nearest neighbor.
We do this by first creating a distance matrix of all the distances to each other:
	-> Append the attraction name that has the smallest distance from the home location
	-> Remove that row
	-> Repeat the step until there is only 1 attraction remaining
	-> Append the last attraction to the route list

By doing this, it will ensure that no same attraction is visited.
'''

while len(coor) != 0: # Used nearest neighbor method to solve TSP problem
	route.append(ride) # Append the initial ride to the route list
	locations_1 = coor.values # Set the values within the dataframe as an array containing the coordinates
	home = coor.loc['%s' % (ride)].values # Sets the current nearest attraction as the home coordinates

	# Calls the spherical_dist function to calculate the distance between each coordinate and the home location
	dist = pd.DataFrame(list(zip(spherical_dist(locations_1[:, None], home))), index = coor.index, columns = ['Distance (mi)'])
	dist = dist.loc[~((dist['Distance (mi)'] == 0.0))]
	coor = coor.drop(ride, axis = 0)
	ride = dist.index[dist['Distance (mi)'].values.argmin()]
	home = coor.loc['%s' % (ride)].values
	total_distance += dist.values.min()[0]
	if len(coor) == 1:
		route.append(ride)
		break

# Initialize an empty list to append the final values of the coordinates in consecutive order as per the route
final_lat = list()
final_long = list()
# Creates an array containing the waiting times of each respected attraction in the optimized route
# Special thanks to: U9-Forward from StackOverflow:
# https://stackoverflow.com/questions/56178513/how-do-i-only-call-the-dictionary-value-within-a-list-if-it-meets-a-condition/56178554?noredirect=1#comment98983609_56178554
waiting = [d['wait'] for d in sorted(hpl, key=lambda x: ''.join(route).find(x['name'])) if d['name'] in route]

# Creates a list containing numbers from 1 to the very last order
order = np.arange(1, len(route) + 1)

# Used to append the values of the attractions in respect to the routes
for i in range(len(route)):
	final = geocoder.geocode('%s, Hershey Park Dr' % (route[i]))
	final_lat.append(final[0]['geometry']['lat'])
	final_long.append(final[0]['geometry']['lng'])

'''
Below are the codes used to graph the HersheyPark map via plotly:
	To start, please make sure you:
		1) Have an account registered in plotly (https://plot.ly/#/)
		2) Have an account registered in mapbox via plotly (https://account.mapbox.com/auth/signin/?route-to=https://studio.mapbox.com/)

'''

# Creates a dataframe that will be used to create the text in the plot
dataframe = pd.DataFrame(list(zip(route, order, waiting)), columns = ['Name', 'Order', 'Wait'])
dataframe['text'] = 'Order: ' + dataframe['Order'].astype(str) + '<br>Attraction: ' + dataframe['Name'].astype(str) + '<br>Waiting Time (min): ' + dataframe['Wait'].astype(str)

# Generates the data to be used for the scatter map plot in plotly:
data = [
    go.Scattermapbox(
        lat= final_lat,
        lon= final_long,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=11,
			color = 'rgb(255,0,0)', # Assigns the marker color as red
			opacity = 0.9
        ),
        text= dataframe['text'], # Creates a text containing each information listed before at every marker
    )
]

# Generates the layout for the map

layout = dict(
		title = 'Hershey Park Map<br>(Hover to View Details)',
		mapbox=go.layout.Mapbox(
			accesstoken=mapbox_access_token,
			bearing = 0,
			center = go.layout.mapbox.Center(
					lat=40.2888382, # Sets Hershey Park coordinates as the center point of the map
					lon=-76.6546074,
			),
			pitch = 0,
			zoom = 14),
		)


fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='Hershey Park Map') # This will open up a Plotly window in the browser with the plotted map

print('The suggested route is: %s' % (route)) # Prints the optimal route for the user
# Prints out the total accumulated distance taken by the route in the desired unit of measurement
print('The total distance for this trip is: %f %s' % (total_distance*unit, metric))
