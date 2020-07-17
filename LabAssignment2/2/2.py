import glfw
from OpenGL.GL import *
import numpy as np
import math

num = -1

def begin():
    if num==-1:
        glBegin(GL_LINE_LOOP)
    elif num==1:
        glBegin(GL_POINTS)
    elif num==2:
        glBegin(GL_LINES)
    elif num==3:
        glBegin(GL_LINE_STRIP)
    elif num==4:
        glBegin(GL_LINE_LOOP)
    elif num==5:
        glBegin(GL_TRIANGLES)
    elif num==6:
        glBegin(GL_TRIANGLE_STRIP)
    elif num==7:
        glBegin(GL_TRIANGLE_FAN)
    elif num==8:
        glBegin(GL_QUADS)
    elif num==9:
        glBegin(GL_QUAD_STRIP)
    elif num==0:
        glBegin(GL_POLYGON)

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    begin()
    t = np.linspace(0, 2*math.pi, 13)
    x = np.cos(t)
    y = np.sin(t)
    for i in range(12):
        glVertex2f(x[i], y[i])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global num
    if action==glfw.PRESS:
        if key==glfw.KEY_1:
            num = 1
        elif key==glfw.KEY_2:
            num = 2
        elif key==glfw.KEY_3:
            num = 3
        elif key==glfw.KEY_4:
            num = 4
        elif key==glfw.KEY_5:
            num = 5
        elif key==glfw.KEY_6:
            num = 6
        elif key==glfw.KEY_7:
            num = 7
        elif key==glfw.KEY_8:
            num = 8
        elif key==glfw.KEY_9:
            num = 9
        elif key==glfw.KEY_0:
            num = 0
    

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2018008613", None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)

    # Make the window's context current
    glfw.make_context_current(window)
    
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        
        # Render here, e.g. using pyOpenGL
        render()
        
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
