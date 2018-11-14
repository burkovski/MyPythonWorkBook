"""
рисует окружности на холсте
"""

import math
import sys
from tkinter import *


def point(tick, range, radius):
    angle = tick * (360 / range)
    radians_per_degree = math.pi / 180
    point_x = int(round(radius * math.sin(angle * radians_per_degree)))
    point_y = int(round(radius * math.cos(angle * radians_per_degree)))
    return point_x, point_y


def circle(canvas, points, radius, center_x, center_y, slow=0):
    canvas.delete("lines")
    canvas.delete("points")
    for i in range(points):
        x, y = point(i+1, points, radius-4)
        scaled_x, scaled_y = (center_x + x), (center_y - y)
        canvas.create_line(center_x, center_y, scaled_x, scaled_y, tag="lines")
        canvas.create_rectangle(scaled_x-2, scaled_y-2, scaled_x+2, scaled_y+2, fill="red", tag="points")
        if slow: canvas.update()


def plotter(canvas, scale_var, check_var, width, origin_x, origin_y):
    circle(canvas, scale_var.get(), (width // 2), origin_x, origin_y, check_var.get())


def make_widgets(root, width, origin_x, origin_y):
    canvas = Canvas(root, width=width, height=width)
    canvas.pack(side=TOP)
    scale_var = IntVar()
    scale_var.set(120)
    check_var = IntVar()
    scale = Scale(root, label="Points on circle", variable=scale_var, from_=1, to=360)
    scale.pack(side=LEFT)
    Checkbutton(root, text="Slow mode", variable=check_var).pack(side=LEFT)
    Button(root, text="Plot", command=lambda: plotter(canvas, scale_var, check_var,
                                                      width, origin_x, origin_y)).pack(side=LEFT, padx=50)

def launcher():
    root = Tk()
    if len(sys.argv) == 2:
        width = int(sys.argv[1])
    else:
        width = 500
    origin_x = origin_y = width // 2
    make_widgets(root, width, origin_x, origin_y)
    root.mainloop()


if __name__ == "__main__":
    launcher()