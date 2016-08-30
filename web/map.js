function initmap(){
	
	var map = L.map('mapid').setView([-6.816667, 39.283889], 12);
	
	var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
		attribution: '© OpenStreetMap contributors',
		maxZoom: 18,
		minZoom: 11
	});

	var otm = L.tileLayer('http://tile.opentopomap.org/{z}/{x}/{y}.png',{
		attribution: '© OpenStreetMap contributors',
		maxZoom: 14,
		minZoom: 11
	});

	var oepnv = L.tileLayer('http://tile.memomaps.de/tilegen/{z}/{x}/{y}.png',{
		attribution: '© OpenStreetMap contributors',
		maxZoom: 18,
		minZoom: 11
	});

	function bus_stops_popup(feature, layer){
		layer.bindPopup('Cluster-ID: ' + feature.properties.cluster_id
						+ '<br />Number of activities: ' + feature.properties.num_activity_points
						+ '<br />Distance to activities center: ' + feature.properties.distance_to_cluster + ' m'
						+ '<br />Snapped to: ' + feature.properties.snapped_to
		);
	}

	function circle_style(radius, fillColor='#999', color='#000'){
		var style = {
					radius: radius,
					fillColor: fillColor,
					color: color,
					weight: 1,
					opacity: 1,
					fillOpacity: 0.6
			}
		return style;
	};

	var bus_stops = new L.GeoJSON.AJAX("../data/bus_stops.geojson",{
		onEachFeature: bus_stops_popup,
		pointToLayer: function (feature, latlng) {
				if (feature.properties.num_activity_points < 3){
					radius = 6
				}
				else if (feature.properties.num_activity_points < 10){
					radius = 9
				}
				else {
					radius = 12
				}
				if (feature.properties.distance_to_cluster < 100){
					color = '#00ff00';
				}
				else if (feature.properties.distance_to_cluster < 400){
					color = '#c9ff00';
				}
				else if (feature.properties.distance_to_cluster < 700){
					color = '#ff7800';
				}
				else {
					color = '#ff0000';
				}
				return L.circleMarker(latlng, circle_style(radius,color));
			}
	});
	
	var routes = new L.GeoJSON.AJAX("../data/routes.geojson");
	var streets = new L.GeoJSON.AJAX("../data/osm_major_streets.geojson");
	var aps = new L.GeoJSON.AJAX("../data/activity_points.geojson");
	var overlayMaps = { "Bus Stops": bus_stops, "Bus Routes": routes, "Major Streets":streets, "Activity Points":aps };
	var baseMaps = { "OpenStreetMap": osm, "OpenTopoMap": otm, "ÖPNV Map": oepnv };
	
	oepnv.addTo(map);
	bus_stops.addTo(map);
	L.control.layers(baseMaps,overlayMaps,{collapsed:false}).addTo(map);
}
