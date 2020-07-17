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
        

def render(): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity() 
 
    # draw cooridnates 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.])) 
    glEnd() 
 
    glColor3ub(255, 255, 255) 
 
    ########################### 
    # implement here
    F()
    ########################### 
 
    drawTriangle() 
 
def drawTriangle(): 
    glBegin(GL_TRIANGLES) 
    glVertex2fv(np.array([0.,.5])) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([.5,0.])) 
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global l
    if action==glfw.PRESS:
        if key==glfw.KEY_Q:
            #glTranslatef(-0.1, 0, 0)
            l = [1] + l
        elif key==glfw.KEY_E:
            #glTranslatef(0.1, 0, 0)
            l = [2] + l
        elif key==glfw.KEY_A:
            #glRotatef(10, 0, 0, 1)
            l = [3] + l
        elif key==glfw.KEY_D:
            #glRotatef(350, 0, 0, 1)
            l = [4] + l
        elif key==glfw.KEY_1:
            l=list()
            


def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480, '2018008613', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
