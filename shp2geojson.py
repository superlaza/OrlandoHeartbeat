import shapefile
import datetime
from osgeo import osr
from json import dumps

def get_transform(prj_string):
	p1 = osr.SpatialReference()
	p1.ImportFromEPSG(4326)
	p2 = osr.SpatialReference()
	p2.ImportFromWkt(prj_string)
	return osr.CoordinateTransformation(p2, p1)

def toJSON(input_path, output_path):
	prj_string = open(input_path+'.prj', 'r').read()
	_transform = get_transform(prj_string)

	reader = shapefile.Reader(input_path)
	fields = reader.fields[1:]
	field_names = [field[0] for field in fields]
	_buffer = []
	for sr in reader.shapeRecords():
	   atr = dict(zip(field_names, sr.record))
	   geom = sr.shape.__geo_interface__
	   if isinstance(geom['coordinates'][0], tuple):
		   geom['coordinates'] = [_transform.TransformPoint(*coords) for coords in geom['coordinates']]
	   else:
		   geom['coordinates'] = _transform.TransformPoint(*geom['coordinates'])
	   atr = {k:v.strftime("%Y-%m-%d") if isinstance(v, datetime.date) else v for k,v in atr.items()}
	   d = dict(type="Feature", geometry=geom, properties=atr)
	   _buffer.append(d) 

	geojson = open(output_path, "w")
	geojson.write(dumps({"type": "FeatureCollection", "features": _buffer}, indent=2) + "\n")
	geojson.close()

toJSON("./data/OrlandoStreetCenterlines/shapefile/OrlandoStreetCenterlines",\
	   "./data/OrlandoStreetCenterlines/geojson/OrlandoStreetCenterlines.json")

toJSON("./data/Traffic/ptms/shapefile/ptms","./data/Traffic/ptms/geojson/ptms.json")