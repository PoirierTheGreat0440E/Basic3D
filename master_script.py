import tkinter
from texture_gestion import gestionneur_texture
from vertex_gestion import VertexStorage
from visuel_gestion import Visualiser


ETERNAL_WIDTH = 1200
ETERNAL_HEIGHT = 630

class MasterFrame( tkinter.Frame ):

    def process_key_press(self,event):
        
        if ( event.char == 'a' ):
            self.visualiser.cursor_element.translate(0.1,0.0,0.0)
        if ( event.char == 'q' ):
            self.visualiser.cursor_element.translate(-0.1,0.0,0.0)
        if ( event.char == 'z' ):
            self.visualiser.cursor_element.translate(0.0,0.1,0.0)
        if ( event.char == 's' ):
            self.visualiser.cursor_element.translate(0.0,-0.1,0.0)
        if ( event.char == 'e' ):
            self.visualiser.cursor_element.translate(0.0,0.0,0.1)
        if ( event.char == 'd' ):
            self.visualiser.cursor_element.translate(0.0,0.0,-0.1)
        if ( event.char == ' ' ):
            self.VS1.add_vertex( self.visualiser.cursor_element.pos_x , self.visualiser.cursor_element.pos_y , self.visualiser.cursor_element.pos_z )
            self.visualiser.update_display_data( self.VS1.vertex_array , self.VS1.color_array , self.VS1.texcoord_array )

    def communiquer_triangle(self,triangle_donne):
        #print("MASTER FRAME : j'ai un triangle WTF le voici" + str(triangle_donne) )
        self.VS1.assigner_texcoords( triangle_donne )

    def communiquer_image(self,image_array):
        #print("MASTER FRAME , communiquer_image :" + str(image_array) )
        self.visualiser.update_texture_data( image_array )

    def process_configure(self,event):
        ETERNAL_WIDTH = event.width
        ETERNAL_HEIGHT = event.height
        #print(event)

    def __init__(self,parent):
        
        super().__init__(parent,width=int(ETERNAL_WIDTH/4),height=ETERNAL_HEIGHT,bg="#1C1C1C")
        self.VS1 = VertexStorage(self)
        self.VS1.pack( side=tkinter.LEFT )

        self.visualiser = Visualiser(self,width=int(ETERNAL_WIDTH/2),height=ETERNAL_HEIGHT)
        self.visualiser.animate = 10
        self.visualiser.pack(side=tkinter.LEFT)
        self.visualiser.bind('<B1-Motion>',self.visualiser.process_button_1_motion)
        self.visualiser.bind('<MouseWheel>',self.visualiser.process_mousewheel)
        self.visualiser.bind('<Double-Button-1>',self.visualiser.process_double_click)

        self.gestionneur_texture = gestionneur_texture(self,width=int(ETERNAL_WIDTH/4),height=ETERNAL_HEIGHT)
        self.gestionneur_texture.pack(side=tkinter.RIGHT,fill=tkinter.BOTH,expand=True)



if __name__ == '__main__':

    root = tkinter.Tk()
    root.geometry( str(ETERNAL_WIDTH)+"x"+str(ETERNAL_HEIGHT)+"+10+10")
    root.title("3D Basics v0.1")
    root.resizable(True,True)
    

    MF = MasterFrame(root)
    MF.pack( fill=tkinter.BOTH , expand=True )

    root.bind('<KeyPress>',MF.process_key_press)
    root.bind('<Configure>',MF.process_configure)

    root.mainloop()
