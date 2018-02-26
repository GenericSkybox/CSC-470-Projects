"""
# Name: Eric Ortiz
# Student Number: 102-39-903
# Date: 2/26/18
# Assignment #5
# Desc: This program renders non-polygonal objects using the ray tracing method via a recursive ray tracer already
        provided in class.
"""

import math

from tkinter import *

# Here we're defining the window constants
CanvasWidth = 800
CanvasHeight = 800

# Lighting and Shading Constants
# L is the lighting vector
L = [1, 1, -1]
# Ia is the level of ambient lighting - which is just a percentage for RGB
Ia = [0.3, 0.3, 0.3]
# Ip is the level of point lighting - which is a percentage for RGB
Ip = [0.5, 0.5, 0.5]
# Ks is the constant of specular reflectivity for the object, given in an array of percentages in RGB
Ks = [0.7, 0.7, 0.7]
# V is the view vector
V = [0, 0, -100]
# N is shininess of the surface
N = 10

# ***************************** Backend Render Functions ***************************
# This function traces the ray through the environment
def trace_ray(level, cop, ray, intensity):
    # We need to "initialize" intersect and obj_normal
    intersect = [None, None, None]
    obj_normal = [None, None, None]

    if level == 0:
        # Maximum depth exceeded -- return black
        intensity = [0, 0, 0]
    else:
        # Check for intersection of ray with objects and set up RGB values corresponding to objects

        # Set distance of closest object initially to a very large number
        t = [100000]

        # Initially no object has been intersected by the ray
        object_code = -1

        # Check for checkerboard intersection
        if checkerboard_intersection(cop, ray, t, intersect):
            object_code = 0
            #print("checkerboard")

        # Check for intersection with Sphere 1
        if sphere_intersection(cop, ray, t, intersect, obj_normal, 0, -400, 600, 100):
            object_code = 1
            #print("green_sphere")

        # Check for intersection with Sphere 2
        if sphere_intersection(cop, ray, t, intersect, obj_normal, -200, -250, 1000, 200):
            object_code = 2
            #print("blue_sphere")

        # Depending on which object was intersected, return that object's point intensity
        if object_code == 0:
            checkerboard_point_intensity(level, ray, intersect, intensity)
        elif object_code == 1:
            # For each sphere you need to provide the base color of the sphere
            # This sphere is green
            base = [0, 255, 0]
            sphere_point_intensity(level, ray, intersect, obj_normal, intensity, base)
        elif object_code == 2:
            # This sphere is blue
            base = [0, 0, 255]
            sphere_point_intensity(level, ray, intersect, obj_normal, intensity, base)
        else:
            # If no objects were intersected, return the background color
            intensity[0] = 150
            intensity[1] = 150
            intensity[2] = 255

    return intensity


# This function computes whether or not the checkerboard as been intersected
def checkerboard_intersection(cop, ray, t, intersect):
    # Normal of the plane
    a = 0
    b = 1
    c = 0

    # Point on the plane
    x1 = 0
    y1 = -500
    z1 = 0

    # Compute intersection of ray with plane
    denom = a * ray[0] + b * ray[1] + c * ray[2]

    if math.fabs(denom) <= 0.001:
        # Ray is parallel to plane
        return False
    else:
        d = a * x1 + b * y1 + c * z1
        t_object = -(a * cop[0] + b * cop[1] + c * cop[2] - d) / denom
        x = cop[0] + ray[0] * t_object
        y = cop[1] + ray[1] * t_object
        z = cop[2] + ray[2] * t_object

        if (z < 0.0) or (z > 8000) or (t_object < 0.0001):
            # No visible intersection
            return False
        elif t[0] < t_object:
            # Another object is closer
            return False
        else:
            # Update t and the intersection point
            t[0] = t_object
            intersect[0] = x
            intersect[1] = y
            intersect[2] = z
            return True


# This function computes the color of the checkerboard
def checkerboard_point_intensity(level, ray, intersect, intensity):
    # Color_flag determines whether or not the square is red or white
    if intersect[0] >= 0.0:
        color_flag = True
    else:
        color_flag = False

    if math.fabs(math.fmod(intersect[0], 400.0)) > 200.0:
        color_flag = not color_flag

    if math.fabs(math.fmod(intersect[2], 400.0)) > 200.0:
        color_flag = not color_flag

    # These calculations are used in the trace_ray call
    n_norm = [0, 1, 0]

    magnitude = (ray[0] * ray[0] + ray[1] * ray[1] + ray[2] * ray[2]) ** (1 / 2.0)
    ray_norm = [0, 0, 0]

    for i in range(3):
        ray_norm[i] = ray[i] / magnitude

    # Calculate the reflection vector
    cosine_phi = 0
    for i in range(3):
        cosine_phi += (-ray_norm[i]) * n_norm[i]

    r = [0, 0, 0]
    if cosine_phi > 0:
        for i in range(3):
            r[i] = n_norm[i] - (-ray_norm[i]) / (2 * cosine_phi)
    elif cosine_phi == 0:
        for i in range(3):
            r[i] = ray_norm[i]
    else:
        for i in range(3):
            r[i] = -n_norm[i] + (-ray_norm[i]) / (2 * cosine_phi)

    # Trace the reflection ray
    trace_ray(level - 1, intersect, r, intensity)

    if color_flag:
        # Red

        # Implement the lighting model from the previous assignment
        lightingModel = computeReflection(n_norm, [255, 0, 0], True)

        intensity[0] = 0.4 * intensity[0] + lightingModel[0]
        intensity[1] = 0.4 * intensity[1] + lightingModel[1]
        intensity[2] = 0.4 * intensity[2] + lightingModel[2]
    else:
        # White

        # Implement the lighting model from the previous assignment
        lightingModel = computeReflection(n_norm, [255, 255, 255], True)

        intensity[0] = 0.4 * intensity[0] + lightingModel[0]
        intensity[1] = 0.4 * intensity[1] + lightingModel[1]
        intensity[2] = 0.4 * intensity[2] + lightingModel[2]


# This function computes whether or not the sphere has been intersected
def sphere_intersection(cop, ray, t, intersect, obj_normal, l, m, n, r):
    # Compute Intersection of Ray with Sphere
    asphere = ray[0] * ray[0] + ray[1] * ray[1] + ray[2] * ray[2]
    bsphere = 2 * ray[0] * (cop[0] - l) + 2 * ray[1] * (cop[1] - m) + 2 * ray[2] * (cop[2] - n)
    csphere = l * l + m * m + n * n + cop[0] * cop[0] + cop[1] * cop[1] + cop[2] * cop[2] + 2 * (-l * cop[0] - m * cop[1] - n * cop[2]) - r * r

    discriminant = bsphere * bsphere - 4 * asphere * csphere

    if discriminant < 0:
        return False
    else:
        ts1 = (-bsphere + discriminant ** (1 / 2.0)) / (2 * asphere)
        ts2 = (-bsphere - discriminant ** (1 / 2.0)) / (2 * asphere)

        if ts1 >= ts2:
            tsphere = ts2
        else:
            tsphere = ts1

        if t[0] < tsphere:
            # Another object is closer
            return False
        elif tsphere < 0.0:
            # No visible intersection
            return False
        else:
            t[0] = tsphere

            for i in range(3):
                intersect[i] = cop[i] + ray[i] * tsphere

            # Reset the object normal using the intersect and the sphere's center
            obj_normal[0] = intersect[0] - l
            obj_normal[1] = intersect[1] - m
            obj_normal[2] = intersect[2] - n

            return True


# This function compute the color of the sphere
def sphere_point_intensity(level, ray, intersect, n, intensity, base):
    # Normalize the incoming ray vector and the surface normal vector
    magnitude = (ray[0] * ray[0] + ray[1] * ray[1] + ray[2] * ray[2]) ** (1/2.0)
    ray_norm = [0, 0, 0]

    for i in range(3):
        ray_norm[i] = ray[i] / magnitude

    magnitude = (n[0] * n[0] + n[1] * n[1] + n[2] * n[2]) ** (1/2.0)
    n_norm = [0, 0, 0]

    for i in range(3):
        n_norm[i] = n[i] / magnitude

    # Calculate the reflection vector
    cosine_phi = 0
    for i in range(3):
        cosine_phi += (-ray_norm[i]) * n_norm[i]

    r = [0, 0, 0]
    if cosine_phi > 0:
        for i in range(3):
            r[i] = n_norm[i] - (-ray_norm[i]) / (2 * cosine_phi)
    elif cosine_phi == 0:
        for i in range(3):
            r[i] = ray_norm[i]
    else:
        for i in range(3):
            r[i] = -n_norm[i] + (-ray_norm[i]) / (2 * cosine_phi)

    # Trace the reflection ray
    trace_ray(level - 1, intersect, r, intensity)

    # Implement the lighting model from the previous assignment
    lightingModel = computeReflection(n, base, False)

    # Add effect of local color
    intensity[0] = 0.7 * intensity[0] + lightingModel[0]
    intensity[1] = 0.7 * intensity[1] + lightingModel[1]
    intensity[2] = 0.7 * intensity[2] + lightingModel[2]


# This function returns the intensity of light at a point, given its normal vector
def computeReflection(normal, base, bright):
    # We'll eventually return an intensity, so let's set it up at the beginning
    finalIntensity = []

    # We need to check to see if this object is a bright object or not, and set the ambient lighting accordingly
    if bright:
        Ia = [0.6, 0.6, 0.6]
    else:
        Ia = [0.3, 0.3, 0.3]

    # Next we need to create Kd based off of the base color passed in
    Kd = []
    for i in range(3):
        Kd.append(base[i]/255)

    # Normalize the normal (in case it isn't normal)
    sqrtN = (normal[0]**2 + normal[1]**2 + normal[2]**2)**(1.0/2)
    Nnormal = [normal[0]/sqrtN, normal[1]/sqrtN, normal[2]/sqrtN]

    # Normalize the lighting vector
    sqrtL = (L[0] ** 2 + L[1] ** 2 + L[2] ** 2) ** (1.0 / 2)
    Lnormal = [L[0] / sqrtL, L[1] / sqrtL, L[2] / sqrtL]

    # Find the dot product of the two normalized vectors
    NdotL = Nnormal[0] * Lnormal[0] + Nnormal[1] * Lnormal[1] + Nnormal[2] * Lnormal[2]

    # For each component of the intensity (RGB), we need to calculate the ambient, emitted, and specular reflection of
    # the point
    for i in range(3):
        # We start with calculating the ambient diffuse reflection (for this color)
        colorIntensity = Ia[i] * Kd[i]

        # Then we need to calculate the emitted diffuse reflection next and add it to the other intensity we just found
        colorIntensity += (Ip[i] * Kd[i] * NdotL)

        # We need to determine the reflection vector for specular reflection
        R = computeR(Nnormal, Lnormal, NdotL)

        # Then we normalize the reflection vector
        sqrtR = (R[0] ** 2 + R[1] ** 2 + R[2] ** 2) ** (1.0 / 2)
        Rnormal = [R[0] / sqrtR, R[1] / sqrtR, R[2] / sqrtR]

        # And normalize the viewing vector
        sqrtV = (V[0] ** 2 + V[1] ** 2 + V[2] ** 2) ** (1.0 / 2)
        Vnormal = [V[0] / sqrtV, V[1] / sqrtV, V[2] / sqrtV]

        # Find the dot product of them both
        VdotR = Vnormal[0] * Rnormal[0] + Vnormal[1] * Rnormal[1] + Vnormal[2] * Rnormal[2]

        # And finally calculate the intensity of the specular reflection
        colorIntensity += Ip[i] * Ks[i] * (VdotR ** N)

        # At the end of it all, we add the final color intensity to the list of color intensities for the point
        finalIntensity.append(round(colorIntensity * 255))

    # Finally return the intensity list of the point
    return finalIntensity


# This function computes the reflection vector
def computeR(Nnormal, Lnormal, NdotL):
    # Let's just go ahead and initialize R and compute 2 * theta(phi)
    R = []
    tcphi = 2 * NdotL

    # Determine R based off of the value of 2 * theta(phi)
    if tcphi > 0:
        for i in range(3):
            R.append(Nnormal[i] - Lnormal[i] / tcphi)

    elif tcphi == 0:
        for i in range(3):
            R.append(-Lnormal[i])

    else:
        for i in range(3):
            R.append(-Nnormal[i] + Lnormal[i] / tcphi)

    # Return R (I'm done)
    return R


# ***************************** Interface Functions ***************************
# Everything below this point implements the interface

# This function is tied to the render button
def render():
    print("Render function entered")
    # Center of Projection Vector (xs, ys, zs)
    cop = [0, 0, -800]
    # Maximum ray depth for reflecting object
    depth = 5

    # Screen X
    for pixel_x in range(1, CanvasWidth, 1):
        # Adjust the screen center
        screen_x = pixel_x - (CanvasWidth / 2)

        for pixel_y in range(1, CanvasHeight, 1):
            # Adjust the screen center
            screen_y = (CanvasHeight / 2) - pixel_y

            # Compute vector for ray from center of projection through pixel (ray_i, ray_j, ray_k)
            ray = [screen_x - cop[0], screen_y - cop[1], 0 - cop[2]]

            # Trace the ray through the environment to obtain the pixel color
            intensity = [0, 0, 0]
            fillColorPercent = trace_ray(depth, cop, ray, intensity)

            # Convert the fill color to a string of hex values
            fillColor = "#"
            for i in range(3):
                fillColorHex = hex(round(fillColorPercent[i])).split('x')[-1]

                if len(fillColorHex) < 2:
                    fillColorHex = "0%s" % fillColorHex
                elif len(fillColorHex) > 2:
                    fillColorHex = "FF"

                fillColor += fillColorHex

            # Finally color the pixel
            w.create_rectangle(pixel_x, pixel_y, pixel_x, pixel_y, fill="", outline=fillColor)
        w.update()


# This function is tied to the quit button
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
controlpanel = Frame(outerframe, relief=RIDGE, borderwidth=4)
controlpanel.pack(expand=True, fill=BOTH)

# Render Button Block
rendercontrols = Frame(controlpanel, height=100, relief=RIDGE, borderwidth=2)
rendercontrols.pack(side=LEFT)

rendercontrolslabel = Label(rendercontrols, text="Render")
rendercontrolslabel.pack()

renderButton = Button(rendercontrols, text="GO!", fg="green", command=render)
renderButton.pack()

# Quit Button Block
quitcontrols = Frame(controlpanel, height=100, relief=RIDGE, borderwidth=2)
quitcontrols.pack(side=RIGHT)

quitcontrolslabel = Label(quitcontrols, text="Quit")
quitcontrolslabel.pack()

quitButton = Button(quitcontrols, text="GET ME OUTTA HERE!!", fg="red", command=quit)
quitButton.pack()

root.mainloop()