import shapefile

sf = shapefile.Reader("ttms.shp")

for shape in sf.iterShapes():
	print shape.points