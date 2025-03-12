import tkinter
import math
from OpenGL import GL
from OpenGL import GLU
from pyopengltk import OpenGLFrame


ETERNAL_WIDTH = 1200
ETERNAL_HEIGHT = 630

class VisualiserCursor():

    def __init__(self):
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.pos_z = 0.0
        self.color = (1.0,1.0,0.0)
        self.grid_mode = ("noMovement","xzPlane","zyPlane","xyPlane")
        self.grid_mode_index = 0

    def translate(self,dx,dy,dz):
        self.pos_x += dx
        self.pos_y += dy
        self.pos_z += dz

    def place(self,x,y,z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def show(self):
        
        GL.glBegin(GL.GL_LINES)
        GL.glColor4f( self.color[0] , self.color[1] , self.color[2] , 0.2 )
        GL.glVertex3f( self.pos_x - 50 , self.pos_y , self.pos_z )
        GL.glVertex3f( self.pos_x + 50 , self.pos_y , self.pos_z )
        GL.glVertex3f( self.pos_x , self.pos_y , self.pos_z - 50 )
        GL.glVertex3f( self.pos_x , self.pos_y , self.pos_z + 50 )
        GL.glVertex3f( self.pos_x , self.pos_y - 50 , self.pos_z )
        GL.glVertex3f( self.pos_x , self.pos_y + 50 , self.pos_z )
        GL.glEnd()

        #self.showGrid()

        GL.glBegin(GL.GL_POINTS)
        GL.glColor3f( self.color[0] , self.color[1] , self.color[2] )
        GL.glVertex3f( self.pos_x , self.pos_y , self.pos_z )
        GL.glEnd()


class VisualiserCamera:

    def __init__(self):
        self.distance_scale = 1.0
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0
        self.cursor_element = VisualiserCursor()

    def update_positions(self,horizontal_turning_direction,vertical_turning_direction):

        if horizontal_turning_direction == 1:
                self.horizontal_angle += 3
        elif horizontal_turning_direction == -1:
                self.horizontal_angle -= 3
        else:
            pass

        if vertical_turning_direction == 1:
            self.vertical_angle += 3
        elif vertical_turning_direction == -1:
            self.vertical_angle -= 3
        else:
            pass
    
    def zooming(self,orientation):

        if orientation == 1:
            self.distance_scale -= 0.2
        elif orientation == -1:
            self.distance_scale += 0.2



class Visualiser(OpenGLFrame):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.camera_element = VisualiserCamera()
        self.cursor_element = VisualiserCursor()
        self.enable_rotating = False
        self.anterior_mouse_position = [ 0.0 , 0.0 ]
        self.vertex_list = []
        self.triangle_color_list = []
        self.texcoord_list = []
        self.texture = [] 
        self.image_en_array = None
        
    def update_display_data(self,vertex_list,color_list,texcoord_list):
        self.vertex_list = vertex_list
        self.triangle_color_list = color_list
        self.texcoord_list = texcoord_list
        #self.triangle_color_list = color_list
        
    def update_texture_data( self ,  image_en_array ):
        #print("VISUALISER, update_texture_data : " + str(image_en_array) )
        self.image_en_array = image_en_array
        longueur = len(self.image_en_array)
        largeur = len(self.image_en_array[0])
        self.texture = GL.glGenTextures(1)
        GL.glBindTexture( GL.GL_TEXTURE_2D , self.texture )
        GL.glTexParameteri( GL.GL_TEXTURE_2D , GL.GL_TEXTURE_MAG_FILTER , GL.GL_NEAREST )
        GL.glTexParameteri( GL.GL_TEXTURE_2D , GL.GL_TEXTURE_MIN_FILTER , GL.GL_NEAREST )
        GL.glTexImage2D( GL.GL_TEXTURE_2D , 0 , 3 , longueur , largeur , 0 , GL.GL_RGB , GL.GL_UNSIGNED_BYTE , self.image_en_array )

    def process_double_click(self,event):
        self.camera_element.vertical_angle = 0.0
        self.camera_element.horizontal_angle = 0.0

    def process_mousewheel(self,event):
        #print(event)
        if event.delta == 120:
            self.camera_element.zooming(1)
        elif event.delta == -120:
            self.camera_element.zooming(-1)

    def process_button_1_motion(self,event):
        
        if event.x > self.anterior_mouse_position[0]:
            self.camera_element.update_positions(1,0)
        elif event.x < self.anterior_mouse_position[0]:
            self.camera_element.update_positions(-1,0)
        else:
            pass

        if event.y > self.anterior_mouse_position[1]:
            self.camera_element.update_positions(0,-1)
        elif event.y < self.anterior_mouse_position[1]:
            self.camera_element.update_positions(0,1)
        else:
            pass

        self.anterior_mouse_position = [ event.x , event.y ]
        #print(event)

    def initgl(self):
        GL.glViewport(0, 0, self.width, self.height)
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glPointSize(6)
        GL.glClearDepthf(1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)

    def show_vertex_list(self):

        if self.image_en_array is not None:
            #print(self.image_en_array.dtype)
            GL.glEnable( GL.GL_TEXTURE_2D )
            GL.glBindTexture( GL.GL_TEXTURE_2D , self.texture )
            pass

        GL.glBegin(GL.GL_TRIANGLES)
        i = 0
        while i < len(self.vertex_list):
            if self.texcoord_list[i] != "NO TEXTURE":
                GL.glTexCoord2f( self.texcoord_list[i][0]/128 , self.texcoord_list[i][1]/128 )
            GL.glColor3f( self.triangle_color_list[i][0] , self.triangle_color_list[i][1] , self.triangle_color_list[i][2]  )
            GL.glVertex3f( self.vertex_list[i][0] , self.vertex_list[i][1] , self.vertex_list[i][2] )
            i += 1
        GL.glEnd()
        GL.glBindTexture( GL.GL_TEXTURE_2D , 0 )
        
        GL.glLineWidth(2)
        
        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glColor3f(1.0,1.0,1.0)
        i = 0
        while i < len(self.vertex_list):
            GL.glVertex3f( self.vertex_list[i][0] , self.vertex_list[i][1] , self.vertex_list[i][2] )
            i += 1
        GL.glEnd()

        GL.glBegin(GL.GL_POINTS)
        GL.glColor3f(1.0,1.0,1.0)
        i = 0
        while i < len(self.vertex_list):
            GL.glVertex3f( self.vertex_list[i][0] , self.vertex_list[i][1] , self.vertex_list[i][2] )
            i += 1
        GL.glEnd()

    def show_directions(self):

        GL.glLineWidth(3)

        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(1.0,0.0,0.0)
        GL.glVertex3f(0.0,0.0,0.0)
        GL.glVertex3f(1.0,0.0,0.0)
        GL.glEnd()

        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.0,1.0,0.0)
        GL.glVertex3f(0.0,0.0,0.0)
        GL.glVertex3f(0.0,1.0,0.0)
        GL.glEnd()

        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.0,0.0,1.0)
        GL.glVertex3f(0.0,0.0,0.0)
        GL.glVertex3f(0.0,0.0,1.0)
        GL.glEnd()

        GL.glLineWidth(2)

        i = -20
        GL.glBegin(GL.GL_LINES)
        GL.glColor4f(0.3,0.3,0.3,0.3)
        while i < 20:
            GL.glVertex3f( -20.0 , 0.0  , i )
            GL.glVertex3f( 20.0 , 0.0 , i )

            GL.glVertex3f( i , 0.0 , -20.0 )
            GL.glVertex3f( i , 0.0 , 20.0 )

            
            i += 0.2
        GL.glEnd()

    def redraw(self):
        
        #GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT )
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        self.show_directions()
        self.show_vertex_list()

        # Showing the cursor of the visualiser
        """
        GL.glBegin(GL.GL_POINTS)
        GL.glColor3f( self.cursor_element.color[0] , self.cursor_element.color[1] , self.cursor_element.color[2] )
        GL.glVertex3f( self.cursor_element.pos_x , self.cursor_element.pos_y , self.cursor_element.pos_z )
        GL.glEnd()"""
        self.cursor_element.show()


        GL.glMatrixMode(GL.GL_PROJECTION)
        #GL.glTranslatef(0.0,0.0,1.0)
        GL.glLoadIdentity()
        GLU.gluPerspective(60,1,0.1,1000.0)
        GLU.gluLookAt( 0.0 , 0.0 , self.camera_element.distance_scale , 0.0 , 0.0 , 0.0 , 0.0 , 1.0 , 0.0 )
        GL.glRotate(self.camera_element.horizontal_angle,0.0,1.0,0.0)
        GL.glRotate(self.camera_element.vertical_angle,1.0,0.0,0.0) 



