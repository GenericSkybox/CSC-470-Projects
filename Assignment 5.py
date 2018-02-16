"""
# Name: Eric Ortiz
# Student Number: 102-39-903
# Date: 2/15/18
# Assignment #5
# Desc: This program renders non-polygonal objects using the ray tracing method via a recursive ray tracer already
        provided in class.
"""

from tkinter import *

# Here we're defining the window constants
CanvasWidth = 600
CanvasHeight = 600


# ***************************** Interface Functions ***************************
# Everything below this point implements the interface

def render():
    print("hi")


def quit():
    exit(0)


# ***************************** Interface and Window Construction ***************************
# Here we actually construct the base of the interface with tkinter
root = Tk()
outerframe = Frame(root)
outerframe.pack()

# Create the canvas on which we'll draw all of the objects
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()

# Create the control panel for the render and quit buttons
controlpanel = Frame(outerframe, borderwidth=2, relief=RIDGE)
controlpanel.pack(expand=True, fill=BOTH)

# Render Button Block
rendercontrols = Frame(controlpanel, height=100)
rendercontrols.pack(side=LEFT)

rendercontrolslabel = Label(rendercontrols, text="Render")
rendercontrolslabel.pack()

renderButton = Button(rendercontrols, text="GO!", fg="green", command=render)
renderButton.pack()

# Quit Button Block
quitcontrols = Frame(controlpanel, height=100)
quitcontrols.pack(side=RIGHT)

quitcontrolslabel = Label(quitcontrols, text="Quit")
quitcontrolslabel.pack()

quitButton = Button(quitcontrols, text="GET ME OUTTA HERE!!", fg="red", command=quit)
quitButton.pack()

root.mainloop()