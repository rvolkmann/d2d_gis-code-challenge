# Door2Door GIS-Code-Challenge Script

* Author: Rouven Volkmann
* Date: August 30, 2016

## Processing

### Introduction

To locate preferred locations for bus stops, crowdfunded activity points are gathered, clustered by a maximum distance and snapped to the closest bus route or street.

**Clustering**

The script runs a hierarchical clustering algorithm (Ward) on the pointset based on a maximum walking distance.
Then the weighted centroid of each cluster is calculated to receive the activity hot-spots.

**Snapping**

Bus stops are preferred along established bus routes. Therefore the script tries to snap to the closest bus route. It might be suitable to start a new route if the established ones are too far and enough activities are recorded. Then, the script decides to snap to the next major street instead on which the new bus route might run.

The street data was downloaded from OpenStreetMap (highway=trunk|primary|secondary|tertiary) on August 30, 2016.



### Run the script

**Prerequisites**

* Python
* Python modules: SciPy, fiona, pyproj

Run the following command:

```bash
python data/run.py
```

## Web app

After processing, you can view the result in a web app.

Run a webserver pointing to the root folder of the repository.
With Python-integrated SimpleHTTPServer you can simply run following command from that folder:

```bash
python -m SimpleHTTPServer
```

Fire up your preffered browser and load http://localhost:8000/web

## Todo

Several things should be done to improve the script further

* merge close-by bus stops
* snap by street routing instead of direct line
* having more activity data, the data could be filtered by their reliability and other attributes

