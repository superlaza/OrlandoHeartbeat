import shapefile
sf = shapefile.Reader("./data/OrlandoStreetCenterlines/OrlandoStreetCenterlines")

shapes = sf.shapes()

print [field[0] for field in sf.fields]
for sr in sf.iterShapeRecords():
	print sr.record
	print dir(sr.shape)
	print sr.shape.shapeType
	print sr.shape.points
	break