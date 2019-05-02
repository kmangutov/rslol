import csv

def parse():
	with open('data.csv', mode='r') as csv_file:
		reader = csv.reader(csv_file)
		images = []
		for row in reader:
			_id = str(row[0])
			_rects = (len(row) - 1)/4

			images.append([_rects[1:]])

			print('id: ' + str(_id) + ', rects: ' + str(_rects))
		return images
