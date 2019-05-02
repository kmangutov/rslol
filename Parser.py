import csv

def parse():
	images = []
	with open('data.csv', mode='r') as csv_file:
		reader = csv.reader(csv_file)
		
		for row in reader:
			_id = str(row[0])
			_rects = (len(row) - 1)/4

			images.append([row[1:]])

			print('id: ' + str(_id) + ', rects: ' + str(_rects))
	return images
