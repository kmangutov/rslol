







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
WINDOW_SIZE = 128
X_WINDOWS = int(w / WINDOW_SIZE)
Y_WINDOWS = int(h / WINDOW_SIZE)
SLICES_PER_WINDOW = X_WINDOWS * Y_WINDOWS

print('xwindows ' + str(X_WINDOWS))
print('ywindows ' + str(Y_WINDOWS))
print('slices per window ' + str(SLICES_PER_WINDOW))

# pull random image slice and corresponding bounding box from images
def sample():
	#choose slice

	index = random.randint(0, int(23 * SLICES_PER_WINDOW))
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



root = Toplevel()
im, bounds = sample()

def pixelsToArray(im):
	pixels = np.asarray(im)
	flat = []
	for i in range(0, len(pixels)):
		for j in range(0, len(pixels[i])):
			flat.append(pixels[i][j][0])
			flat.append(pixels[i][j][1])
			flat.append(pixels[i][j][2])
	return flat

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

root = Toplevel()
im, bounds = sample()

prediction = model.predict(np.asarray(pixelsToArray(im)).reshape(1,49152))
print(str(prediction))