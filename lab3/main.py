import sys
import math
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def spin(angle):
    angle = angle * 180 / math.pi
    glRotatef(angle, 1.0, 0.0, 0.0)
    # glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time)
    axes()

    N = 20
    random.seed(420)
    # print_point_egg(N)
    # print_line_egg(N)
    # print_triangle_egg(N)
    print_strip_egg(N)
    # print_triangle_carpet_3d(-2, -2, -1, 4, 3)

    glFlush()


def print_point_egg(N: int):
    points = calculate_egg_points(N)

    for i in range(N):
        for j in range(N):
            print_point_egg_part(points, i, j)


def print_point_egg_part(points: list, i: int, j: int):
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)

    glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])

    glEnd()


def print_line_egg(N: int):
    points = calculate_egg_points(N)
    
    for i in range(N):
        for j in range(N):
            print_line_egg_part(points, i, j, N)


def print_line_egg_part(points: list, i: int, j: int, N: int):
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)

    next_j = j + 1 if j + 1 < N else 0 
    glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
    glVertex3f(points[i][next_j][0], points[i][next_j][1], points[i][next_j][2])

    next_i = i + 1 if i + 1 < N else 0 
    glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
    glVertex3f(points[next_i][j][0], points[next_i][j][1], points[next_i][j][2])    

    glEnd()


def print_triangle_egg(N: int):
    points = calculate_egg_points(N)
    
    for i in range(N):
        for j in range(N):
            print_triangle_egg_part(points, i, j, N)


color_range = 30
colors = [[[random.random(), random.random(), random.random()] for _ in range(color_range)] for _ in range(color_range)]
def print_triangle_egg_part(points: list, i: int, j: int, N: int):
    next_i = i + 1 if i + 1 < N else 0
    next_j = j + 1 if j + 1 < N else 0

    glBegin(GL_TRIANGLES)

    glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
    glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
    glColor3f(colors[i][next_j][0], colors[i][next_j][1], colors[i][next_j][2])
    glVertex3f(points[i][next_j][0], points[i][next_j][1], points[i][next_j][2])
    glColor3f(colors[next_i][j][0], colors[next_i][j][1], colors[next_i][j][2])
    glVertex3f(points[next_i][j][0], points[next_i][j][1], points[next_i][j][2])

    glColor3f(colors[i][next_j][0], colors[i][next_j][1], colors[i][next_j][2])
    glVertex3f(points[i][next_j][0], points[i][next_j][1], points[i][next_j][2])
    glColor3f(colors[next_i][j][0], colors[next_i][j][1], colors[next_i][j][2])
    glVertex3f(points[next_i][j][0], points[next_i][j][1], points[next_i][j][2])
    glColor3f(colors[next_i][next_j][0], colors[next_i][next_j][1], colors[next_i][next_j][2])
    glVertex3f(points[next_i][next_j][0], points[next_i][next_j][1], points[next_i][next_j][2])

    glEnd()


def print_strip_egg(N: int):
    points = calculate_egg_points(N)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex3f(points[i][j][0], points[i][j][1], points[i][j][2])
            glColor3f(colors[i + 1][j][0], colors[i + 1][j][1], colors[i + 1][j][2])
            glVertex3f(points[i + 1][j][0], points[i + 1][j][1], points[i + 1][j][2])
        glEnd()


def calculate_egg_points(N: int):
    points = [[[0]  * 3 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        u = 1/(N-1) * i
        for j in range(N):
            v = 1/(N-1) * j
            points[i][j][0] = (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * math.cos(math.pi*v)
            points[i][j][1] = 160*u**4 - 320*u**3 + 160*u**2 - 5
            points[i][j][2] = (-90*u**5 + 225*u**4 - 270*u**3 + 180*u**2 - 45*u) * math.sin(math.pi*v)

    return points


def print_triangle_carpet_3d(x: int, y: int, z: int, length: int, depth: int):
    if depth == 1:
        print_pyramid(x, y, z, length)
        return

    half_length = length / 2
    next_depth = depth - 1

    print_triangle_carpet_3d(x, y, z, half_length, next_depth)
    print_triangle_carpet_3d(x, y + half_length, z, half_length, next_depth)
    print_triangle_carpet_3d(x + half_length, y, z, half_length, next_depth)
    print_triangle_carpet_3d(x + half_length, y + half_length, z, half_length, next_depth)
    print_triangle_carpet_3d(x + half_length / 2, y + half_length / 2, z + calculate_pyramid_height(half_length), half_length, next_depth)


def print_pyramid(x: int, y: int, z: int, length: int):
    pyramid_height = calculate_pyramid_height(length)
    pyramid_top_x = x + length / 2
    pyramid_top_y = y + length / 2
    pyramid_top_z = z + pyramid_height

    glBegin(GL_TRIANGLES)

    glColor3f(random.random(), random.random(), random.random())
    glVertex3f(x, y, z)
    glVertex3f(x, y + length, z)
    glVertex3f(x + length, y, z)

    glVertex3f(x, y + length, z)
    glVertex3f(x + length, y, z)
    glVertex3f(x + length, y + length, z)

    glColor3f(random.random(), random.random(), random.random())
    glVertex3f(x, y, z)
    glVertex3f(x, y + length, z)
    glVertex3f(pyramid_top_x, pyramid_top_y, pyramid_top_z)

    glColor3f(random.random(), random.random(), random.random())
    glVertex3f(x, y, z)
    glVertex3f(x + length, y, z)
    glVertex3f(pyramid_top_x, pyramid_top_y, pyramid_top_z)

    glColor3f(random.random(), random.random(), random.random())
    glVertex3f(x, y + length, z)
    glVertex3f(x + length, y + length, z)
    glVertex3f(pyramid_top_x, pyramid_top_y, pyramid_top_z)

    glColor3f(random.random(), random.random(), random.random())
    glVertex3f(x + length, y, z)
    glVertex3f(x + length, y + length, z)
    glVertex3f(pyramid_top_x, pyramid_top_y, pyramid_top_z)

    glEnd()


def calculate_pyramid_height(length: int):
    triangle_height = math.sqrt(length**2 - (length/2)**2)
    pyramid_height = math.sqrt(triangle_height**2 - (length/2)**2)
    return pyramid_height


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
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
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
