







from render import loadImage, loadBoxes, imageSize, loadImage2, renderImage

from tkinter import *
from PIL import Image
from PIL import ImageTk
import random
from Rect import Rect
from PIL import ImageFilter
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from keras.models import load_model


w, h = imageSize()
WINDOW_SIZE = 64
X_WINDOWS = int(w / WINDOW_SIZE)
Y_WINDOWS = int(h / WINDOW_SIZE)
SLICES_PER_WINDOW = X_WINDOWS * Y_WINDOWS

print('xwindows ' + str(X_WINDOWS))
print('ywindows ' + str(Y_WINDOWS))
print('slices per window ' + str(SLICES_PER_WINDOW))

# pull random image slice and corresponding bounding box from images
ii = 0
def sample():
	#choose slice
	global ii
	index = ii#random.randint(0, int(23 * SLICES_PER_WINDOW))
	ii = ii + 1

	imageIndex = int(index / SLICES_PER_WINDOW)
	sliceIndex = index % SLICES_PER_WINDOW
	sliceX = int(sliceIndex % X_WINDOWS)
	sliceY = int(sliceIndex / X_WINDOWS)

	print('index ' + str(index) + ', imageIndex ' + str(imageIndex) + ', sliceX ' + str(sliceX) + ', sliceY ' + str(sliceY))

	x1 = int(sliceX * WINDOW_SIZE)
	y1 = int(sliceY * WINDOW_SIZE)
	x2 = int(x1 + WINDOW_SIZE)
	y2 = int(y1 + WINDOW_SIZE)
	sliceRect = Rect(x1, y1, x2, y2)

	print(str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2))

	_slice = loadImage2(imageIndex, x1, y1, x2, y2)
	#renderImage(_slice, WINDOW_SIZE, WINDOW_SIZE)

	boxes = loadBoxes(imageIndex)
	bounds = []
	for i in range(0, len(boxes), 4):
		rect = Rect(boxes[i], boxes[i + 1], boxes[i + 2], boxes[i + 3])
		rect.shift(-41, -26)

		print ('check ' + str(rect))
		if (rect.intersects(sliceRect)):
			print('INTERSECT !!!!!!!! ' + str(rect))
			rect.shift(-1 * x1, -1 * y1)
			#rect.bound(0, 0, WINDOW_SIZE, WINDOW_SIZE)
			bounds.append(rect)

	return _slice, bounds

#######################



def pixelsToArray(im):
	pixels = np.asarray(im)
	r = []
	g = []
	b = []
	for i in range(0, len(pixels)):
		for j in range(0, len(pixels[i])):
			r.append(pixels[i][j][0])
			g.append(pixels[i][j][1])
			b.append(pixels[i][j][2])
	return r + g + b

def pixelsToWHD(im):
	pixels = np.asarray(im)
	arr = []
	for i in range(0, len(pixels)):
		h = []
		for j in range(0, len(pixels[i])):
			d = pixels[i][j][0:3]
			#d = [pixels[i][j][1]]
			h.append(d)
		arr.append(h)
	return arr


def createMask(bounds):
	arr = []
	for i in range(0, WINDOW_SIZE * WINDOW_SIZE):
		x = int(i / WINDOW_SIZE)
		y = i % WINDOW_SIZE

		hit = False
		for j in range(0, len(bounds)):
			if bounds[j].x1 < x and bounds[j].y1 < y and bounds[j].x2 > x and bounds[j].y2 > y:
				hit = True

		if hit:
			arr.append(1)
		else:
			arr.append(0)
	return arr


model = load_model('checkpoints/model.h5')

images = []

for s in range(0, 5):

	root = Toplevel()
	canvas = Canvas(root, width=WINDOW_SIZE * 3, height=WINDOW_SIZE * 12)
	canvas.pack()

	for k in range(0, 12):
		im, bounds = sample()

		inp = np.asarray([pixelsToWHD(im)])
		#print('input: ' + str(inp))

		prediction = model.predict(inp)#.reshape(1,WINDOW_SIZE * WINDOW_SIZE * 3))
		#prediction = model.predict(np.asarray([pixelsToArray(im)]))#.reshape(1,WINDOW_SIZE * WINDOW_SIZE * 3))
		
		print(str(prediction))

		image = ImageTk.PhotoImage(im)
		images.append(image)
		canvas.create_image(0, k * WINDOW_SIZE, anchor=NW, image = image)

		val = int(9 * prediction[0][0])
		color = '#' + str(val) + str(val) + str(val)
		canvas.create_rectangle(WINDOW_SIZE, k * WINDOW_SIZE, WINDOW_SIZE + WINDOW_SIZE, k * WINDOW_SIZE + WINDOW_SIZE, width=0, fill=color)
		#for i in range(0, len(prediction[0])):
	#		x = WINDOW_SIZE + int(i / WINDOW_SIZE)
	#		y = i % WINDOW_SIZE + k * WINDOW_SIZE
	#		val = int(9 * float(prediction[0][i]))
	#		val = max(0, val)
	#		color = '#' + str(val) + str(val) + str(val)
	#		canvas.create_rectangle(x, y, x, y, width=0, fill=color)

		mask = createMask(bounds)

		for i in range(0, len(mask)):
			x = WINDOW_SIZE * 2 + int(i / WINDOW_SIZE)
			y = i % WINDOW_SIZE + k * WINDOW_SIZE
			val = int(mask[i])
			if val == 0:
				color = '#000'
			else:
				color = '#fff'
			canvas.create_rectangle(x, y, x, y, width=0, fill=color)



root.mainloop()