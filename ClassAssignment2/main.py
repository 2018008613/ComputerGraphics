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
    global drop, dx, dy, dz, eye, at, gCamAng, gCamHeight, S_mode, Z_mode
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

    #Light
    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT7)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object

    # light position
    glPushMatrix()

    lightPos0 = (3.,4.,5.,1.)
    lightPos3 = (-3.,-4, 5.,0)
    lightPos7 = (3.,-4.,-5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT3, GL_POSITION, lightPos3)
    glLightfv(GL_LIGHT7, GL_POSITION, lightPos7)
    glPopMatrix()

    # light intensity for each color channel
    lightColor0 = (1,0,0,1.)
    ambientLightColor0 = (.2,.3,.1,1.)
    lightColor3 = (0,1,0,1.)
    ambientLightColor3 = (.1,.3,.2,1.)
    lightColor7 = (0,0,1,1.)
    ambientLightColor7 = (.3,.2,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, lightColor3)
    glLightfv(GL_LIGHT3, GL_SPECULAR, lightColor3)
    glLightfv(GL_LIGHT3, GL_AMBIENT, ambientLightColor3)
    glLightfv(GL_LIGHT7, GL_DIFFUSE, lightColor7)
    glLightfv(GL_LIGHT7, GL_SPECULAR, lightColor7)
    glLightfv(GL_LIGHT7, GL_AMBIENT, ambientLightColor7)

    # material reflectance for each color channel
    objectColor = (1,1,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()

    glColor3ub(0, 0, 255)
    
    if drop == 1:
        if S_mode == 0:
            if Z_mode == 0:
                drawCube_glDrawArray()
            else:
                w_drawCube_glDrawArray()
        else:
            if Z_mode == 0:
                drawCube_glDrawElements()
            else:
                w_drawCube_glDrawElements()

    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def w_drawCube_glDrawArray():
    global w_gVertexArraySeparate
    varr = w_gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_LINES, 0, int(varr.size/6))

def w_drawCube_glDrawElements():
    global w_gVertexArrayIndexed, w_gIndexArray
    varr = w_gVertexArrayIndexed
    iarr = w_gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_LINES, iarr.size, GL_UNSIGNED_INT, iarr)

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
    global gCamAng, gCamHeight, S_mode, Z_mode
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_S:
            S_mode = (S_mode + 1) % 2
        elif key==glfw.KEY_Z:
            Z_mode = (Z_mode + 1) % 2

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
    global w_sep, w_sep_cnt, w_ida, w_ida_cnt, drop, vertex_array, normal_array, sep, sep_cnt, ida, ida_cnt, gVertexArraySeparate, gVertexArrayIndexed, gIndexArray, w_gVertexArraySeparate, w_gVertexArrayIndexed, w_gIndexArray
    f = open(paths[0], 'r')
    sp = paths[0].split('\\')
    l = len(sp)
    print("File name is " + sp[l - 1])
    total_face = 0
    face_3 = 0
    face_4 = 0
    face_more = 0
    vertex_array = np.ones((1000,3))
    vertex_num = 0
    normal_array = np.ones((1000,3))
    normal_num = 0
    sep = np.ones((1000, 3))
    sep_cnt = 0
    ida = np.ones((1000, 3))
    ida_cnt = 0
    w_sep = np.ones((1000, 3))
    w_sep_cnt = 0
    w_ida = np.ones((1000, 2))
    w_ida_cnt = 0

    total_n = np.zeros((1000,3))
    avg_n = np.zeros((1000,3))
    total_cnt = np.zeros(1000)
    
    while True:
        line = f.readline()
        if not line:
            break
        sp = line.split()
        if sp[0] == 'v':
            va = np.array([float(sp[1]), float(sp[2]), float(sp[3])])
            if vertex_num >= len(vertex_array):
                vertex_array = np.resize(vertex_array,(2 * len(vertex_array), 3))
                total_n = np.resize(total_n,(2 * len(total_n), 3))
                avg_n = np.resize(avg_n,(2 * len(avg_n), 3))
                total_cnt = np.resize(total_cnt,2 * len(total_cnt))
            vertex_array[vertex_num] = va
            vertex_num += 1

        elif sp[0] == 'vn':
            va = np.array([float(sp[1]), float(sp[2]), float(sp[3])])
            if normal_num >= len(normal_array):
                normal_array = np.resize(normal_array,(2 * len(normal_array), 3))
            normal_array[normal_num] = va
            normal_num += 1

        elif sp[0] == 'f':
            total_face += 1
            array = np.ones((len(sp)-1, 2))
            for i in range(0, len(sp)-1):
                split_face = sp[i + 1].split('/')
                array[i][0] = int(split_face[0])
                array[i][1] = int(split_face[2])
                total_n[int(array[i][0] - 1)] += normal_array[int(array[i][1] - 1)]
                total_cnt[int(array[i][0] - 1)] += 1
            if len(sp) == 4:
                face_3 += 1
            elif len(sp) == 5:
                face_4 += 1
            elif len(sp) > 5:
                face_more += 1
            triangulation(len(sp)-1, array)        
    f.close()
    print("Total number of faces are " + str(total_face))
    print("Number of faces with 3 vertices are " + str(face_3))
    print("Number of faces with 4 vertices are " + str(face_4))
    print("Number of faces with more than 4 vertices are " + str(face_more))
    
    gVertexArraySeparate = np.ones((sep_cnt, 3))
    gVertexArraySeparate = sep[0:sep_cnt]
    gIndexArray = np.ones((ida_cnt, 3))
    gIndexArray = ida[0:ida_cnt]
    w_gVertexArraySeparate = np.ones((w_sep_cnt, 3))
    w_gVertexArraySeparate = w_sep[0:w_sep_cnt]
    w_gIndexArray = np.ones((w_ida_cnt, 2))
    w_gIndexArray = w_ida[0:w_ida_cnt]
    gVertexArrayIndexed = np.ones((vertex_num * 2, 3))
    now = 0
    for i in range(0, vertex_num):
        avg_n[i] = total_n[i] / total_cnt[i]
        gVertexArrayIndexed[now] = avg_n[i]
        now+=1
        gVertexArrayIndexed[now] = vertex_array[i]
        now+=1
    gVertexArraySeparate = gVertexArraySeparate.astype('float32')
    gVertexArrayIndexed = gVertexArrayIndexed.astype('float32')
    gIndexArray = gIndexArray.astype('int32')
    w_gVertexArraySeparate = w_gVertexArraySeparate.astype('float32')
    w_gIndexArray = w_gIndexArray.astype('int32')
    w_gVertexArrayIndexed = gVertexArrayIndexed
    drop = 1

def triangulation(num, array):
    global w_sep, w_sep_cnt, w_ida, w_ida_cnt, sep, sep_cnt, ida, ida_cnt, normal_array, vertex_array
    for i in range(1, num - 1):
        if (sep_cnt + 6) >= len(sep):
            sep = np.resize(sep,(2 * len(sep), 3))
        sep[sep_cnt] = normal_array[int(array[0][1] - 1)]
        sep_cnt += 1
        sep[sep_cnt] = vertex_array[int(array[0][0] - 1)]
        sep_cnt += 1
        sep[sep_cnt] = normal_array[int(array[i][1] - 1)]
        sep_cnt += 1
        sep[sep_cnt] = vertex_array[int(array[i][0] - 1)]
        sep_cnt += 1
        sep[sep_cnt] = normal_array[int(array[i+1][1] - 1)]
        sep_cnt += 1
        sep[sep_cnt] = vertex_array[int(array[i+1][0] - 1)]
        sep_cnt += 1
        if ida_cnt >= len(ida):
                ida = np.resize(ida,(2 * len(ida), 3))
        ida[ida_cnt][0] = int(array[0][0] - 1)
        ida[ida_cnt][1] = int(array[i][0] - 1)
        ida[ida_cnt][2] = int(array[i+1][0] - 1)
        ida_cnt+=1

    for i in range(0, num):
        if (w_sep_cnt + 4) >= len(w_sep):
            w_sep = np.resize(w_sep,(2 * len(w_sep), 3))
        w_sep[w_sep_cnt] = normal_array[int(array[i][1] - 1)]
        w_sep_cnt += 1
        w_sep[w_sep_cnt] = vertex_array[int(array[i][0] - 1)]
        w_sep_cnt += 1
        w_sep[w_sep_cnt] = normal_array[int(array[(i+1)%num][1] - 1)]
        w_sep_cnt += 1
        w_sep[w_sep_cnt] = vertex_array[int(array[(i+1)%num][0] - 1)]
        w_sep_cnt += 1
        if w_ida_cnt >= len(w_ida):
                w_ida = np.resize(w_ida,(2 * len(w_ida), 3))
        w_ida[w_ida_cnt][0] = int(array[i][0] - 1)
        w_ida[w_ida_cnt][1] = int(array[(i+1)%num][0] - 1)
        w_ida_cnt+=1
        


drop = 0
S_mode = 0
Z_mode = 0
normal_array = None
vertex_array = None
ida = None
ida_cnt = 0
sep = None
sep_cnt = 0
w_sep = None
w_sep_cnt = 0
w_ida = None
w_ida_cnt = 0
gVertexArraySeparate = None
gVertexArrayIndexed = None
gIndexArray = None
w_gVertexArraySeparate = None
w_gVertexArrayIndexed = None
w_gIndexArray = None
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
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
