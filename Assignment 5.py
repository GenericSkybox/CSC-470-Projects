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

"""
From here on down is all of the C++ code that Dr. O'Neal used in his project

#include <stdio.h>
#include <math.h>

#include <suntool/sunview.h>
#include <suntool/panel.h>
#include <suntool/canvas.h>
#include <suntool/scrollbar.h>
#include <suntool/seln.h>

static short icon_image[] = {
#include </user/include/images/core_eye.icon>
};

DEFINE_ICON_FROM_IMAGE(render_icon, icon_image);

Window frame;
Canvas canvas_sw, panel_sw;

Pixwin *pw;
Scrollbar bar1, bar2;

static void render_proc(), quit_proc();

main(argc, argv)
int argc; char **argv;

{
    frame = window_create(  NULL, FRAME,
                            FRAME_LABEL,    "Example Canvas",
                            FRAME_ICON,     &render_icon,
                            WIN_WIDTH,      600,
                            WIN_HEIGHT,     600,
                            FRAME_ARGS,     argc, argv,
                            0);
    
    panel_sw = window_create(frame, PANEL, 0);
    
    panel_create_item(  panel_sw, PANEL_BUTTON,
                        PANEL_LABEL_IMAGE, panel_button_image(panel_sw, "Render", 6, 0),
                        PANEL_NOTIFY_PROC, render_proc,
                        0);
    
    panel_create_item(  panel_sw, PANEL_BUTTON,
                        PANEL_LABEL_IMAGE, panel_button_image(panel_sw, "Quit", 4, 0),
                        PANEL_NOTIFY_PROC, quit_proc,
                        0);
                        
    window_fit_height(panel_sw);
    
    bar1 = scrollbar_create(SCROLL_PLACEMENT,   SCROLL_WEST,
                            SCROLL_LINE_HEIGHT, 4,
                            0);
    
    bar2 = scrollbar_create(SCROLL_PLACEMENT,   SCROLL_NORTH,
                            SCROLL_DIRECTION,   SCROLL_HORIZONTAL,
                            SCROLL_LINE_HEIGHT, 4,
                            0);
    
    canvas_sw = window_create(  frame,                      CANVAS,
                                WIN_BELOW,                  panel_sw,
                                CANVAS_AUTO_SHRINK,         FALSE,
                                CANVAS_WIDTH,               1200,
                                CANVAS_HEIGHT,              1200,
                                WIN_VERTICAL_SCROLLBAR,     bar1,
                                WIN_HORIZONTAL_SCROLLBAR,   bar2,
                                0);
    
    window_main_loop(frame);
    exit(0);
}

static void
render_proc(/* ARGS UNUSED */)
{
    static void setup_drawing_canvas();
    static void trace_ray();
    static void put_pixel();
    
    int pixel_x, pixel_y, screen_x, screen_y;
    double xs, ys, zs;          /* center of projection */
    int ray_i, ray_j, ray_k;    /* vector for light entering eye */
    int ir, ig, ib;             /* intensity of red, green, and blue primaries */
    int depth;                  /* maximum ray depth for reflecting objects */
    
    depth = 5;                  /* initialize maximum ray depth */
    
    setup_drawing_canvas();
    
    /* center of projection */
    xs = 0; ys = 0; zs = -800;
    
    for ( pixel_x = 1; pixel_x <=1200; pixel_x++)
    {
        pw_batch_on(pw);        /* batch a vertical swipe */
        screen_x = pixel_x - 600;
        for ( pixel_y = 1; pixel_y <= 1200; pixel_y++)
        {
            screen_y = 600 - pixel_y;
            
            /* compute vector for ray from center of projection through pixel */
            ray_i = screen_x - xs;
            ray_j = screen_y - ys;
            ray_k = 0 - zs;
            
            /* trace the ray through the environment to obtain the pixel color */
            trace_ray(  0, depth, xs, ys, zs,
                        (double) ray_i, (double) ray_j, (double) ray_k,
                        &ir, &ig, &ib);
            
            put_pixel(pixel_x, pixel_y, ir, ig, ib);
        }
        pw_batch_off(pw);       /* end of vertical swipe */
    }
}

static void
trace_ray(flag, level, xs, ys, zs, ray_i, ray_j, ray_k, ir, ig, ib)
int flag, level;
double xs, ys, zs, ray_i, ray_j, ray_k;
int *ir, *ig, *ib;
{
    static int sphere1_intersection();
    static int sphere2_intersection();
    static int checkerboard_intersection();
    static void checkerboard_point_intensity();
    static void sphere1_point_intensity();
    static void sphere2_point_intensity();
    
    double t;                   /* distance of closest object */
    double intersect_x;
    double intersect_y;         /* intersection point of ray and object */
    double intersect_z;
    double obj_normal_x;
    double obj_normal_y;        /* normal of closest object at intersect point */
    double obj_normal_z;
    int object_code;            /* integer code for the intersected object */
    int object_r, object_g, object_b;   /* RGB values of an object */
    
    if (level == 0)
    {
        /* maximum depth exceeded -- return black */
        *ir = 0; *ig = 0; *ib = 0;
    }
    else
    {
        
    }
}
"""