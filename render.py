from tkinter import *
#import PIL.Image
#import PIL.ImageTk
from PIL import Image
from PIL import ImageTk
from HoverInfo import HoverInfo
import sys
from Parser import parse

from Rect import Rect

index = 0
if len(sys.argv) > 1:
	index = sys.argv[1]

def renderImage(root, photo, w, h):
	canvas = Canvas(root, width=w, height=h)
	canvas.pack()
	canvas.create_image(0, 0, anchor=NW, image = photo)
	return canvas


def loadImage(id):
	filename = "screenshots/" + str(id) + ".png"

	im = Image.open(filename)
	width, height = im.size
	im = im.resize((int(width / 2.0), int(height / 2.0)), Image.ANTIALIAS)
	im = im.crop((41, 26, 858, 455))
	photo = ImageTk.PhotoImage(im)

	return photo

def loadImage2(id, x1, y1, x2, y2):
	filename = "screenshots/" + str(id) + ".png"

	im = Image.open(filename)
	width, height = im.size
	im = im.resize((int(width / 2.0), int(height / 2.0)), Image.ANTIALIAS)
	im = im.crop((41, 26, 858, 455))
	im = im.crop((x1, y1, x2, y2))
	return im

def imageSize():
	filename = "screenshots/0.png"

	im = Image.open(filename)
	width, height = im.size
	im = im.resize((int(width / 2.0), int(height / 2.0)), Image.ANTIALIAS)
	im = im.crop((41, 26, 858, 455))
	return im.size

_images = parse()
def loadBoxes(id):
	global _images
	return _images[id][0]


if __name__ == '__main__':

	root = Toplevel()

	photo = loadImage(14)
	canvas = renderImage(photo, 800, 800)
	boxes = loadBoxes(14)
	print('boxes: ' + str(boxes))

	for i in range(0, len(boxes), 4):#
		x1 = boxes[i]
		y1 = boxes[i + 1]
		x2 = boxes[i + 2]
		y2 = boxes[i + 3]

		rect = Rect(x1, y1, x2, y2)
		rect.shift(-41, -26)
		canvas.create_rectangle( rect.x1, rect.y1, rect.x2, rect.y2, width = 5 )



	root.mainloop()

#canvas = Canvas(root, width=1400, height=900)
#canvas.pack()

#photo = loadImage(index)
#canvas.create_image(0, 0, anchor=NW, image = photo)

#boxes = loadBoxes(index)


#for i in range(0, len(boxes), 4):#
#	x1 = boxes[i]
#	y1 = boxes[i + 1]
#	x2 = boxes[i + 2]
#	y2 = boxes[i + 3]

#	rect = canvas.create_rectangle( x1, y1, x2, y2, width = 5 )
#canvas.itemconfig(rect, tags='shp')
#########

#root.mainloop()
#GOD BOUNDS (after scale) [41, 26, 858, 455],