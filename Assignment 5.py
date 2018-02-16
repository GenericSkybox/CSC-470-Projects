"""
# Name: Eric Ortiz
# Student Number: 102-39-903
# Date: 2/15/18
# Assignment #5
# Desc: This program renders non-polygonal objects using the ray tracing method via a recursive ray tracer already
        provided in class.
"""

from tkinter import *

CanvasWidth = 400
CanvasHeight = 400



root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()

root.mainloop()