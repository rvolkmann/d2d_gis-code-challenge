#!/usr/bin/python

""" CONFIG """

# Maximum time we want people to walk to the next bus stop
max_minutes = 10

# m/s (default=1.4 via Wikipedia)
walking_speed = 1.4 

# EPSG Code of the input GeoJSON and the valid metric coordinate system for the location
epsg_file = 'EPSG:4326'
epsg_metric = 'EPSG:32737'

""" """ """ """

import json
import fiona
from shapely.geometry import Point,LineString

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

# Load activity points geojson file
with fiona.open(activity_points_file, 'r') as activity_points:
	features = list(activity_points)

points = [trans(f['geometry']['coordinates'],epsg_file,epsg_metric) for f in features]

# Calculate the Maximum distance to walk to the next bus stop
max_distance = walking_speed * 60 * max_minutes

"""

Cluster the pointlist and
add the cluster information to the original features

"""
cluster = cluster_pointlist(points,max_distance)
for n,feature in enumerate(features):
	features[n]['properties']['cluster'] = int(cluster[n])

"""

Reorganize features to cluster id

"""
clusters = {}
for feature in features:
	if feature['properties']['cluster'] in clusters:
		clusters[feature['properties']['cluster']].append(feature)
	else:
		clusters[feature['properties']['cluster']] = [feature]

"""

Calculate weighted mean and create Bus Stops Feature-List

"""
cluster_centroids = []
for key, cluster in clusters.iteritems():
	xlist = [c['geometry']['coordinates'][0] for c in cluster]
	ylist = [c['geometry']['coordinates'][1] for c in cluster]
	xmean = sum(xlist)/float(len(xlist))
	ymean = sum(ylist)/float(len(ylist))
	cluster_centroid = {'type':'Feature','geometry':{'type': 'Point','coordinates':[xmean,ymean]},'properties':{'cluster_id':key, 'num_activity_points':len(cluster)}}
	cluster_centroids.append(cluster_centroid)

""" Snap Cluster Centroids to bus routes to find the bus stops

Shapely has a nice function to find the closest Point on a LineString.
The Following calculates the shortest distance to each Bus Route and then finds the closest one.

Todo:

* Improve performance by calculating only close Lines (some kind of geographic indexing needed)
* Don't snap by direct line, but by street routing

"""
# Load routes geojson file
with fiona.open(routes_file, 'r') as r:
	routes = list(r)

# Transform routes to metric coordinate system
transformed_routes = []
for route in routes:
	line = route['geometry']['coordinates']
	l = []
	for point in line:
		l.append(trans(point,epsg_file,epsg_metric))
	transformed_routes.append(LineString(l))

# Loop through the cluster centroids
bus_stops = []
for key,cluster_centroid in enumerate(cluster_centroids):
	# Create shapely point for bus stop
	p = Point(trans(cluster_centroid['geometry']['coordinates'],epsg_file,epsg_metric))
	# Calculate shortest distances to the transformed routes
	distances = []
	for l in transformed_routes:
		cpol = l.interpolate(l.project(p)) # cpol = closest point on line
		dist = p.distance(cpol)
		distances.append({'dist':dist,'cpol':cpol})
	# Find the closest route
	shortest_distance = min(distances, key=lambda k: k['dist'])
	cpol = shortest_distance['cpol']
	# Write bus stop
	bus_stop = cluster_centroid
	bus_stop['geometry']['coordinates'] = trans([cpol.x, cpol.y],epsg_metric,epsg_file)
	bus_stop['properties']['distance_to_cluster'] = int(shortest_distance['dist'])
	bus_stops.append(bus_stop)

"""

Write output

"""
with open("../data/activity_points_clusters.geojson", "w") as f:
	f.write(json.dumps({"type": "FeatureCollection","features": features}))

with open("../data/bus_stops.geojson", "w") as f:
	f.write(json.dumps({"type": "FeatureCollection","features": bus_stops}))
