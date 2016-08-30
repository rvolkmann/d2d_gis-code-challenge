# Description GIS-Code-Challenge Script

* Author: Rouven Volkmann
* Date: 2016/09/30

## Processing

### Introduction

To locate preferred locations for bus stops, crowdfunded activity points are gathered, clustered by a maximum distance and snapped to the next bus route or street.

**Clustering**

The script runs a hierarchical clustering algorithm (Ward) on the pointset based on a maximum walking distance.
Then the weighted centroids of the clusters are calculated to receive the activity hot-spots.

**Snapping**

Bus stops are preferred along established bus routes. Therefore the script tries to snap to the next bus route. It might be suitable to start a new bus route if the bus route is too far and there are enough activities recorded. Then, the script decides to snap to the next major street instead on which the new bus route might run.

The street data is downloaded from OpenStreetMap (highway=trunk|primary|secondary|tertiary).

### Prerequisites

* Python
* Python modules: SciPy, fiona, pyproj

### Run the script

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

