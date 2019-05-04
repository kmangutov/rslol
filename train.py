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
from keras.layers import UpSampling2D, Dense,UpSampling2D, Activation, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization, Conv2DTranspose
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



flat = pixelsToArray(im)

print(str(flat))
print(str(bounds))
if False:
	img = ImageTk.PhotoImage(im)
	canvas = renderImage(img, 400, 400)
	for i in range(0, len(bounds)):#
		x1 = bounds[i].x1
		y1 = bounds[i].y1
		x2 = bounds[i].x2
		y2 = bounds[i].y2
		rect = canvas.create_rectangle( x1, y1, x2, y2, width = 5 )
	root.mainloop()

INPUT_SIZE = WINDOW_SIZE * WINDOW_SIZE * 3

model = Sequential()
#model.add(Dense(128, input_dim=INPUT_SIZE, kernel_initializer='glorot_normal'))
#model.add(Activation('relu'))
#model.add(Dense(64, kernel_initializer='glorot_normal'))
#model.add(Activation('relu'))
model.add(Conv2D(16, (4, 4), activation='relu', input_shape=(WINDOW_SIZE, WINDOW_SIZE, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(8, (2, 2), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Conv2D(64, (2, 2), activation='relu'))
#model.add(MaxPooling2D(pool_size=(2, 2)))

#model.add(UpSampling2D(size=(2, 2)))
#model.add(Conv2DTranspose(128, (2, 2)))
model.add(Flatten())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
#model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(UpSampling2D())
#model.add(Flatten())
#model.add(Conv2D(32, (3, 3), activation='relu'))
#model.add(Conv2D(32, (3, 3), activation='relu'))
#model.add(MaxPooling2D(pool_size=(2, 2)))


model.compile(loss='binary_crossentropy',
              optimizer='adam')

for i in range(0, 300):
	im, bounds = sample()

	#_input = np.asarray(pixelsToArray(im)).reshape(1,INPUT_SIZE)
	_input = np.asarray([pixelsToWHD(im)])
	#_output = np.asarray(createMask(bounds)).reshape(1,WINDOW_SIZE * WINDOW_SIZE)
	#_output = np.asarray([max(0, min(1, len(bounds)))])

	overlaparea = 0
	for b in range(0, len(bounds)):
		print('bound b : ' + str(bounds[b]))
		cut = Rect(max(bounds[b].x1, 0), max(bounds[b].y1, 0), min(bounds[b].x2, WINDOW_SIZE), min(bounds[b].y2, WINDOW_SIZE))
		overlap = cut.area() /  (WINDOW_SIZE * WINDOW_SIZE)
		overlaparea += overlap
		#overlaparea += bounds[b].overlap(Rect(0, 0, WINDOW_SIZE, WINDOW_SIZE))
		print('new overlap: ' + str(overlaparea))
	_output = np.asarray([overlaparea])

	print(str(len(_input)))
	print(_input.shape)
	print(', output: ' + str(_output))

	model.fit(_input, _output, batch_size=1, verbose=1, shuffle=False)
	model.save('checkpoints/model.h5')

#GOD BOUNDS (after scale) [41, 26, 858, 455],
#accounted for in image but not bounding box...