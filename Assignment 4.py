"""
# Name: Eric Ortiz
# Student Number: 102-39-903
# Date: 2/15/18
# Assignment #4
# Desc: This program is a basic graphics engine that can display a 3D pyramid on a 2D coordinate plane. There are
        a handful of tools also provided that allow the user to translate, scale, and rotate the pyramid -- along
        with a reset button.
        Furthermore, the objects have an option to have their backface removed, to be filled in, and to have their
        polygons occluded if another object is in front of it.
"""

import math

from operator import add
from tkinter import *

# Here we're defining some canvas constants
CanvasWidth = 700
CanvasHeight = 600
d = 500

# Here we define the ZBUFFER frame and any global variables used in buttons
WIREFRAME = False
FILLSETTING = 1
ZBUFFER = []
MAXDEPTH = 10000
POLYOCCLUSION = True


# ***************************** Initialize Object Classes ***************************
class Pyramid:
    # The default constructor accepts a the base, height, and center of the pyramid
    def __init__(self, base=100, height=100, center=list([0, 0, 100])):
        # Create the height, base, and center of the pyramid based on the passed in parameters
        self.height = height
        self.base = base
        self.center = center

        # Rename the variables so that they are easier to manage in point calculation
        c = list(self.center)
        h = self.height
        b = self.base

        # Calculate the points based on the center, height, and base.
        # Naming convention goes: counterclockwise from the bottom left corner
        self.apex = list(map(add, c, [0, h / 2, 0]))
        self.base1 = list(map(add, c, [-b / 2, -h / 2, -b / 2]))
        self.base2 = list(map(add, c, [b / 2, -h / 2, -b / 2]))
        self.base3 = list(map(add, c, [b / 2, -h / 2, b / 2]))
        self.base4 = list(map(add, c, [-b / 2, -h / 2, b / 2]))

        # Pass in the points by value to these default points to be used in the reset function
        self.defaultapex = list(self.apex)
        self.defaultbase1 = list(self.base1)
        self.defaultbase2 = list(self.base2)
        self.defaultbase3 = list(self.base3)
        self.defaultbase4 = list(self.base4)
        self.defaultcenter = list(self.center)

        # Once the vertices are created, we make the polygons of the pyramid and order the vertices in clockwise order
        # which is needed for backface culling later
        self.frontpoly = [self.apex, self.base2, self.base1]
        self.rightpoly = [self.apex, self.base3, self.base2]
        self.backpoly = [self.apex, self.base4, self.base3]
        self.leftpoly = [self.apex, self.base1, self.base4]
        # Because the base of the pyramid is a square, we break that face into two triangular polygons
        self.bottompoly1 = [self.base2, self.base3, self.base1]
        self.bottompoly2 = [self.base4, self.base1, self.base3]

        # We then create the shape and the object's pointcloud, which contains all of the points of the object
        self.shape = [self.bottompoly1, self.bottompoly2, self.frontpoly, self.rightpoly, self.backpoly, self.leftpoly]
        self.pointcloud = [self.apex, self.base1, self.base2, self.base3, self.base4, self.center]

        # Lastly, we set the object to not be selected
        self.selected = False

    # This function is solely used to reset the object to its original position
    def rebuildShape(self):
        # Set the object's points to the value of the previously stored default ones by using the list() function.
        # That prevents the default vertices from being "tied" to these vertices which will be changed constantly.
        self.apex = list(self.defaultapex)
        self.base1 = list(self.defaultbase1)
        self.base2 = list(self.defaultbase2)
        self.base3 = list(self.defaultbase3)
        self.base4 = list(self.defaultbase4)
        # Also reset the center
        self.center = list(self.defaultcenter)

        # Now we just rebuild the polygons, the shape, and the pointcloud
        self.frontpoly = [self.apex, self.base2, self.base1]
        self.rightpoly = [self.apex, self.base3, self.base2]
        self.backpoly = [self.apex, self.base4, self.base3]
        self.leftpoly = [self.apex, self.base1, self.base4]
        self.bottompoly1 = [self.base2, self.base3, self.base1]
        self.bottompoly2 = [self.base4, self.base1, self.base3]

        self.shape = [self.bottompoly1, self.bottompoly2, self.frontpoly, self.rightpoly, self.backpoly, self.leftpoly]
        self.pointcloud = [self.apex, self.base1, self.base2, self.base3, self.base4, self.center]

    # End Pyramid Class

class Box:
    # The default constructor accepts a length, height, depth, and center of the box
    def __init__(self, length=100, height=100, depth=100, center=[0, 0, 0]):
        # Create the height, length, depth, and center of the box based on the passed in parameters
        self.height = height
        self.length = length
        self.depth = depth
        self.center = center

        # Rename the variables so that they are easier to manage in point calculation
        c = list(self.center)
        h = self.height
        l = self.length
        d = self.depth

        # Calculate the points based on the center, length, height, and depth.
        # Naming convention goes: counterclockwise from the bottom left corner, incrementing upwards (i.e. base1 is on
        # the bottom while base5 is right above it
        self.base1 = list(map(add, c, [-l / 2, -h / 2, -d / 2]))
        self.base2 = list(map(add, c, [l / 2, -h / 2, -d / 2]))
        self.base3 = list(map(add, c, [l / 2, -h / 2, d / 2]))
        self.base4 = list(map(add, c, [-l / 2, -h / 2, d / 2]))
        self.base5 = list(map(add, c, [-l / 2, h / 2, -d / 2]))
        self.base6 = list(map(add, c, [l / 2, h / 2, -d / 2]))
        self.base7 = list(map(add, c, [l / 2, h / 2, d / 2]))
        self.base8 = list(map(add, c, [-l / 2, h / 2, d / 2]))

        # Once the vertices are created, we make the polygons of the box. Since the object is rectangular, then every
        # face of it has two polygons - which are just two triangles
        # Also, the vertices are ordered in clockwise order. This is used for backface culling later.
        self.frontpoly1 = [self.base1, self.base5, self.base2]
        self.frontpoly2 = [self.base6, self.base2, self.base5]
        self.backpoly1 = [self.base3, self.base7, self.base4]
        self.backpoly2 = [self.base8, self.base4, self.base7]
        self.leftpoly1 = [self.base4, self.base8, self.base1]
        self.leftpoly2 = [self.base5, self.base1, self.base8]
        self.rightpoly1 = [self.base2, self.base6, self.base3]
        self.rightpoly2 = [self.base7, self.base3, self.base6]
        self.bottompoly1 = [self.base2, self.base3, self.base1]
        self.bottompoly2 = [self.base4, self.base1, self.base3]
        self.toppoly1 = [self.base5, self.base8, self.base6]
        self.toppoly2 = [self.base7, self.base6, self.base8]

        # Pass in the points by value to these default points to be used in the reset function
        self.defaultbase1 = list(self.base1)
        self.defaultbase2 = list(self.base2)
        self.defaultbase3 = list(self.base3)
        self.defaultbase4 = list(self.base4)
        self.defaultbase5 = list(self.base5)
        self.defaultbase6 = list(self.base6)
        self.defaultbase7 = list(self.base7)
        self.defaultbase8 = list(self.base8)
        self.defaultcenter = list(self.center)

        # We then create the shape and the object's pointcloud, which contains all of the points of the object
        self.shape = [self.frontpoly1, self.frontpoly2, self.backpoly1, self.backpoly2, self.leftpoly1, self.leftpoly2,
                      self.rightpoly1, self.rightpoly2, self.bottompoly1, self.bottompoly2, self.toppoly1,
                      self.toppoly2]
        self.pointcloud = [self.base1, self.base2, self.base3, self.base4, self.base5, self.base6, self.base7,
                           self.base8, self.center]

        # Lastly, we set the object to not be selected
        self.selected = False

    def rebuildShape(self):
        # Set the object's points to the value of the previously stored default ones by using the list() function.
        # That prevents the default vertices from being "tied" to these vertices which will be changed constantly.
        self.base1 = list(self.defaultbase1)
        self.base2 = list(self.defaultbase2)
        self.base3 = list(self.defaultbase3)
        self.base4 = list(self.defaultbase4)
        self.base5 = list(self.defaultbase5)
        self.base6 = list(self.defaultbase6)
        self.base7 = list(self.defaultbase7)
        self.base8 = list(self.defaultbase8)
        # Also reset the center
        self.center = list(self.defaultcenter)

        # Now we just rebuild the polygons, the shape, and the pointcloud
        self.frontpoly1 = [self.base1, self.base5, self.base2]
        self.frontpoly2 = [self.base6, self.base2, self.base5]
        self.backpoly1 = [self.base3, self.base7, self.base4]
        self.backpoly2 = [self.base8, self.base4, self.base7]
        self.leftpoly1 = [self.base4, self.base8, self.base1]
        self.leftpoly2 = [self.base5, self.base1, self.base8]
        self.rightpoly1 = [self.base2, self.base6, self.base3]
        self.rightpoly2 = [self.base7, self.base3, self.base6]
        self.bottompoly1 = [self.base2, self.base3, self.base1]
        self.bottompoly2 = [self.base4, self.base1, self.base3]
        self.toppoly1 = [self.base5, self.base8, self.base6]
        self.toppoly2 = [self.base7, self.base6, self.base8]

        self.shape = [self.frontpoly1, self.frontpoly2, self.backpoly1, self.backpoly2, self.leftpoly1, self.leftpoly2,
                      self.rightpoly1, self.rightpoly2, self.bottompoly1, self.bottompoly2, self.toppoly1,
                      self.toppoly2]
        self.pointcloud = [self.base1, self.base2, self.base3, self.base4, self.base5, self.base6, self.base7,
                           self.base8, self.center]

    # End Box Class

class Cylinder:
    def __init__(self, length=8, radius=2, center=[0,0,0]):
        self.length = length
        self.radius = radius
        self.center = center

        c = list(self.center)
        l = self.length
        r = self.radius

        self.face11 =
        self.face12 =
        self.face13 =
        self.face14 =
        self.face15 =
        self.face16 =
        self.face17 =
        self.face18 =
        self.face1c = list(map(add, c, [0, 0, -l / 2]))

        self.face21 =
        self.face22 =
        self.face23 =
        self.face24 =
        self.face25 =
        self.face26 =
        self.face27 =
        self.face28 =
        self.face2c = list(map(add, c, [0, 0, l / 2]))



        # ***************************** Create the Objects ***************************

# Create a box in the middle of the frame
customCube1 = Box(100, 100, 100, [0,0,0])
# Create a box offset by -200 in x and 100 in z, and make it longer
customCube2 = Box(100, 50, 50, [-200, 0, 100])
# Create a pyramid that is taller than it is wide, 200 in x and 100 in z
customPyramid = Pyramid(100, 150, [200, 0, 100])
customCube3 = Box(100, 100, 100,[0, 0, 0])
customPyramid2 = Pyramid(100, 200, [0, 0, 0])


# This is the main list of objects referenced later to be drawn
currentObject = [customCube1, customPyramid2]
# This is the iterator to keep track of which object is selected
objectNumber = 0

# ***************************** Backend Button Functions ***************************

# This function resets the object to its original size and location in 3D space
def resetPyramid(object):
    # Just call the object's built-in reset function
    object.rebuildShape()

    print("resetPyramid stub executed.")


# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    # Iterate through the points in the object
    for i in range(len(object)):
        point = object[i]
        # For every point, add each component with that of the displacement component
        for j in range(len(point)):
            point[j] += displacement[j]

    print("translate stub executed.")


# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object, scalefactor):
    # Create a variable for object's origin (which is always set to be the last point in the pointcloud)
    center = object[-1]

    # Translate the object to the coordinate plane origin by using the center of the object
    for i in range(len(object)-1):
        point = object[i]
        for j in range(len(point)):
            point[j] -= center[j]

    # Iterate through the points in the object and scale it by the scalefactor
    for i in range(len(object)-1):
        point = object[i]
        for j in range(len(point)):
            point[j] *= scalefactor

    # Move the object back to its original position
    for i in range(len(object)-1):
        point = object[i]
        for j in range(len(point)):
            point[j] += center[j]

    print("scale stub executed.")


# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard position]
def rotateZ(object, degrees):
    # First convert the degrees to radians
    radians = math.radians(degrees)
    # Then create a variable for object's center (which is always set to be the last point in the pointcloud)
    center = object[-1]

    # Translate the object to the coordinate plane origin by using the center of the object
    for i in range(len(object) - 1):
        point = object[i]
        for j in range(len(point)):
            point[j] -= center[j]

    # Iterate through the polygons in the object and grab each point
    for i in range(len(object)-1):
        point = object[i]
        # So that the points don't get manipulated during computation, assign the x and y values separately
        x = point[0]
        y = point[1]
        # Use the z-rotation function
        point[0] = (x * math.cos(radians)) - (y * math.sin(radians))
        point[1] = (x * math.sin(radians)) + (y * math.cos(radians))

    # Move the object back to its original position
    for i in range(len(object)-1):
        point = object[i]
        for j in range(len(point)):
            point[j] += center[j]


    print("rotateZ stub executed.")


# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object, degrees):
    # First convert the degrees to radians
    radians = math.radians(degrees)
    # Then create a variable for object's center (which is always set to be the last point in the pointcloud)
    center = object[-1]

    # Translate the object to the coordinate plane origin by using the center of the object
    for i in range(len(object) - 1):
        point = object[i]
        for j in range(len(point)):
            point[j] -= center[j]

    # Iterate through the polygons in the object and grab each point
    for i in range(len(object)-1):
        point = object[i]
        # So that the points don't get manipulated during computation, assign the x and z values separately
        x = point[0]
        z = point[2]
        # Use the y-rotation function
        point[0] = (x * math.cos(radians)) + (z * math.sin(radians))
        point[2] = (-1 * (x * math.sin(radians))) + (z * math.cos(radians))

    # Move the object back to its original position
    for i in range(len(object) - 1):
        point = object[i]
        for j in range(len(point)):
            point[j] += center[j]

    print("rotateY stub executed.")


# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object, degrees):
    # First convert the degrees to radians
    radians = math.radians(degrees)
    # Then create a variable for object's center (which is always set to be the last point in the pointcloud)
    center = object[-1]

    # Translate the object to the coordinate plane origin by using the center of the object
    for i in range(len(object) - 1):
        point = object[i]
        for j in range(len(point)):
            point[j] -= center[j]

    # Iterate through the polygons in the object and grab each point
    for i in range(len(object)-1):
        point = object[i]
        # So that the points don't get manipulated during computation, assign the y and z values separately
        y = point[1]
        z = point[2]
        # Use the x-rotation function
        point[1] = (y * math.cos(radians)) - (z * math.sin(radians))
        point[2] = (y * math.sin(radians)) + (z * math.cos(radians))

    # Move the object back to its original position
    for i in range(len(object) - 1):
        point = object[i]
        for j in range(len(point)):
            point[j] += center[j]

    print("rotateX stub executed.")

# This function will select the next object in the list of currentObjects
def selectNextObject():
    # Grab the global iterator for the selection and the list of objects
    global objectNumber
    global currentObject

    # Deselect the currently selected object
    currentObject[objectNumber].selected = False

    # Iterate through the list of objects, unless if the object is at the end of the list. In which case, make the
    # iterator 0 again
    if objectNumber is (len(currentObject)-1):
        objectNumber = 0
    else:
        objectNumber += 1

    # Reselect the object at the iterator
    currentObject[objectNumber].selected = True

    print("nextSelection stub executed.")


# This function will select the previous object in the list of currentObjects
def selectPrevObject():
    # Grab the global iterator for the selection and the list of objects
    global objectNumber
    global currentObject

    # Deselect the currently selected object
    currentObject[objectNumber].selected = False

    # Iterate through the list of objects, unless if the object is at the beginning of the list. Then make the iterator
    # the last item in the list
    if objectNumber is 0:
        objectNumber = (len(currentObject)-1)
    else:
        objectNumber -= 1

    # Reselect the object at the iterator
    currentObject[objectNumber].selected = True

    print("prevSelection stub executed.")

# ***************************** Backend Button Functions ***************************
# This function resets the ZBUFFER and then redraws every object in our currentObject list
def drawAllObjects():
    # First we grab the global ZBUFFER, then we set each point in the zbuffer frame to have the MAXDEPTH, which is
    # defined at the beginning of the program
    global ZBUFFER
    ZBUFFER = [[MAXDEPTH for j in range(CanvasHeight)] for i in range(CanvasWidth)]

    # Once the ZBUFFER is set, we just draw every object in the currentObject list
    for i in range(len(currentObject)):
        drawCurrentObject(currentObject[i])

    print("ALL OBJECTS DRAWN")


# This function will draw an object by repeatedly calling drawPoly on each polygon in the object
def drawCurrentObject(object):
    # Iterate through the polygons of the object and pass it to drawPoly
    for i in range(len(object.shape)):
        # We also pass in whether or not the object is selected
        drawPoly(object.shape[i], object.selected)

    print("drawObject stub executed.")


# This function will draw a polygon by repeatedly calling drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly, selected):
    # First we need to cull the backfaces of the object. This is done by running each polygon through the backface
    # culling function and determining whether or not the polygon is facing the camera
    frontface = backfaceCulling(poly)

    # If frontface is true, then we display can display that polygon
    if frontface:
        # But before we draw the lines for the edges of the polygon, we need to fill it if both the fill setting allows
        # it and if the wireframe is turned off
        if FILLSETTING >= 1 and WIREFRAME is False:
            # If both of those are true, then we can fill the polygon
            scan(poly, selected)
        # Once we done filling (or not), we iterate through the edges of the polygon and draw the lines for it
        for i in range(len(poly)):
            drawLine(poly[i - 1], poly[i], selected)

    print("drawPoly stub executed.")


# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(start, end, selected):
    # First convert the given start and end points of the edge to their perspective projection
    startproject = project(start)
    endproject = project(end)

    # Then we displace the projection points so that the center of the canvas is in the middle of the canvas
    startdisplay = convertToDisplayCoordinates(startproject)
    enddisplay = convertToDisplayCoordinates(endproject)

    # If the fill setting permits it or if we have the wireframes turned on, then we draw the edges of the polygon
    if FILLSETTING != 2 or WIREFRAME is True:
        # If the object is selected, draw the lines in red. Otherwise, draw them in black
        if selected is True:
            w.create_line(startdisplay[0], startdisplay[1], enddisplay[0], enddisplay[1], fill="red")
        else:
            w.create_line(startdisplay[0], startdisplay[1], enddisplay[0], enddisplay[1])

    print("drawLine stub executed.")


# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    # Grab the distance of the center of projection from the screen and use it to find the new points for ps
    global d
    # Just plug it into the perspective projection formula
    xps = (d * point[0]) / (d + point[2])
    yps = (d * point[1]) / (d + point[2])
    zps = point[2] / (d + point[2])
    # Return the new point perspective projection point
    return [xps, yps, zps]


# This function converts a 2D point to display coordinates (+ depth) in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    displayXY = []
    # Reorient the components of the point so that the origin is in the center of the canvas with a positive y axis
    displayXY.append(point[0] + CanvasWidth/2)
    displayXY.append(-point[1] + CanvasHeight/2)
    displayXY.append(point[2])
    # Return the new display point
    return displayXY


# This function is removes the back faces of an object that are pointing away from the camera.
def backfaceCulling(poly):
    # If WIREFRAME is true, then we'll show the backfaces, return true, and not even bother calculating
    if WIREFRAME:
        return True

    # Otherwise, we'll grab the points from the polygon, which should be arranged in clockwise order
    p0 = poly[0]
    p1 = poly[1]
    p2 = poly[2]

    # Then we create the x, y, and z components of the surface normal by running the former three points through a
    # cross-product
    A = ((p1[1] - p0[1]) * (p2[2] - p0[2]) - (p2[1] - p0[1]) * (p1[2] - p0[2]))
    B = -((p1[0] - p0[0]) * (p2[2] - p0[2]) - (p2[0] - p0[0]) * (p1[2] - p0[2]))
    C = ((p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]))

    # Let's create a point q which is the perspective projected version of the point p0
    q = project(p0)

    # So then we compute the plane offset as the dot product of the surface normal and the perspective point, q, on the
    # polygon
    offset = q[0] * A + q[1] * B + q[2] * C

    # So if the z component of the surface normal times the screen depth (d) minus the plane offset is greater than
    # zero, the point is on the positive side of the plane.
    return (C * (-d) - offset) > 0


# This function scans the polygon, line by line, and fills it with the appropriate color
def scan(poly, selected):
    # To begin with, we need to create a table of the polygon's edges that's sorted by the edge's maximum y value
    # The each row in the table is organized as: ymax, ymin, initial x, negative inverse slope, z, and change in z
    table = createTable(poly)
    # Once the sorted table is made, we set a pointer to the top of the polygon, which should be the initial x and the
    # maximum y of the first edge in the table
    pointer = [table[0][2], table[0][0]]

    # So long as the pointer is above the minimum value of y of the two edges that we are scanning between, we will
    # continue to fill the polygon
    while pointer[1] > table[0][1] and pointer[1] > table[1][1]:
        # Before anything else, we need to determine the z values of the left and right edge of the polygon by taking
        # each edge's z and subtracting its change in z
        zHorLeft = table[0][4] - table[0][5]
        zHorRight = table[1][4] - table[1][5]

        # Then, we have to determine the vertical constant of each point in a line, which is dependent on the left and
        # right edges' horizontal z's and the x initials of the edges
        # If the initial x for both edges is (almost) the same, then we just set the constant to be 0
        if math.trunc(table[1][2]-table[0][2]) == 0:
            zVertConst = 0
        else:
            zVertConst = (zHorRight - zHorLeft)/(table[1][2]-table[0][2])

        # To get us started, we set the vertical iterator to left edge's horizontal z
        zVert = zHorLeft

        # For every line between two edges, we'll work the pointer from the left edge's initial x to the right edge's
        while pointer[0] < table[1][2]:
            # We need to determine the z value of our point and see if it's closer to the camera than whatever point is
            # already at that spot
            pz = zVert + zVertConst

            # If polyocclusion is turned off, then we just ignore the z buffer basically by make the z value of the
            # pointer to be the same as the value already in the ZBUFFER
            if not POLYOCCLUSION:
                pz = ZBUFFER[math.trunc(pointer[0])][pointer[1]]

            # Then we check to see if the point is on-screen and if the z value of the pointer is less than or equal to
            # the current value of the zbuffer at the pointer's location
            if 0 < pointer[0] < CanvasWidth and 0 < pointer[1] < CanvasHeight and \
                            pz <= ZBUFFER[math.trunc(pointer[0])][pointer[1]]:

                # We update the value at the zbuffer to be that of the z of the pointer
                ZBUFFER[math.trunc(pointer[0])][pointer[1]] = pz

                # The farther along X the pointer is, the more white it becomes - this equation figures out the
                # hexadecimal color of the point based on where the point is and its relation to the CanvasWidth
                # We also split the "0x" part of it so we can concatenate the string easily to the rest of the fill
                # color later
                fillBlue = hex(round(pointer[0] * (255 / CanvasWidth))).split('x')[-1]

                # If somehow we get a single digit value for the hexademical, we just add a zero to the front of it
                if len(fillBlue) < 2:
                    fillBlue = "0%s" % fillBlue

                # Lastly, we make the actual fill color to be 0000 plus whatever the range of blue we have
                fillColor = "#FFFF%s" % fillBlue

                # This is used to demonstrate zbuffer by making the unselected object blue
                if not selected:
                    fillColor = "#0000FF"
            # If the pointer is off the screen, then we change the fill color to be "", which is basically null. This
            # will prevent the program from crashing and also minorly help boost performance
            else:
                fillColor = ""

            # Now that we have our fill color, we make the point we draw have the outline of that fill color and not
            # bother filling in the actual rectangle since the points are small enough that it doesn't matter
            w.create_rectangle(pointer[0], pointer[1], pointer[0], pointer[1], fill="", outline=fillColor)
            # We update the zVert iterator to be that of the z of the pointer
            zVert = pz
            # Lastly for this row, we increment the pointer along the x axis
            pointer[0] += 1

        # Once we're done with iterating through the row, we update the initial z for both edges to be that of the left
        # and right horizonal z's respectively
        table[0][4] = zHorLeft
        table[1][4] = zHorRight
        # We then increment the initial x values of both edges by their negative inverse slopes
        table[0][2] += table[0][3]
        table[1][2] += table[1][3]
        # And finally, we set the pointer equal to the leftmost edge's initial x and decrement the y value of pointer
        pointer[0] = table[0][2]
        pointer[1] -= 1

    # Once the first two edges are done being filled, we check to see which edge's ymin we passed up while scanning
    # Whichever one that is, we delete from the table
    if table[0][1] >= table[1][1]:
        del table[0]
    else:
        del table[1]

    # Next we need to make sure that we're still scanning from the leftmost edge to the rightmost one. We may have
    # switched sides along the way, which is denoted by the new first edge of the row having a greater x initial than
    # the new second edge of the row
    # If that's the case, we'll just swap 'em in the table
    if table[0][2] > table[1][2]:
        table[0], table[1] = table[1], table[0]

    # Once we have our two "new" edges situated in the table, we can begin filling the polygon again, moving from left
    # to right
    # Since the ymin values of the last two edges should be the same, we just need to check if we passed one of them
    # before we stop filling
    while pointer[1] > table[0][1]:
        zHorLeft = table[0][4] - table[0][5]
        zHorRight = table[1][4] - table[1][5]

        if math.trunc(table[1][2]-table[0][2]) == 0:
            zVertConst = 0
        else:
            zVertConst = (zHorRight - zHorLeft)/(table[1][2]-table[0][2])

        zVert = zHorLeft

        while pointer[0] < table[1][2]:
            pz = zVert + zVertConst

            if not POLYOCCLUSION:
                pz = ZBUFFER[math.trunc(pointer[0])][pointer[1]]

            if 0 < pointer[0] < CanvasWidth and 0 < pointer[1] < CanvasHeight and \
                            pz <= ZBUFFER[math.trunc(pointer[0])][pointer[1]]:
                ZBUFFER[math.trunc(pointer[0])][pointer[1]] = pz
                fillBlue = hex(round(pointer[0] * (255 / CanvasWidth))).split('x')[-1]

                if len(fillBlue) < 2:
                    fillBlue = "0%s" % fillBlue

                fillColor = "#FFFF%s" % fillBlue

                if not selected:
                    fillColor = "#0000FF"
            else:
                fillColor = ""

            w.create_rectangle(pointer[0], pointer[1], pointer[0], pointer[1], fill="", outline=fillColor)

            zVert = pz
            pointer[0] += 1

        table[0][4] = zHorLeft
        table[1][4] = zHorRight
        table[0][2] += table[0][3]
        table[1][2] += table[1][3]
        pointer[0] = table[0][2]
        pointer[1] -= 1


# This function creates a table where each row represents the edge of the triangular polygon passed in. Each row
# contains the edge's ymax, ymin, initial x, negative inverse slope, z, and dz. All of this is used in computing the
# polygon fill and zbuffer of a face of the object
def createTable(poly):
    # First we create an empty list of the vertices in the polygon and we initialize the table
    vertices = []
    table = []

    # We then run through the list of vertices in the polygon, convert them all to display coordinates, and add them to
    # our new list of vertices
    for i in range(len(poly)):
        vertices.append(convertToDisplayCoordinates(project(poly[i])))

    # Out of the new vertices, we create 3 edges, which correspond to the ones initialized in the polygon passed in
    edgeList = [[vertices[0], vertices[1]], [vertices[1], vertices[2]], [vertices[2], vertices[0]]]

    # For each edge, we determine its ymax, ymin, initial x, negative inverse slope, z, and dz before adding those
    # values to its corresponding row
    for i in range(len(edgeList)):
        # First we grab an edge and check to see which of its two points has the higher y value
        edge = edgeList[i]

        if edge[0][1] >= edge[1][1]:
            # From there, we set the maximum y value of the edge accordingly, with the other y value automatically being
            # the minimum
            # We truncate the values so that our negative inverse slope function doesn't give us a stupidly high number
            ymax = math.trunc(edge[0][1])
            ymin = math.trunc(edge[1][1])

            # The initial x1 value of the edge corresponds to the point with the highest y value. The other x2 value is
            # just used later the "slope" calculation
            x1 = math.trunc(edge[0][0])
            x2 = math.trunc(edge[1][0])

            # We also need to grab the z value of the highest point and the lowest point. Both are used to find the
            # change in z (dz) later
            z1 = edge[0][2]
            z2 = edge[1][2]
        else:
            ymin = math.trunc(edge[0][1])
            ymax = math.trunc(edge[1][1])

            x2 = math.trunc(edge[0][0])
            x1 = math.trunc(edge[1][0])

            z2 = edge[0][2]
            z1 = edge[1][2]

        # If the edge is a horizontal line, then we need to set the negative inverse slope and change in z to 0
        if ymax - ymin == 0:
            dx = 0.0
            dz = 0.0
        # Otherwise, compute dx and dz as normal
        else:
            dx = -((x1 - x2) / (ymax - ymin))
            dz = (z2 - z1) / (ymin - ymax)

        # Then we create the rows based on which edge is being evaluated
        if i == 0:
            rowOne = [ymax, ymin, x1, dx, z1, dz]
        elif i == 1:
            rowTwo = [ymax, ymin, x1, dx, z1, dz]
        else:
            rowThree = [ymax, ymin, x1, dx, z1, dz]

    # Once we're done creating the rows, we need to order the edges in the table by their ymax and then their initial x
    # This is done be checking which two edges share the same ymax - since this would imply those two edges have the
    # shared highest of the three

    # If all three of them have the same max height, then the triangle is a upside down right triangle. So, we need to
    # make sure that the horizontal edge is the first row, and the second row is the leftmost edge
    if rowOne[0] == rowTwo[0] == rowThree[0]:
        # We do this by checking to make sure that the first row we check has the greatest ymin. This row contains the
        # horizontal edge. Then we check which of the other two rows has the smallest x initial. This row is the left-
        # most edge. Then we order them accordingly
        if rowOne[1] > rowTwo[1] and rowTwo[3] < rowThree[3]:
            table.append(rowOne)
            table.append(rowTwo)
            table.append(rowThree)
        elif rowOne[1] > rowTwo[1] and rowThree[3] < rowTwo[3]:
            table.append(rowOne)
            table.append(rowThree)
            table.append(rowTwo)
        elif rowTwo[1] > rowOne[1] and rowOne[3] < rowThree[3]:
            table.append(rowTwo)
            table.append(rowOne)
            table.append(rowThree)
        elif rowTwo[1] > rowOne[2] and rowThree[3] < rowOne[3]:
            table.append(rowTwo)
            table.append(rowThree)
            table.append(rowOne)
        elif rowThree[1] > rowOne[1] and rowOne[3] < rowTwo[3]:
            table.append(rowThree)
            table.append(rowOne)
            table.append(rowTwo)
        else:
            table.append(rowThree)
            table.append(rowTwo)
            table.append(rowOne)

    # In every other case, once we determine which two edges have the same ymax, we need to figure out which edge
    # is the leftmost edge. This can be done by comparing their negative inverse slopes. Whichever one is negative -
    # i.e. the actual slope of the edge is positive - that edge is the leftmost edge.

    # Thus we order the table accordingly: The leftmost highest edge, the rightmost highest edge, and the lowest
    # edge
    elif rowOne[0] == rowTwo[0]:
        if rowOne[3] < rowTwo[3]:
            table.append(rowOne)
            table.append(rowTwo)
        else:
            table.append(rowTwo)
            table.append(rowOne)

        table.append(rowThree)

    elif rowTwo[0] == rowThree[0]:
        if rowTwo[3] < rowThree[3]:
            table.append(rowTwo)
            table.append(rowThree)
        else:
            table.append(rowThree)
            table.append(rowTwo)

        table.append(rowOne)

    else:
        if rowOne[3] < rowThree[3]:
            table.append(rowOne)
            table.append(rowThree)
        else:
            table.append(rowThree)
            table.append(rowOne)

        table.append(rowTwo)

    # Finally, we return the ordered table
    return table


# ***************************** Interface Functions ***************************
# Everything below this point implements the interface

# Reset Button Call
def reset():
    w.delete(ALL)
    resetPyramid(currentObject[objectNumber])
    drawAllObjects()

# Scale Larger Call
def larger():
    w.delete(ALL)
    scale(currentObject[objectNumber].pointcloud, 1.1)
    drawAllObjects()

# Scale Smaller Call
def smaller():
    w.delete(ALL)
    scale(currentObject[objectNumber].pointcloud, .9)
    drawAllObjects()

# Translate Forward Call
def forward():
    w.delete(ALL)
    translate(currentObject[objectNumber].pointcloud, [0, 0, 10])
    drawAllObjects()

# Translate Backward Call
def backward():
    w.delete(ALL)
    translate(currentObject[objectNumber].pointcloud, [0, 0, -10])
    drawAllObjects()

# Translate Left Call
def left():
    w.delete(ALL)
    translate(currentObject[objectNumber].pointcloud, [-10, 0, 0])
    drawAllObjects()

# Translate Right Call
def right():
    w.delete(ALL)
    translate(currentObject[objectNumber].pointcloud, [10, 0, 0])
    drawAllObjects()

# Translate Up Call
def up():
    w.delete(ALL)
    translate(currentObject[objectNumber].pointcloud, [0, 10, 0])
    drawAllObjects()

# Translate Down Call
def down():
    w.delete(ALL)
    translate(currentObject[objectNumber].pointcloud, [0, -10, 0])
    drawAllObjects()

# Rotate Positive X Call
def xPlus():
    w.delete(ALL)
    rotateX(currentObject[objectNumber].pointcloud, 5)
    drawAllObjects()

# Rotate Negative X Call
def xMinus():
    w.delete(ALL)
    rotateX(currentObject[objectNumber].pointcloud, -5)
    drawAllObjects()

# Rotate Positive Y Call
def yPlus():
    w.delete(ALL)
    rotateY(currentObject[objectNumber].pointcloud, 5)
    drawAllObjects()

# Rotate Negative Y Call
def yMinus():
    w.delete(ALL)
    rotateY(currentObject[objectNumber].pointcloud, -5)
    drawAllObjects()

# Rotate Positive Z Call
def zPlus():
    w.delete(ALL)
    rotateZ(currentObject[objectNumber].pointcloud, 5)
    drawAllObjects()

# Rotate Negative Z Call
def zMinus():
    w.delete(ALL)
    rotateZ(currentObject[objectNumber].pointcloud, -5)
    drawAllObjects()

# Select Next Object Call
def nextSelection():
    w.delete(ALL)
    selectNextObject()
    drawAllObjects()

# Select Previous Object Call
def prevSelection():
    w.delete(ALL)
    selectPrevObject()
    drawAllObjects()

# Toggle Backface Culling Call
def backfaceToggle():
    global WIREFRAME
    w.delete(ALL)
    WIREFRAME = not WIREFRAME

    print("backfacetoggle stub executed.")

    drawAllObjects()

# Change Filling Setting Call
def changeFillSetting():
    global FILLSETTING

    w.delete(ALL)

    if FILLSETTING == 0:
        FILLSETTING = 1
    elif FILLSETTING == 1:
        FILLSETTING = 2
    else:
        FILLSETTING = 0

    fill_button_text.set("Setting is: %d" % FILLSETTING)

    print("filltoggle stub executed")

    drawAllObjects()

# Toggle Polygon Occlusion Call
def polygonOcclusion():
    global POLYOCCLUSION

    w.delete(ALL)

    POLYOCCLUSION = not POLYOCCLUSION

    if POLYOCCLUSION:
        setting = "ON"
    else:
        setting = "OFF"

    occlusion_button_text.set("Occlusion is %s" % setting)

    print("polygonocclusion stub executed")

    drawAllObjects()


# ***************************** Interface and Window Construction ***************************
# Here we actually construct the base of the interface with tkinter
root = Tk()
outerframe = Frame(root)
outerframe.pack()
w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()

# Then we set the first object in the list of objects to be selected
currentObject[0].selected = True
# Then we draw all of the objects
drawAllObjects()

# We also set up the text for the polygon filling and polygon occlusion buttons which need to be modified every time we
# press them
fill_button_text = StringVar()
fill_button_text.set("Setting is: %d" % FILLSETTING)
occlusion_button_text = StringVar()
occlusion_button_text.set("Occlusion is ON")

# So before we set up all of the buttons and labels, we need to make the control panel for them
controlpanel = Frame(outerframe)
controlpanel.pack()

# Reset Button Block
resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

# Scale Buttons Block
scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

# Translate Buttons Block
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

# Rotation Buttons Block
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

# Selection Buttons Block
selectcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
selectcontrols.pack(side=LEFT)

selectcontrolslabel = Label(selectcontrols, text="Selection")
selectcontrolslabel.pack()

selectBackwardButton = Button(selectcontrols, text="Prev", command=prevSelection)
selectBackwardButton.pack(side=LEFT)

selectForwardButton = Button(selectcontrols, text="Next", command=nextSelection)
selectForwardButton.pack(side=LEFT)

# Wireframe Toggle Block
wireframecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
wireframecontrols.pack(side=LEFT)

wireframecontrolslabel = Label(wireframecontrols, text="Wireframe")
wireframecontrolslabel.pack()

wireframeToggle = Checkbutton(wireframecontrols, text="Toggle", command=backfaceToggle)
wireframeToggle.pack(side=LEFT)

# Fill Setting Button Block
fillsettingcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
fillsettingcontrols.pack(side=LEFT)

fillsettingcontrolslabel = Label(fillsettingcontrols, text="Polygon Fill")
fillsettingcontrolslabel.pack()

fillsettingButton = Button(fillsettingcontrols, textvariable=fill_button_text, command=changeFillSetting)
fillsettingButton.pack(side=LEFT)

# Polygon Occlusion Button Block
polyocclusioncontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
polyocclusioncontrols.pack(side=LEFT)

polyocclusioncontrolslabel = Label(polyocclusioncontrols, text="Polygon Occlusion")
polyocclusioncontrolslabel.pack()

polyocclusionButton = Button(polyocclusioncontrols, textvariable=occlusion_button_text, command=polygonOcclusion)
polyocclusionButton.pack()

# Loop the window
root.mainloop()