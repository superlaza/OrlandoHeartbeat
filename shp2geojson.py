import shapefile
import datetime
from osgeo import osr

# Found in OrlandoStreetCenterlines folder, .prj
prj_string = 'PROJCS["NAD_1983_StatePlane_Florida_East_FIPS_0901_Feet",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199432955]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",656166.6666666665],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",-81],PARAMETER["Scale_Factor",0.9999411764705882],PARAMETER["Latitude_Of_Origin",24.33333333333333],UNIT["Foot_US",0.304800609601219241]]'

p1 = osr.SpatialReference()
p1.ImportFromEPSG(4326)
p2 = osr.SpatialReference()
p2.ImportFromWkt(prj_string)
_transform = osr.CoordinateTransformation(p2, p1)

reader = shapefile.Reader("./data/OrlandoStreetCenterlines/OrlandoStreetCenterlines")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
   atr = dict(zip(field_names, sr.record))
   geom = sr.shape.__geo_interface__
   geom['coordinates'] = [_transform.TransformPoint(*coords) for coords in geom['coordinates']]
   d = dict(type="Feature", geometry=geom, properties=atr)
   if isinstance(atr['MaintDate'], datetime.date):
	   atr['MaintDate'] = atr['MaintDate'].strftime("%Y-%m-%d")
   buffer.append(d) 

from json import dumps
geojson = open("OrlandoStreetCenterlines.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()