import glfw
from OpenGL.GL import *
import numpy as np

R = np.array([[1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]])

def render(T): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity() 
    # draw cooridnate 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.])) 
    glEnd() 
    # draw triangle 
    glBegin(GL_TRIANGLES) 
    glColor3ub(255, 255, 255) 
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] ) 
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] ) 
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] ) 
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global R
    if action==glfw.PRESS:
        if key==glfw.KEY_W:
            R = np.array([[0.9, 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]]) @ R
        elif key==glfw.KEY_E:
            R = np.array([[1.1, 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]]) @ R
        elif key==glfw.KEY_S:
            th = np.radians(10)
            R = np.array([[np.cos(th), -np.sin(th), 0.],
            [np.sin(th), np.cos(th), 0.],
            [0., 0., 1.]]) @ R
        elif key==glfw.KEY_D:
            th = np.radians(350)
            R = np.array([[np.cos(th), -np.sin(th), 0.],
            [np.sin(th), np.cos(th), 0.],
            [0., 0., 1]]) @ R
        elif key==glfw.KEY_X:
            R = np.array([[1., -0.1, 0.],
            [0., 1., 0.],
            [0., 0., 1.]]) @ R
        elif key==glfw.KEY_C:
            R = np.array([[1., 0.1, 0.],
            [0., 1., 0],
            [0., 0., 1]]) @ R
        elif key==glfw.KEY_R:
            R = np.array([[1., 0., 0.],
            [0., -1., 0.],
            [0., 0., 1.]]) @ R
        elif key==glfw.KEY_1:
            R = np.array([[1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]])

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2018008613", None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)


    # set the number of screen refresh to wait before calling glfw.swap_buffer().
    # if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        global R
        render(R)


        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
