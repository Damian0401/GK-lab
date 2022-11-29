import sys

import math

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]
up = 1

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

scale = 1
R = 10

rotate_mode = 0


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    global theta
    global phi
    global R
    global up

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    fix_scale()

    if left_mouse_button_pressed:
        calculate_angles()

    if rotate_mode == 1:
        rotate_camera()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0, 0, 0, 
              0.0, up, 0.0)

    if rotate_mode == 0:
        rotate_object()

    axes()
    example_object()

    glFlush()


def calculate_angles():
    global theta
    global phi

    theta += delta_x * pix2angle
    phi += delta_y * pix2angle
    theta %= 360
    phi %= 360


def rotate_camera():
    fix_viewer()
    fix_up()


def rotate_object():
    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)
    glScalef(scale, scale, scale)


def fix_scale():
    global scale
    global R

    scale = 0.3 if scale < 0.3 else scale
    R = 3 if R < 3 else R
    scale = 1.5 if scale > 1.5 else scale
    R = 15 if R > 15 else R


def fix_up():
    global up

    if (phi > 90 and phi < 270):
        up = -1
    else:
        up = 1


def fix_viewer():
    global viewer
    global R

    viewer[0] = math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180) * R
    viewer[1] = math.sin(phi * math.pi / 180) * R
    viewer[2] = math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180) * R


def increase_size():
    global scale
    global R

    scale += 0.05
    R -= 0.5


def decrease_size():
    global scale
    global R

    scale -= 0.05
    R += 0.5


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global scale
    global R
    global rotate_mode

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_KP_ADD and action == GLFW_PRESS:
        increase_size()

    if key == GLFW_KEY_KP_SUBTRACT and action == GLFW_PRESS:
        decrease_size()

    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        rotate_mode = (rotate_mode + 1) % 2


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global scale
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


    if mouse_y_pos_old > y_pos and right_mouse_button_pressed == 1:
        increase_size()

    if mouse_y_pos_old < y_pos and right_mouse_button_pressed == 1:
        decrease_size()

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global scale

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
