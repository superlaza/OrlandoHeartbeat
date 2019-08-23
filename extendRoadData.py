import json
from pprint import pprint
from collections import defaultdict
import numpy as np
import pandas as pd

allroads = json.load(open('./data/OrlandoStreetCenterlines/geojson/OrlandoStreetCenterlines.json', 'r'))
matchedroads = json.load(open('./data/processed/matched_road_segments.json', 'r'))

traffic_data = defaultdict(dict)
for feature in allroads['features']:
	streetname = feature['properties']['StreetName']
	segment = feature['properties']['SegmentNum']
	segment = unicode(str(segment), "utf-8") 

	if streetname in matchedroads:
		coords = feature['geometry']['coordinates']
		if segment in matchedroads[streetname]:
			traffic_data[streetname][segment] = [np.average(coords, axis=0), matchedroads[streetname][segment]['Traffic'][0][1]['AADT']]
		else:
			traffic_data[streetname][segment] = [np.average(coords, axis=0), np.nan]

# pprint(dict(traffic_data))

_max = -1
segmentData = {}
for streetname, data in traffic_data.items():
	std = np.std([datum[0] for datum in data.values()], axis=0)
	argmax = np.argmax(std)
	ordered = sorted(data.items(), key=lambda x:x[1][0][argmax])

	# print streetname
	series = pd.Series([o[1][1] for o in ordered])
	fvi = series.first_valid_index()
	lvi = series.last_valid_index()

	if fvi != 0:
		series[0] = 0.85*series[fvi]
	if lvi != series.size-1:
		series[series.size-1] = 0.85*series[lvi]

	interpolated = series.interpolate(method='akima').abs()

	interpolated.fillna(0, inplace=True)

	for i in range(len(ordered)):
		segment = ordered[i][0]
		segmentData[segment] = interpolated[i]

		if interpolated[i] > _max:
			_max = interpolated[i]

features = []
traffic_data = defaultdict(dict)
for feature in allroads['features']:
	streetname = feature['properties']['StreetName']
	segment = feature['properties']['SegmentNum']
	segment = unicode(str(segment), "utf-8") 

	if streetname in matchedroads:
		feature['properties'] = {
		'Traffic': float(segmentData[segment])
		}
		features.append(feature)

allroads['features'] = features
json.dump(allroads, open('test.json', 'wb'))

print 'max traffic', _max