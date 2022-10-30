import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

def startup():
    glClearColor(0.5, 0.5, 0.5, 1.0)
    update_viewport(None, 800, 800)

def shutdown():
    pass

def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if (width <= height):
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio, 1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # print_basic_triangles()
    # print_rectangle(0, 0, 40, 20)
    # print_fancy_rectange(-50, 50, 40, 20, 2)
    # print_carpet(-50, 50, 100, 100, 5)
    print_triangle_carpet(-50, 0, 0, 50, 50, 0, 4)

    glFlush()

def print_basic_triangles():
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(0.5, 0.5, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.0, 0.0)
    glColor3f(0.5, 0.0, 0.5)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

def print_rectangle(x, y, width, height, red = 0.0, green = 0.0, blue = 0.0):
    glColor3f(red, green, blue)

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x, y - height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y - height)
    glVertex2f(x, y - height)
    glEnd()

def print_fancy_rectange(x, y, width, height, scale = 1.0):
    NWcolorR = random.randint(0, 255) / 255
    NWcolorG = random.randint(0, 255) / 255
    NWcolorB = random.randint(0, 255) / 255
    NEcolorR = random.randint(0, 255) / 255
    NEcolorG = random.randint(0, 255) / 255
    NEcolorB = random.randint(0, 255) / 255
    SWcolorR = random.randint(0, 255) / 255
    SWcolorG = random.randint(0, 255) / 255
    SWcolorB = random.randint(0, 255) / 255
    SEcolorR = random.randint(0, 255) / 255
    SEcolorG = random.randint(0, 255) / 255
    SEcolorB = random.randint(0, 255) / 255
    width = width * scale
    height = height * scale

    glBegin(GL_TRIANGLES)
    glColor3f(NWcolorR, NWcolorG, NWcolorB)
    glVertex2f(x, y)
    glColor3f(NEcolorR, NEcolorG, NEcolorB)
    glVertex2f(x + width, y)
    glColor3f(SWcolorR, SWcolorG, SWcolorB)
    glVertex2f(x, y - height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(NEcolorR, NEcolorG, NEcolorB)
    glVertex2f(x + width, y)
    glColor3f(SEcolorR, SEcolorG, SEcolorB)
    glVertex2f(x + width, y - height)
    glColor3f(SWcolorR, SWcolorG, SWcolorB)
    glVertex2f(x, y - height)
    glEnd()

def print_carpet(x, y, width, height, dapth):
    print_rectangle(x, y, width, height, 1, 1, 1)
    # print_fancy_rectange(x, y, width, height, 1)
    print_carpet_part(x, y, width, height, dapth)

def print_carpet_part(x, y, width, height, depth):
    shift_x = width / 3
    shift_y = height / 3
    print_rectangle(x + shift_x, y - shift_y, width / 3, height / 3 , 0.5, 0.5, 0.5)

    if (depth > 1):
        newWidth = width / 3
        newHeight = height / 3
        newDepth = depth - 1
        print_carpet_part(x, y, newWidth, newHeight, newDepth)
        print_carpet_part(x + shift_x, y, newWidth, newHeight, newDepth)
        print_carpet_part(x + 2 * shift_x, y, newWidth, newHeight, newDepth)
        print_carpet_part(x, y - shift_y, newWidth, newHeight, newDepth)
        print_carpet_part(x, y - 2 * shift_y, newWidth, newHeight, newDepth)
        print_carpet_part(x + 2 * shift_x, y - shift_y, newWidth, newHeight, newDepth)
        print_carpet_part(x + shift_x, y - 2 * shift_y, newWidth, newHeight, newDepth)
        print_carpet_part(x + 2 * shift_x, y - 2 * shift_y, newWidth, newHeight, newDepth)

def print_triangle_carpet(x1, y1, x2, y2, x3, y3, depth):
    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()
    print_triangle_carpet_part(x1, y1, x2, y2, x3, y3, depth)

def print_triangle_carpet_part(x1, y1, x2, y2, x3, y3, depth):
    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex2f((x1 + x2) / 2, (y1 + y2) / 2)
    glVertex2f((x2 + x3) / 2, (y2 + y3) / 2)
    glVertex2f((x3 + x1) / 2, (y3 + y1) / 2)
    glEnd()

    if (depth > 0):
        newDepth = depth - 1
        print_triangle_carpet_part(x1, y1, (x1 + x2) / 2, (y1 + y2) / 2, (x1 + x3) / 2, (y1 + y3) / 2, newDepth)
        print_triangle_carpet_part(x2, y2, (x2 + x3) / 2, (y2 + y3) / 2, (x2 + x1) / 2, (y2 + y1) / 2, newDepth)
        print_triangle_carpet_part(x3, y3, (x3 + x1) / 2, (y3 + y1) / 2, (x3 + x2) / 2, (y3 + y2) / 2, newDepth)

def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(800, 800, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwWaitEvents()
    shutdown()

    glfwTerminate()

if __name__ == '__main__':
    main()
