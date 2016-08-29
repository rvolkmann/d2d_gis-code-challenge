#!/usr/bin/python

import json
import fiona

# Maximum time we want people to walk to the next bus stop
max_minutes = 10

# m/s (default=1.4 via Wikipedia)
walking_speed = 1.4 

# EPSG Code of the input GeoJSON and the valid metric coordinate system for the location
epsg_file = 'EPSG:4326'
epsg_metric = 'EPSG:32737'

def trans(coords,in_init,out_init):
	"""
	Transform coordinates using pyproj
	coordinates have to be of instance list or tuple
	"""
	from pyproj import Proj,transform
	p1 = Proj(init=in_init)
	p2 = Proj(init=out_init)
	return transform(p1,p2,coords[0],coords[1])

def cluster_pointlist(points,max_distance):
	"""
	Cluster a list or tuple of points by max_distance using scipy
	"""
	from scipy.cluster.hierarchy import linkage, fcluster
	import numpy as np
	X = np.array(points)
	Z = linkage(X, 'ward')
	return fcluster(Z, max_distance, criterion='distance')

activity_points_file = '../data/activity_points.geojson'
routes_file = '../data/routes.geojson'

with fiona.open(activity_points_file, 'r') as activity_points:
	features = list(activity_points)

points = [trans(f['geometry']['coordinates'],epsg_file,epsg_metric) for f in features]

# Calculate the Maximum distance to walk to the next bus stop
max_distance = walking_speed * 60 * max_minutes

# Cluster points and add the cluster information to the features
cluster = cluster_pointlist(points,max_distance)
for n,feature in enumerate(features):
	features[n]['properties']['cluster'] = int(cluster[n])

# Return weighted centroid of clusters
""" 
Needs to be written ...
"""

# Snap to bus routes
""" 
Needs to be written ...
"""

# Write output
with open("../data/activity_points_clusters.geojson", "w") as f:
	f.write(json.dumps({"type": "FeatureCollection","features": features}))

#with open("../data/bus_stops.geojson", "w") as f:
#	f.write(json.dumps({"type": "FeatureCollection","features": bus_stops}))
