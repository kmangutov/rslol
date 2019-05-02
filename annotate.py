from tkinter import *
#import PIL.Image
#import PIL.ImageTk
from PIL import Image
from PIL import ImageTk
from HoverInfo import HoverInfo
import sys

root = Toplevel()

filename = "screenshots/5.png"
if len(sys.argv) > 1:
	filename = sys.argv[1]

im = Image.open(filename)
width, height = im.size
im = im.resize((int(width / 2.0), int(height / 2.0)), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(im)


canvas = Canvas(root, width=1400, height=900)
canvas.pack()


canvas.create_image(0, 0, anchor=NW, image = photo)

#label = Label(root, image=photo)
#label.image = photo  # keep a reference!
#label.hover = HoverInfo(root, '(55, 56)')
#label.pack()

x1 = 0
y1 = 0
x2 = 0 
y2 = 0
rect = 0

rects = []

def paint( event ):
	python_green = "#cccccc"
   
	global x1
	global y1
	global x2
	global y2

	if x1 == 0 or y1 == 0:
		x1, y1 = event.x, event.y
	x2, y2 = event.x, event.y

	global rect
	if rect != 0:
		canvas.delete(rect)
	rect = canvas.create_rectangle( x1, y1, x2, y2, width = 5 )
	canvas.itemconfig(rect, tags='shp')

def release(event):
	global x1
	global y1
	global x2
	global y2

	values = [x1, y1, x2, y2]
	rects.append(values)
	_rect = canvas.create_rectangle( x1, y1, x2, y2, width = 5 )
	print(str(values) + ",")


	x1 = 0
	y1 = 0
	x2 = 0 
	y2 = 0


canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", release)




root.mainloop()