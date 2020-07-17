import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

#Orbit을 위한 변수
gCamAng = 0.
gCamHeight = 0.
left_m = 0
#Panning을 위한 변수
right_m = 0
dx = 0.
dy = 0.
#Orbit과 Panning을 위한 변수
befx = 0.
befy = 0.
#Zooming을 위한 변수
dz = 0.
#gluLookat을 위한 변수
eye = np.array([0.,3.,3.])
at = np.array([0.,0.,0.])

def render():
    global dx, dy, dz, eye, at, gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    #Panning, Zooming
    up = np.array([0.,1.,0.])
    w = eye - at
    w = w / np.sqrt( np.dot(w, w) )
    u = np.cross(up, w)
    u = u / np.sqrt( np.dot(u, u) )
    v = np.cross(w, u)
    v = v / np.sqrt( np.dot(v, v) )
    u = u * dx
    v = v * dy
    w = w * dz
    dx = 0.
    dy = 0.
    dz = 0.
    eye[0] += (u[0] + v[0] + w[0])
    eye[1] += (u[1] + v[1] + w[1])
    eye[2] += (u[2] + v[2] + w[2])
    at[0] += (u[0] + v[0])
    at[1] += (u[1] + v[1])
    at[2] += (u[2] + v[2])

    #Orbit
    deye = eye
    deye[0] = eye[0]-at[0]
    deye[1] = eye[1]-at[1]
    deye[2] = eye[2]-at[2]
    deye = deye @ np.array([[1.,0.,0.],
                            [0.,np.cos(gCamHeight),-np.sin(gCamHeight)],
                            [0.,np.sin(gCamHeight), np.cos(gCamHeight)]])
    deye = deye @ np.array([[np.cos(gCamAng),0.,np.sin(gCamAng)],
                            [0.,1.,0.],
                            [-np.sin(gCamAng),0., np.cos(gCamAng)]])
    
    deye[0] += at[0]
    deye[1] += at[1]
    deye[2] += at[2]
    eye = deye
    
    gCamHeight = 0
    gCamAng = 0
    
    
    gluLookAt(eye[0], eye[1], eye[2], at[0], at[1], at[2], 0, 1, 0)

    #hierarchical model
    glMatrixMode(GL_MODELVIEW)  
    drawFrame()
    glColor3ub(255, 255, 255)
    drawXZ()
    t = glfw.get_time() 
 
    # blue base transformation 
    glPushMatrix() 
    glTranslatef(np.sin(t), 0, 0) 
 
    # blue base drawing 
    glPushMatrix()
    glScalef(.2, .2, .2) 
    glColor3ub(0, 0, 255)
    drawUnitCube()
    glPopMatrix() 
 
    # red arm transformation 
    glPushMatrix() 
    glRotatef(t*(180/np.pi), 0, 0, 1) 
    glTranslatef(.2, 0, 0.) 
 
    # red arm drawing 
    glPushMatrix()
    glScalef(.2, .04, .04) 
    glColor3ub(255, 0, 0) 
    drawUnitCube()
    glPopMatrix()

    #green arm transformation
    glPushMatrix()
    glTranslatef(.1, 0, 0)
    glRotatef(t*(180/np.pi), 0, 0, 1)

    #green arm drawing
    glPushMatrix()
    glScalef(.1, .1, .1)
    glColor3ub(0, 255, 0)
    drawUnitCube()
    
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

    # red arm transformation 
    glPushMatrix() 
    glRotatef(t*(180/np.pi), 0, 0, 1) 
    glTranslatef(0., .2, 0.) 
 
    # red arm drawing 
    glPushMatrix()
    glScalef(.04, .2, .04) 
    glColor3ub(255, 0, 0) 
    drawUnitCube()
    glPopMatrix()

    #green arm transformation
    glPushMatrix()
    glTranslatef(0., .1, 0)
    glRotatef(t*(180/np.pi), 0, 0, 1)

    #green arm drawing
    glPushMatrix()
    glScalef(.1, .1, .1)
    glColor3ub(0, 255, 0)
    drawUnitCube()
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()

    # red arm transformation 
    glPushMatrix() 
    glRotatef(t*(180/np.pi), 0, 0, 1) 
    glTranslatef(-0.2, 0, 0.) 
 
    # red arm drawing 
    glPushMatrix()
    glScalef(.2, .04, .04) 
    glColor3ub(255, 0, 0) 
    drawUnitCube()
    glPopMatrix()

    #green arm transformation
    glPushMatrix()
    glTranslatef(-0.1, 0, 0)
    glRotatef(t*(180/np.pi), 0, 0, 1)

    #green arm drawing
    glPushMatrix()
    glScalef(.1, .1, .1)
    glColor3ub(0, 255, 0)
    drawUnitCube()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

    # red arm transformation 
    glPushMatrix() 
    glRotatef(t*(180/np.pi), 0, 0, 1) 
    glTranslatef(0., -0.2, 0.) 
 
    # red arm drawing 
    glPushMatrix()
    glScalef(.04, .2, .04) 
    glColor3ub(255, 0, 0) 
    drawUnitCube()
    glPopMatrix()

    #green arm transformation
    glPushMatrix()
    glTranslatef(0., -0.1, 0)
    glRotatef(t*(180/np.pi), 0, 0, 1)

    #green arm drawing
    glPushMatrix()
    glScalef(.1, .1, .1)
    glColor3ub(0, 255, 0)
    drawUnitCube()
    glPopMatrix()

    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()


def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()
 
def drawBox(): 
    glBegin(GL_QUADS) 
    glVertex3fv(np.array([1,1,0.])) 
    glVertex3fv(np.array([-1,1,0.])) 
    glVertex3fv(np.array([-1,-1,0.])) 
    glVertex3fv(np.array([1,-1,0.])) 
    glEnd() 

def drawX():
    glBegin(GL_LINES)
    glVertex3f(-10, 0.,0)
    glVertex3f(10, 0.,0)
    glEnd()

def drawZ():
    glBegin(GL_LINES)
    glVertex3f(0, 0.,10)
    glVertex3f(0, 0.,-10)
    glEnd()

def drawXZ():
    for i in range(50):
        glPushMatrix()
        glTranslatef(0,0, i * 0.2)
        #glScalef(.5,.5,.5)
        drawX()
        glPopMatrix()
    for i in range(50):
        glPushMatrix()
        glTranslatef(0,0, -i * 0.2)
        #glScalef(.5,.5,.5)
        drawX()
        glPopMatrix()
    for i in range(50):
        glPushMatrix()
        glTranslatef(i * 0.2,0, 0)
        #glScalef(.5,.5,.5)
        drawZ()
        glPopMatrix()
    for i in range(50):
        glPushMatrix()
        glTranslatef(-i * 0.2,0, 0)
        #glScalef(.5,.5,.5)
        drawZ()
        glPopMatrix()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([-10.,0.,0.]))
    glVertex3fv(np.array([10.,0.,0.]))
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,10]))
    glVertex3fv(np.array([0.,0.,-10.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

def cursor_callback(window, xpos, ypos):
    global left_m, right_m, befx, befy, gCamAng, gCamHeight, dx, dy
    #Orbit
    if left_m == 1:
        gCamAng = np.radians((xpos - befx) /5)
        gCamHeight = np.radians((ypos - befy) / 5)
    #Panning
    elif right_m == 1:
        dx = -(xpos - befx) / 200
        dy = (ypos - befy) / 200
    befx = xpos
    befy = ypos
    

def button_callback(window, button, action, mod):
    global left_m, right_m
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            left_m = 1
        elif action==glfw.RELEASE:
            left_m = 0
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            right_m = 1
        elif action==glfw.RELEASE:
            right_m = 0
     
def scroll_callback(window, xoffset, yoffset):
    global dz
    #Zooming
    if yoffset == 1:
        #휠을 위로 올릴때
        dz -= 0.1
    elif yoffset == -1:
        #휠을 아래로 내릴때
        dz += 0.1

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000,1000,'2018008613', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
