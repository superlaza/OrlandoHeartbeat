import shapefile
import datetime
from osgeo import osr

path = './data/geofabrik/'

prj_string = open(path+'osm_roads_free_1.prj', 'r').read()

p1 = osr.SpatialReference()
p1.ImportFromEPSG(4326)
p2 = osr.SpatialReference()
p2.ImportFromWkt(prj_string)
_transform = osr.CoordinateTransformation(p2, p1)

reader = shapefile.Reader(path+'osm_roads_free_1')
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
_buffer = []
for sr in reader.shapeRecords():
	print sr
	break
	if sr.record[4][:2] == '75' and sr.record[1] == 2016:
		atr = dict(zip(field_names, sr.record))
		geom = sr.shape.__geo_interface__
		geom['coordinates'] = _transform.TransformPoint(*geom['coordinates'])
		d = dict(type="Feature", geometry=geom, properties=atr)
		_buffer.append(d) 

from json import dumps
geojson = open("ttms.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": _buffer}, indent=2) + "\n")
geojson.close()