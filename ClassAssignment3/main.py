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

drag_mode = 0
space_mode = 0
motion_cnt = 0

def render():
    global dx, dy, dz, eye, at, gCamAng, gCamHeight, space_mode, motion_cnt, drag_mode, frame_time, frame_num, pop_push_matrix, offset_matrix, channel_cnt_matrix, channel_type_matrix, channel_value_matrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
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
    drawFrame()
    glColor3ub(255, 255, 255)
    drawXZ()

    #Light
    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object

    # light position
    glPushMatrix()
    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    
    lightColor = (0.,0.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    objectColor = (0,0,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    glColor3ub(0, 0, 255)
    offset_idx = 3
    channel_cnt_idx = 0
    channel_type_idx = 0
    if drag_mode == 1:
        if space_mode == 0:
            for i in pop_push_matrix:
                if i == 1:
                    glPushMatrix()
                elif i == 2:
                    glPushMatrix()
                    x = offset_matrix[offset_idx]
                    offset_idx += 1
                    y = offset_matrix[offset_idx]
                    offset_idx += 1
                    z = offset_matrix[offset_idx]
                    offset_idx += 1
                    drawUnitCube(x, y, z)
                    glTranslatef(x, y, z)
                elif i == 3:
                    glPushMatrix()
                    x = offset_matrix[offset_idx]
                    offset_idx += 1
                    y = offset_matrix[offset_idx]
                    offset_idx += 1
                    z = offset_matrix[offset_idx]
                    offset_idx += 1
                    drawUnitCube(x, y, z)
                    glTranslatef(x, y, z)
                elif i == -1:
                    glPopMatrix()    
        else: 
            for i in pop_push_matrix:
                if i == 1:
                    glPushMatrix()
                    this_channel_cnt = channel_cnt_matrix[channel_cnt_idx]
                    channel_cnt_idx += 1
                    for j in range(0,int(this_channel_cnt)):
                        if channel_type_matrix[channel_type_idx] == 1:
                            glTranslatef(channel_value_matrix[motion_cnt][channel_type_idx]/100, 0, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 2:
                            glTranslatef(0, channel_value_matrix[motion_cnt][channel_type_idx]/100, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 3:
                            glTranslatef(0, 0, channel_value_matrix[motion_cnt][channel_type_idx]/100)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 4:
                            glRotatef(channel_value_matrix[motion_cnt][channel_type_idx], 1, 0, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 5:
                            glRotatef(channel_value_matrix[motion_cnt][channel_type_idx], 0, 1, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 6:
                            glRotatef(channel_value_matrix[motion_cnt][channel_type_idx], 0, 0, 1)
                            channel_type_idx += 1
                elif i == 2:
                    glPushMatrix()
                    
                    x = offset_matrix[offset_idx]
                    offset_idx += 1
                    y = offset_matrix[offset_idx]
                    offset_idx += 1
                    z = offset_matrix[offset_idx]
                    offset_idx += 1
                    drawUnitCube(x, y, z)
                    glTranslatef(x, y, z)
                    this_channel_cnt = channel_cnt_matrix[channel_cnt_idx]
                    channel_cnt_idx += 1
                    for j in range(0,int(this_channel_cnt)):
                        if channel_type_matrix[channel_type_idx] == 1:
                            glTranslatef(channel_value_matrix[motion_cnt][channel_type_idx]/100, 0, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 2:
                            glTranslatef(0, channel_value_matrix[motion_cnt][channel_type_idx]/100, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 3:
                            glTranslatef(0, 0, channel_value_matrix[motion_cnt][channel_type_idx]/100)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 4:
                            glRotatef(channel_value_matrix[motion_cnt][channel_type_idx], 1, 0, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 5:
                            glRotatef(channel_value_matrix[motion_cnt][channel_type_idx], 0, 1, 0)
                            channel_type_idx += 1
                        elif channel_type_matrix[channel_type_idx] == 6:
                            glRotatef(channel_value_matrix[motion_cnt][channel_type_idx], 0, 0, 1)
                            channel_type_idx += 1
                elif i == 3:
                    glPushMatrix() 
                    x = offset_matrix[offset_idx]
                    offset_idx += 1
                    y = offset_matrix[offset_idx]
                    offset_idx += 1
                    z = offset_matrix[offset_idx]
                    offset_idx += 1
                    drawUnitCube(x, y, z)
                    glTranslatef(x, y, z)
                    
                elif i == -1:
                    glPopMatrix()
            if motion_cnt < frame_num - 1:
                motion_cnt += 1

    glPopMatrix()

    glDisable(GL_LIGHTING)

    

def drawUnitCube(x, y, z):
    cubelen = np.sqrt(x*x + y*y + z*z)
    L1 = np.sqrt(x*x + y*y)
    L2 = x
    th1 = np.arccos(L1/cubelen)
    th2 = np.arccos(L2/L1)
    if x==0 and y==0:
        th2 = 0
    else:
        th2 = np.arccos(L2/L1)
    if y < 0:
        th2 = -th2
    if z > 0:
        th1 = -th1
    

    glPushMatrix()
    glRotatef(np.degrees(th2), 0, 0, 1)
    glRotatef(np.degrees(th1), 0, 1, 0)
    
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 255)

    glNormal3f(-1,0,0)
    glVertex3f( 0, 0.02, 0.02)
    glVertex3f( 0, 0.02, -0.02)
    glVertex3f( 0, -0.02, -0.02)
    glVertex3f( 0, -0.02, 0.02)

    glNormal3f(1,0,0)                     
    glVertex3f( cubelen, 0.02, 0.02)
    glVertex3f( cubelen, 0.02, -0.02)
    glVertex3f( cubelen, -0.02, -0.02)
    glVertex3f( cubelen, -0.02, 0.02) 

    glNormal3f(0,-1,0)                        
    glVertex3f( 0, -0.02, -0.02)
    glVertex3f( 0, -0.02, 0.02)
    glVertex3f( cubelen, -0.02, 0.02)
    glVertex3f( cubelen, -0.02, -0.02)

    glNormal3f(0,0,1)                         
    glVertex3f( 0, -0.02, 0.02)
    glVertex3f( 0, 0.02, 0.02)
    glVertex3f( cubelen, 0.02, 0.02)
    glVertex3f( cubelen, -0.02, 0.02)

    glNormal3f(0,1,0)
    glVertex3f( 0, 0.02, -0.02)
    glVertex3f( 0, 0.02, 0.02)
    glVertex3f( cubelen, 0.02, 0.02)
    glVertex3f( cubelen, 0.02, -0.02)

    glNormal3f(0,0,-1)                           
    glVertex3f( 0, 0.02, -0.02)
    glVertex3f( 0, -0.02, -0.02)
    glVertex3f( cubelen, -0.02, -0.02)
    glVertex3f( cubelen, 0.02, -0.02)
    glEnd()
    glPopMatrix()
 
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
        elif key==glfw.KEY_SPACE:
            global space_mode
            space_mode = 1

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

def drop_callback(window, paths):
    global drag_mode, frame_num, frame_time, pop_push_matrix, offset_matrix, channel_cnt_matrix, channel_type_matrix,channel_value_matrix
    f = open(paths[0], 'r')
    sp = paths[0].split('\\')
    l = len(sp)
    print("File name is " + sp[l - 1])
    check_motion = 0
    pop_push_matrix = np.zeros(100000)
    pop_push_num = 0
    offset_matrix = np.zeros(100000)
    offset_matrix_num = 0
    channel_cnt_matrix = np.zeros(100000)
    channel_cnt_matrix_num = 0
    channel_type_matrix = np.zeros(100000)
    channel_type_matrix_num = 0
    channel_value_matrix = np.zeros(100000)
    frame_num = 0
    frame_time = 0
    joint_num = 0
    total_channel_num = 0
    motion_num = 0
    joint_list = np.zeros(1000, dtype="U20")
    while True:
        line = f.readline()
        if not line:
            break
        sp = line.split()
        if sp[0] == 'MOTION':
            check_motion = 1
            continue
        elif sp[0] == 'ROOT' or sp[0] == 'JOINT' or sp[0] == 'End':
            joint_list[joint_num] = sp[1]
            joint_num += 1
            pop_push_matrix[pop_push_num] = 3
            if sp[0] == 'ROOT':
                pop_push_matrix[pop_push_num] = 1
            elif sp[0] == 'JOINT':
                pop_push_matrix[pop_push_num] = 2
            pop_push_num += 1
        elif sp[0] == 'OFFSET':
            offset_matrix[offset_matrix_num] = float(sp[1])
            offset_matrix_num += 1
            offset_matrix[offset_matrix_num] = float(sp[2])
            offset_matrix_num += 1
            offset_matrix[offset_matrix_num] = float(sp[3])
            offset_matrix_num += 1
        elif sp[0] == 'CHANNELS':
            this_channel_num = int(sp[1])
            total_channel_num += this_channel_num
            channel_cnt_matrix[channel_cnt_matrix_num] = int(sp[1])
            channel_cnt_matrix_num += 1
            for i in range(2,2 + this_channel_num):
                if sp[i] == 'Xposition':
                    channel_type_matrix[channel_type_matrix_num] = 1
                    channel_type_matrix_num += 1
                elif sp[i] == 'Yposition':
                    channel_type_matrix[channel_type_matrix_num] = 2
                    channel_type_matrix_num += 1
                elif sp[i] == 'Zposition':
                    channel_type_matrix[channel_type_matrix_num] = 3
                    channel_type_matrix_num += 1
                elif sp[i] == 'Xrotation':
                    channel_type_matrix[channel_type_matrix_num] = 4
                    channel_type_matrix_num += 1
                elif sp[i] == 'Yrotation':
                    channel_type_matrix[channel_type_matrix_num] = 5
                    channel_type_matrix_num += 1
                elif sp[i] == 'Zrotation':
                    channel_type_matrix[channel_type_matrix_num] = 6
                    channel_type_matrix_num += 1
                
        elif sp[0] == '}':
            pop_push_matrix[pop_push_num] = -1
            pop_push_num += 1
        elif sp[0] == 'Frames:':
            frame_num = int(sp[1])
        elif sp[0] == 'Frame' and sp[1] == 'Time:':
            frame_time = float(sp[2])
            channel_value_matrix = np.zeros((frame_num, total_channel_num))
        elif check_motion == 1 and len(sp) == total_channel_num:
            for i in range(0, total_channel_num):
                channel_value_matrix[motion_num][i] = float(sp[i])
            motion_num += 1
    joint_list = joint_list[0:joint_num]
    print("Number of frames : " + str(frame_num))
    print("FPS : " + str(1/frame_time))
    print("Number of joints : " + str(joint_num))
    print("Joint list : ")
    print(joint_list)

    pop_push_matrix = pop_push_matrix[0:pop_push_num]
    offset_matrix = offset_matrix[0:offset_matrix_num]
    channel_cnt_matrix = channel_cnt_matrix[0:channel_cnt_matrix_num]
    channel_type_matrix = channel_type_matrix[0:channel_type_matrix_num]
    drag_mode = 1
    #for new example : too large x,y,z position
    offset_matrix = offset_matrix / 100
    
            
frame_time = 0
frame_num = 0
pop_push_matrix = None
offset_matrix = None
channel_cnt_matrix = None
channel_type_matrix = None
channel_value_matrix = None
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
    glfw.set_drop_callback(window, drop_callback)

    while not glfw.window_should_close(window):
        glfw.swap_interval(1)
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
