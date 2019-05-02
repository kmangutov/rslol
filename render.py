from tkinter import *
#import PIL.Image
#import PIL.ImageTk
from PIL import Image
from PIL import ImageTk
from HoverInfo import HoverInfo
import sys
from Parser import parse

root = Toplevel()


index = 0

if len(sys.argv) > 1:
	index = sys.argv[1]
filename = "screenshots/" + str(index) + ".png"

im = Image.open(filename)
width, height = im.size
im = im.resize((int(width / 2.0), int(height / 2.0)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(im)


canvas = Canvas(root, width=1400, height=900)
canvas.pack()


canvas.create_image(0, 0, anchor=NW, image = photo)

#########render bounding boxes
images = parse()
boxes = images[0][0]

print('boxes:' + str(boxes))

for i in range(0, len(boxes), 4):
	x1 = boxes[i]
	y1 = boxes[i + 1]
	x2 = boxes[i + 2]
	y2 = boxes[i + 3]

	rect = canvas.create_rectangle( x1, y1, x2, y2, width = 5 )
#canvas.itemconfig(rect, tags='shp')
#########

root.mainloop()