import csv

with open('data.csv', mode='r') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
    	_id = str(row[0])
    	_rects = (len(row) - 1)/4

    	print('id: ' + str(_id) + ', rects: ' + str(_rects))