import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

l = list()

def F():
    for i in l:
        if(i == 1):
            glTranslatef(-0.1, 0, 0)
        elif(i == 2):
            glTranslatef(0.1, 0, 0)
        elif(i == 3):
            glRotatef(10, 0, 0, 1)
        elif(i == 4):
            glRotatef(350, 0, 0, 1)
        

def render(M): 
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
 
    glColor3ub(255, 255, 255) 
 
    # draw point p 
    glBegin(GL_POINTS) 
    # your implementation
    glVertex2fv(M @ np.array([1,0.0]))
    glEnd() 
 
    # draw vector v 
    glBegin(GL_LINES) 
    # your implementation
    glVertex2fv(M @ np.array([0, 0.0]))
    glVertex2fv(M @ np.array([0.5,0.0]))
    glEnd()    


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, '2018008613', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        t = glfw.get_time()

        th = t
        M = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])
        
        render(M)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
