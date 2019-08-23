from dbfread import DBF

count = 0
sites = []

import shapefile
sf = shapefile.Reader("./data/Traffic/ptms/ptms")

shapes = sf.shapes()

print [field[0] for field in sf.fields]
for sr in sf.iterShapeRecords():
	if sr.record[4][:2] == '75':
		print sr.record
		break
		# print sr.shape.points
