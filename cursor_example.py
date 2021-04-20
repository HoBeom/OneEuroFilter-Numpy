# Code from https://stackoverflow.com/questions/42631060/draw-a-defined-size-circle-around-cursor-in-tkinter-python
import tkinter as tk
import numpy as np

import signal
from one_euro_filter import OneEuroFilter

global circle
global one_euro_filter
global start
circle = 0
circle_noisy = 0
min_cutoff = 0.07
beta = 0.0004
start = True

def motion(event):
    point = np.array([event.x + 3, event.y + 7])  
    #the addition is just to center the oval around the center of the mouse
    #remove the the +3 and +7 if you want to center it around the point of the mouse

    # add x, y random noise
    point_noisy = point + np.random.normal(scale=50, size=2)

    global start
    global one_euro_filter
    if start:
        one_euro_filter = OneEuroFilter(
            point_noisy,
            min_cutoff=min_cutoff,
            beta=beta
        )
        point_hat = point_noisy
        start = False
    else:
        point_hat = one_euro_filter(point_noisy)

    global circle
    global circle_noisy
    global canvas

    canvas.delete(circle)  #to refresh the circle each motion
    canvas.delete(circle_noisy)

    radius = 20  #change this for the size of your circle
    radius_noisy = 5

    x_max = point_hat[0] + radius
    x_min = point_hat[0] - radius
    y_max = point_hat[1] + radius
    y_min = point_hat[1] - radius

    circle = canvas.create_oval(x_max, y_max, x_min, y_min, outline="black")

    x_max = point_noisy[0] + radius_noisy
    x_min = point_noisy[0] - radius_noisy
    y_max = point_noisy[1] + radius_noisy
    y_min = point_noisy[1] - radius_noisy

    circle_noisy = canvas.create_oval(x_max, y_max, x_min, y_min, outline="red")

root = tk.Tk()
root.bind("<Motion>", motion)

global canvas

# https://stackoverflow.com/questions/40780634/tkinter-canvas-window-size
canvas = tk.Canvas(root, width=1200, height=800, background="bisque")
canvas.pack()

# code from https://stackoverflow.com/questions/39840815/exiting-a-tkinter-app-with-ctrl-c-and-catching-sigint/51525592
def handler(event):
    root.destroy()
    print('caught ^C')

def check():
    root.after(500, check)  #  time in ms.

# the or is a hack just because I've shoving all this in a lambda. setup before calling main loop
signal.signal(signal.SIGINT, lambda x,y : print('terminal ^C') or handler(None))

# this let's the terminal ^C get sampled every so often
root.after(500, check)  #  time in ms.

root.bind_all('<Control-c>', handler)

root.mainloop()