"""
# Name: Eric Ortiz
# Student Number: 102-39-903
# Date: 12/19/17
# Assignment #1
# Desc: This program is a basic graphics engine that can display a 3D pyramid on a 2D coordinate plane. There are
        a handful of tools also provided that allow the user to translate, scale, and rotation the pyramid -- along
        with a reset button.
"""

import math
from tkinter import *

CanvasWidth = 400
CanvasHeight = 400
d = 500

# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
apex = [0,50,100]
base1 = [-50,-50,50]
base2 = [50,-50,50]
base3 = [50,-50,150]
base4 = [-50,-50,150]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in counter clockwise order when viewed from the outside
frontpoly = [apex,base1,base2]
rightpoly = [apex,base2,base3]
backpoly = [apex,base3,base4]
leftpoly = [apex,base4,base1]
bottompoly = [base4,base3,base2,base1]

# Definition of the object
Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
PyramidPointCloud = [apex, base1, base2, base3, base4]
#************************************************************************************

# This function resets the pyramid to its original size and location in 3D space
# Note that shortcuts like "apex = [0,50,100]" will not work as they build new
# structures rather than modifying the existing Pyramid / PyramidPointCloud
def resetPyramid():
    # grab the global variables of Pyramid and its point cloud
    global Pyramid
    global PyramidPointCloud

    # recreate the original points of the triangle
    apex = [0, 50, 100]
    base1 = [-50, -50, 50]
    base2 = [50, -50, 50]
    base3 = [50, -50, 150]
    base4 = [-50, -50, 150]

    # organize these points into their respective polygons
    frontpoly = [apex, base1, base2]
    rightpoly = [apex, base2, base3]
    backpoly = [apex, base3, base4]
    leftpoly = [apex, base4, base1]
    bottompoly = [base4, base3, base2, base1]

    # reset the pyramid and point cloud with the new polys
    Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]
    PyramidPointCloud = [apex, base1, base2, base3, base4]

    print("resetPyramid stub executed.")

# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    # iterate through the points in the object
    for i in range(len(object)):
        point = object[i]
        # for every point, add each component with that of the displacement component
        for j in range(len(point)):
            point[j] += displacement[j]

    print("translate stub executed.")
    
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object,scalefactor):
    # iterate through the points in the object
    for i in range(len(object)):
        point = object[i]
        # for every point, multiply each component by the scalefactor
        for j in range(len(point)):
            point[j] *= scalefactor

    print("scale stub executed.")

# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard position]
def rotateZ(object,degrees):
    # first convert the degrees to radians
    radians = math.radians(degrees)

    # iterate through the polygons in the object and grab each point
    for i in range(len(object)):
        point = object[i]
        # so that the points don't get manipulated during computation, assign the x and y values separately
        x = point[0]
        y = point[1]
        # use the z-rotation function
        point[0] = (x * math.cos(radians)) - (y * math.sin(radians))
        point[1] = (x * math.sin(radians)) + (y * math.cos(radians))

    print("rotateZ stub executed.")
    
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object,degrees):
    # first convert the degrees to radians
    radians = math.radians(degrees)

    # iterate through the polygons in the object and grab each point
    for i in range(len(object)):
        point = object[i]
        # so that the points don't get manipulated during computation, assign the x and z values separately
        x = point[0]
        z = point[2]
        # use the y-rotation function
        point[0] = (x * math.cos(radians)) + (z * math.sin(radians))
        point[2] = (-1 * (x * math.sin(radians))) + (z * math.cos(radians))

    print("rotateY stub executed.")

# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object,degrees):
    # first convert the degrees to radians
    radians = math.radians(degrees)

    # iterate through the polygons in the object and grab each point
    for i in range(len(object)):
        point = object[i]
        # so that the points don't get manipulated during computation, assign the y and z values separately
        y = point[1]
        z = point[2]
        # use the x-rotation function
        point[1] = (y * math.cos(radians)) - (z * math.sin(radians))
        point[2] = (y * math.sin(radians)) + (z * math.cos(radians))

    print("rotateX stub executed.")

# The function will draw an object by repeatedly calling drawPoly on each polygon in the object
def drawObject(object):
    for i in range(len(object)):
        drawPoly(object[i])
    print("drawObject stub executed.")

# This function will draw a polygon by repeatedly calling drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly):
    for i in range(len(poly)):
        drawLine(poly[i-1], poly[i])
    print("drawPoly stub executed.")

# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(start,end):
    # first convert the given start and end points to their perspective projection
    startproject = project(start)
    endproject = project(end)

    # then displace the projection points so that the center of the canvas is the origin
    startdisplay = convertToDisplayCoordinates(startproject)
    enddisplay = convertToDisplayCoordinates(endproject)

    # draw the line with the new canvas-centered points
    w.create_line(startdisplay[0],startdisplay[1],enddisplay[0],enddisplay[1])
    print("drawLine stub executed.")

# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    # grab the distance of the center of projection from the screen and use it to find the new points for ps
    global d
    # just plug it into the perspective projection formula
    xps = (d*point[0])/(d+point[2])
    yps = (d*point[1])/(d+point[2])
    zps = point[2]/(d+point[2])
    # create the new point perspective projection point
    ps = [xps, yps, zps]
    return ps

# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    displayXY = []
    # reorient the components of the point so that the origin is in the center of the canvas with a positive y axis
    displayXY.append(point[0]+200)
    displayXY.append(-point[1]+200)
    displayXY.append(point[2])
    return displayXY

# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    resetPyramid()
    drawObject(Pyramid)

def larger():
    w.delete(ALL)
    scale(PyramidPointCloud,1.1)
    drawObject(Pyramid)

def smaller():
    w.delete(ALL)
    scale(PyramidPointCloud,.9)
    drawObject(Pyramid)

def forward():
    w.delete(ALL)
    translate(PyramidPointCloud,[0,0,5])
    drawObject(Pyramid)

def backward():
    w.delete(ALL)
    translate(PyramidPointCloud,[0,0,-5])
    drawObject(Pyramid)

def left():
    w.delete(ALL)
    translate(PyramidPointCloud,[-5,0,0])
    drawObject(Pyramid)

def right():
    w.delete(ALL)
    translate(PyramidPointCloud,[5,0,0])
    drawObject(Pyramid)

def up():
    w.delete(ALL)
    translate(PyramidPointCloud,[0,5,0])
    drawObject(Pyramid)

def down():
    w.delete(ALL)
    translate(PyramidPointCloud,[0,-5,0])
    drawObject(Pyramid)

def xPlus():
    w.delete(ALL)
    rotateX(PyramidPointCloud,5)
    drawObject(Pyramid)

def xMinus():
    w.delete(ALL)
    rotateX(PyramidPointCloud,-5)
    drawObject(Pyramid)

def yPlus():
    w.delete(ALL)
    rotateY(PyramidPointCloud,5)
    drawObject(Pyramid)

def yMinus():
    w.delete(ALL)
    rotateY(PyramidPointCloud,-5)
    drawObject(Pyramid)

def zPlus():
    w.delete(ALL)
    rotateZ(PyramidPointCloud,5)
    drawObject(Pyramid)

def zMinus():
    w.delete(ALL)
    rotateZ(PyramidPointCloud,-5)
    drawObject(Pyramid)

root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
drawObject(Pyramid)
w.pack()

controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="DN", command=down)
upButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

root.mainloop()