from dbfread import DBF

count = 0
sites = []
print list(DBF('../ttms/ttms.dbf'))[0].keys()
for record in DBF('../ttms/ttms.dbf'):

	# print record.keys()
	# print record['LOCATION']
	# print record['SECTION_']
	# print record['Sitetype']
	# if 'YEAR_' in record:
	# 	print record['YEAR_']
	# print record['COMM']

	cosite = record['Cosite']
	if cosite[:2] == '75':
		# print record['YEAR_'], cosite
		print record.values()

	# count += 1
	# if count == 100:
	# 	break

