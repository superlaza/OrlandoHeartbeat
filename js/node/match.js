// non-parallel
// 1092 devices, 645s, ~11mins
//

var turf = require('turf');
var Parallel = require('paralleljs');
var _ = require('lodash');
var jsonfile = require('jsonfile')

var roads = require('../../data/OrlandoStreetCenterlines/geojson/OrlandoStreetCenterlines.json');
var devices = require("../../data/Traffic/ptms/geojson/ptms.json");

road = roads.features[0];

var getClosestRoad = function(device){
	var min = 100000;
	var minLine;
	for (var i = roads.features.length - 1; i >= 0; i--) {
		var point = turf.pointOnLine(roads.features[i], device, {units: 'miles'});
		var dist = point.properties.dist;

		if (dist <= min) { min = dist; minLine = roads.features[i];}
	}

	// if (min < 1) {
	// 	console.log(min)
	// 	console.log(device.properties.COMM)
	// 	console.log(minLine.properties.StreetName)
	// 	console.log(device.properties)
	// 	console.log(minLine.properties)
	// 	console.log('\n\n')
	// }

	// var propKeys = 

	var year = device.properties.YEAR_;
	var traffic = [
		[year,
		{
			'TFCTR': device.properties['TFCTR'],
			'KFCTR': device.properties['KFCTR'],
			'DFCTR': device.properties['DFCTR'],
			'AADT': device.properties['AADT'],
		}]
	];
	var props = {
		'COMM': device.properties['COMM'],
		'Cosite': device.properties['Cosite']
	}

	var data = {
		'Traffic': traffic,
		'Device': props
	}
	return [min, minLine.properties.SegmentNum, data, minLine.properties.StreetName];
}

var matchedRoads = {};
var count = 0;
for (var i = devices.features.length - 1; i >= 0; i--) {
	var device = devices.features[i];

	if(device.properties.Cosite.substring(0,2) == '75'){
		
		var ret = getClosestRoad(device);
		var dist = ret[0];
		var SegmentNum = ret[1];
		var data = ret[2];
		var streetname = ret[3];

		if (dist < 1) {

			if (streetname in matchedRoads) {
				matchedRoads[streetname][SegmentNum] = data;
			}
			else{
				matchedRoads[streetname] = {};
				matchedRoads[streetname][SegmentNum] = data;
			}
		}

		count += 1;

		if (count % 100 == 0) {console.log(count)}
		// if (count == 5) {break}

	}
}
console.log(count)

var file = '../../data/processed/matched_road_segments.json'

jsonfile.writeFile(file, matchedRoads, function (err) {
  console.error(err)
})