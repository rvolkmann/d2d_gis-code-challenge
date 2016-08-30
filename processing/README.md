# Description GIS-Code-Challenge Script

* Author: Rouven Volkmann
* Date: 2016/09/29

## Introduction

To locate preferred locations for bus stops, crowdfunded activity points are gathered and clustered.

The Script ...

1. clusters a point-set based on a maximum distance to each other,
2. calculates the weighted centroid for each cluster,
3. snaps the centroid to the given bus routes (= bus stops) and
4. shows the results in a web app.

## Processing

### Prerequisites

* Python
* Python modules: SciPy, fiona, pyproj

### Run processing

Run the following command:

```bash
python data/run.py
```

## Web app

After processing, you can look at the result in a web app.

Run a webserver pointing to the root folder of the repository.
With Python-integrated SimpleHTTPServer you can simply run following command from that folder:

```bash
python -m SimpleHTTPServer
```

Fire up your preffered browser and load http://localhost:8000/web

