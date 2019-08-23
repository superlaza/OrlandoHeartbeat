import shapefile
import datetime
from osgeo import osr

reader1 = shapefile.Reader("./data/OrlandoStreetCenterlines/OrlandoStreetCenterlines")
reader2 = shapefile.Reader("./data/Traffic/ptms/ptms")

for sr2 in reader2.shapeRecords():
	if sr2.record[4][:2] == '75' and sr2.record[1] == 2016:
		for sr1 in reader1.shapeRecords():
			
			geom1 = sr1.shape.__geo_interface__
			geom2 = sr2.shape.__geo_interface__