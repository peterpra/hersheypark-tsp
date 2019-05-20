# **Traveling Salesman Problem in Hershey Park**

Authors: *Brandon Buesching, Peter Pranata*

YouTube Video Link:
<br>https://www.youtube.com/watch?v=kcP7aa7PCj4&feature=youtu.be

### **BACKGROUND**
Amusement parks are expensive. The average cost of a standard single-day ticket for major amusement parks within the United States is around $89 [1]. When guests spend this amount of money for entertainment, they expect a certain level of quality to justify the purchase. A guest's perceived quality of an amusement park is significantly impacted by the amount that they are able to accomplish on the day of their visit. There exist three pieces of information that are imperative for amusement park guests: the distance between them and their favorite rides, the current wait times at their favorite rides, and an easy-to-understand map of the park. Amusement parks have largely neglected to provide their guests with a comprehensive tool that conveniently includes each of these features.

### **PROJECT OBJECTIVE**
Hershey Park is a family-themed amusement park located in Hershey, Pennsylvania. As a top-tier vacation destination, it is imperative that Hershey Park provides a tool that incorporates the three features previously listed (distance between current guest location and park rides, live wait times at park rides, and aesthetically-pleasing graphic that includes live wait times). This project seeks to create an algorithm that provides such a tool for Hershey Park's customers. 

### **REQUIREMENTS**
* ```amusement``` 

Go to the command line window and type "pip install amusement".

* ```numpy```

Go to the command line window and type "pip install numpy".

* ```pandas```

Go to the command line window and type "pip install pandas".

* ```mapbox``` (_Account creation and API key required_)

You will also need to create an account and obtain an API key from mapbox. Visit https://plot.ly/, go to Settings, hover over your user icon, then click "Mapbox Access tokens" on the left banner. Next, register for an online mapbox account. In the upper right corner, click on your account icon. Next, scroll down until you see "Access Tokens". Copy the default access token and paste it in the "Add a New Access Token" box in plotly. Click "Add Token". 
* ```opencage``` (_API key required_)

Go to the command line window and type "pip install opencage". You will also need to create an account and obtain an API key. Visit opencagedata.com and register by providing the following information: name, company/organization, email address, and password. Click on "API" in the top banner and you will be linked to a screen displaying your API.

* ```plotly``` (_Account creation and API key required_)

Go to the command line window and type "pip install plotly". You will need to create an account in order to use plotly. Registration requires the following information: name, company/organization, role, email address, username, and password. Visit https://plot.ly/ and hover over your username in the top right corner of the screen. Click "Settings" and then press "API Key" on the left banner to obtain your API key. 

### **UNIQUE FEATURES**
* Distance converter
<br>The distance converter allows guests to toggle between units of distance - standard (feet) and metric (meter). 

* No repeated rides 
<br>This program assumes that guests want to maximize the number of unique rides that they visit during the day, so subtour elimination was imposed by removing previously-visited rides from the dataframe. </br>
* Zoomable map 
<br>The map showing the TSP-routes are interactive; guests can zoom in and out to obtain their desired map resolution. This is a built-in feature of plotly which increases the appeal of the tool.

### **HOW TO RUN THE CODE**
1. Make sure that you have the API and Access Token keys for OpenCage, Plotly, and Map Box (through Plotly).
2. Make sure all necessary packages are installed.
3. Open a terminal window.
4. Change directory to where the 'amusement_project.py' is saved.
5. Type the following command: ```python amusement_project.py```
6. Answer any prompt that arises.

### **ANALYSIS**
*Note: This is a concise analysis of the code. A more-detailed analysis is presented in the Youtube Link provided.*

As previously described, this project provides guests with a suggested ride sequence that minimizes the total travel distance. The algorithm, more specifically, was derived using the "nearest neighbor" approach. When the user selects the run option, he/she is presented with a myriad of "raw" data, shown below. This is a list of many dictionaries that have been called from the ```amusement``` API. This data was used to generate ride names and wait times. The data shown below is a partial of the entire data source taken from the API.

```
[{'name': 'Carrousel', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Balloon Flite', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Skyrush', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'sooperdooperLooper',
  'wait': 0,
  'isOpen': False,
  'single_rider': None},
 {'name': 'Fahrenheit', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Scrambler', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Coal Cracker', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Cocoa Cruiser', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Comet', 'wait': 0, 'isOpen': False, 'single_rider': None},
 {'name': 'Convoy', 'wait': 0, 'isOpen': False, 'single_rider': None},
```
After the raw data has been displayed, the user will be prompted to enter his starting location. This is the ride that is closest to his current location. In this example, he inputs "Skyrush". The user is also prompted to enter his preferred unit of measurement, which is an additional unique feature of this algorithm. In this case, he inputs "Meters".
```
What is your starting location?
Please insert the name of the closest attraction: Skyrush

What unit of measurement do you prefer? (Meters or Feet): Meters
```
After these inputs are entered, the suggested route is displayed to the user, as well as the total distance required to complete the sequence. In this case, "Comet" is the closest ride to "Skyrush", "sooperdooperLooper" is the closest ride to "Comet", and so on. We generate this suggested route using a while loop as a method to convey the nearest neighbor heuristic for the travelling salesmen problem:
```
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
```
As you can see, the code basically appends the value of home as the 1st position and broadcasts the distances to each of the rides into an array. Afterwards, the ride with the minimum distance is set to as the next home location, while the row of the previous home location is removed. From here, the method is repeated until only 1 row is left, which represents the last attraction the customer should visit in the heuristic. 

<br>We speciffically took a function from Stackoverflow for the calculation of distances between coordinates. More specifically, the code is:
```
def spherical_dist(pos1, pos2, r=3958.75):
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))
 ```
 As you can see, this code calculates a distance in miles for two coordinates or more. Since we set pos1 as the home location (1 coordinate) while pos2 as the destination coordinate (n-array), it will create a distance matrix that shows the distance from home to each of the destinations, with the distance being 0 for home to home. 
 
<br>Overall, the name of the attraction that generates the least distance at each iteration will be appended to: ```route = []```

The total distance for the suggested sequence is also displayed to the user, as shown below:
```
The suggested route is: ['Skyrush', 'Comet', 'Carrousel', 'sooperdooperLooper', 'Great Bear', 'Coal Cracker', 'Kissing Tower', 'Monorail ', 'Trailblazer', 'Storm Runner', 'Sidewinder', 'Pirate', 'The Claw', 'Fahrenheit', 'Tidal Force', 'Wild Mouse', 'Laff Trakk', 'Wildcat', 'Lightning Racer']

The total distance for this trip is: 2139.858683 Meters 
```
Finally, a map will be displayed that plots the ride locations, ride coordinates, order within the suggested sequence assigned to each ride, and current wait times of each ride. This information will be available to the user when he hovers his mouse over each plotted circle. The color of the plotted locations was changed to red for easier identification. The plot given the current example is displayed below:

<a href="https://ibb.co/gPD4GVF"><img src="https://i.ibb.co/s6FWhHJ/picture.png" alt="picture" border="0"></a>

Based on the suggested ride sequence (with accompanying total distance) and map (with accompanying coordinates, sequence order, and wait times), the user can be better informed of a near-optimal sequence of rides to visit while at Hershey Park.

### **LIMITATIONS**
*  Ride location accuracy 

The accuracy of the algorithm is dependent upon the precision of the geocoordinates stored within Google Maps. The opencage.geocoder API was used to collect the geocordinates of each of the rides within Hershey Park. If one of the geocoordinates is incorrect (even by a seemingly insignificant amount), then the program's output (suggestion for the next ride to visit) may be a poor recommendation. 
*  Limited usage

Secondly, the algorithm will only function if Hershey Park is open. This makes intuitive sense, as wait times will only exist when the park is open and guests are waiting on line. For the purposes of academic research, however, the algorithm cannot be run outside of normal park hours.

### **OBSTACLES**
* Publicly-accessible amusement park ride wait time API

One of the major challenges encountered in the creation of this program was the availability of a publically-accessible amusement park ride wait time API. The original intent was to develop this routing tool for Disney World, however, it became clear that the wait times were not publicly available online from Disney World itself. While a third-party API claimed to have this data available, accessibility required an API key. No instructions were provided by the third-party as to how to obtain the key.

* Park hours vs. debugging 

This project was unique in the fact that debugging was limited to the hours in which Hershey Park was open and its rides were operating. Hershey Park's rides are currently only open on weekends and there were several weekends in which the park was closed due to stormy weather. This limited the amount of time available for debugging. Because of this constraint, we actually made a dummy list that contains less data but formatted in the same way with the actual raw data. This is our dummy list:
```
status = [{'name': 'Carrousel', 'wait': 0, 'isOpen': True, 'single_rider': None},
{'name': 'Balloon Flite', 'wait': 0, 'isOpen': True, 'single_rider': None},
{'name': 'Skyrush', 'wait': 0, 'isOpen': False, 'single_rider': None},
{'name': 'SooperDooperLooper','wait': 5, 'isOpen': True,'single_rider': None},
{'name': 'Fahrenheit', 'wait': 20, 'isOpen': True, 'single_rider': None},
{'name': 'Dummy', 'wait': 0, 'isOpen': False, 'single_rider': None}]
```
As you can see, the format is the same but it is just smaller and contains some different information so that we can develop our code. ```status``` was used throughout the course of our project since it was faster, and easier to run for debugging purposes.

### **FURTHER STUDY**
In the future, the algorithm developed within this project can be applied to other amusement parks. The successful implementation of the algorithm into other parks is dependent upon two conditions: the accessibity of ride geocoordinates (callable from the Google Maps API, a .csv file [in which case the geocoordinates are fixed points], or some other source) and the accessibility of ride wait times. The latter condition is far more constraining; unless the amusement park publicly displays ride wait times on its mobile app or website, it may not be possible for an external party to obtain this information in developing this algorithm. Endless opportunities abound for the operators of amusement parks, however. Using this project's algorithm as a template, amusement park operators can easily develop a Traveling Salesman Problem algorithm (and perhaps make it accessible through a mobile app) for routing guests from ride to ride based on current location.

Furthermore, the algorithm developed within this project could also be used for non-guest related purposes. For example, the park operators could use this algorithm to minimize the distance required for brochure distribution, cleaning services, maintenance checks, security patrols, and so on. This could ultimately decrease worker fatigue, increase worker morale, and boost productivity.

Future work involving the algorithm developed within this project could incorporate ride wait times into the objective function. Given the complexity of the Traveling Salesman Problem, it was was challenging to incorporate a weighted objective function (distance and ride wait times). A future modification, however, could entail the inclusion of wait times into the objective function along with the distances to each ride.


### **REFERENCES**
[1] https://www.nasdaq.com/article/what-are-the-ticket-prices-for-us-theme-parks-cm528910 
<br>[2] https://stackoverflow.com/questions/49841989/python-drop-value-0-row-in-specific-columns?answertab=active#tab-top
<br>[3] https://stackoverflow.com/questions/19413259/efficient-way-to-calculate-distance-matrix-given-latitude-and-longitude-data-in
<br>[4] https://stackoverflow.com/questions/56178513/how-do-i-only-call-the-dictionary-value-within-a-list-if-it-meets-a-condition/56178554?noredirect=1#comment98983609_56178554
<br>[5] https://plot.ly/python/scattermapbox/


