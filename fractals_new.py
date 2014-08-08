# a program to calculate fractals
import itertools
import numpy
import pyglet
import pyglet.graphics
import julia

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)
        
    def clear(self):
        self.x = None
        self.y = None
    
    def valid(self):
        if self.x and self.y:
            return True
        else:
            return False
    
class World(object):
    def __init__(self, julia_set, others, colors):
        self.julia_set = julia_set
        self.other_points = others
        self.colors = colors
    
    def set_attributes(self, x_origin, y_origin, width, size):
        self.x_origin = x_origin
        self.y_origin = y_origin
        self.width = width
        self.size = size
    
def number_in_julia_set(z, c):
    z_n = z
    for i in xrange(100):
        z_n = z_n**2 + c
        if abs(z_n) > 2:
            return i
    return True

def reverse_transform(x, y, x_origin, y_origin, width, screen_size):
    x = float(width) * x / screen_size + x_origin
    y = float(width) * y / screen_size + y_origin
    return [x, y]

def transform_coordinates(x, y, x_origin, y_origin, width, screen_size):
    x = (x - x_origin) / float(width) * screen_size
    y = (y - y_origin) / float(width) * screen_size
    return [x, y]

def get_julia_set(c, x_origin, y_origin, width, size):
    """ c - the c paramter in z = z^2 + c
        x, y - the coordinate of the lower left corner
        width - the width in coordinates of the space
        size - number of pixels wide"""
    x_space = numpy.linspace(x_origin, x_origin+width, size)
    y_space = numpy.linspace(y_origin, y_origin+width, size)
    
    colors = []
    other_points = []
    julia_set = []
    i = 0
    counter = 0
    for x, y in itertools.product(x_space, y_space):
        transformed = transform_coordinates(x, y, x_origin, y_origin, width, size)
        z = complex(x, y)
        result = julia.number_in_julia_set(z, c) 
        if result == True:
            julia_set.extend(transformed)
        else:
            other_points.extend(transformed)
            #red = int(-0.0255*result**2 + 5.1*result)
            red = int(result / 100. * 255)
            blue = 255 - red
            colors.extend([red, 0, blue, 255])
        i += 1
        if i % int(size**2 * 0.05) == 0:
            print "%.1f%%" % (i / float(size**2) * 100)

    return julia_set, other_points, colors

size = 700
window = pyglet.window.Window(size, size)
c = -0.757 + -0.164j
c2 = -0.116 + 0.895j
c3 = -0.01 + 0.651j
c4 = -0.15 + 1.0j
c5 = -0.52 + 0.57j

c = c5

x_origin = 0.0
y_origin = 0.0
width = 0.5

julia_set, other_points, colors = get_julia_set(c, x_origin, y_origin, width, size)
world = World(julia_set, other_points, colors)
world.set_attributes(x_origin, y_origin, width, size)

click_point = Point(None, None)
drag_point = Point(None, None)

@window.event
def on_draw():
    window.clear()
    #pyglet.graphics.draw(len(julia_set) / 2, pyglet.gl.GL_POINTS,
    #   ('v2f', julia_set)
    #)
    # Here just leave it the black of the background, so the actual set appears black
    pyglet.graphics.draw(len(world.other_points) / 2, pyglet.gl.GL_POINTS,
       ('v2f', world.other_points),
       ('c4B', world.colors)
    )
    
    if click_point.valid() and drag_point.valid():
        width1 = drag_point.x - click_point.x
        width2 = drag_point.y - click_point.y
        if abs(width1) > abs(width2):
            width = width1
        else:
            width = width2
        
        point1 = [click_point.x, click_point.y]
        point2 = [click_point.x+width, click_point.y]
        point3 = [click_point.x+width, click_point.y+width]
        point4 = [click_point.x, click_point.y+width]
        
        pyglet.graphics.draw(4, pyglet.gl.GL_LINE_LOOP,
           ('v2i', (point1 + point2 + point3 + point4)),
           ('c4B', (255, 255, 255, 255) * 4)   
        )
    
@window.event
def on_mouse_motion(x, y, dx, dy):
    real, imaginary = reverse_transform(x, y, world.x_origin, world.y_origin, world.width, world.size)
    # if imaginary >= 0:
#         print "%.3f + %.3fi" % (real, imaginary)
#     else:
#         print "%.3f - %.3fi" % (real, -imaginary)

@window.event
def on_mouse_press(x, y, button, modifiers):
    click_point.x = x
    click_point.y = y

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    drag_point.x = x
    drag_point.y = y
    
@window.event
def on_mouse_release(x, y, button, modifiers):
    width1 = drag_point.x - click_point.x
    width2 = drag_point.y - click_point.y
    if abs(width1) > abs(width2):
        box_width = width1
    else:
        box_width = width2
        
    new_x_origin, new_y_origin = reverse_transform(click_point.x, click_point.y, world.x_origin, world.y_origin, world.width, world.size)
    new_width = box_width * (world.width / world.size)

    julia_set, other_points, colors = get_julia_set(c, new_x_origin, new_y_origin, new_width, world.size)
    world.julia_set = julia_set
    world.other_points = other_points
    world.colors = colors
    world.set_attributes(new_x_origin, new_y_origin, new_width, size)
    
    print new_x_origin, new_y_origin
    print new_width
    
    click_point.clear()
    drag_point.clear()
    
pyglet.app.run()