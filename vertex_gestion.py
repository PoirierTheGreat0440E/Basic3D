import tkinter

ETERNAL_WIDTH = 1200
ETERNAL_HEIGHT = 630

class VertexStorage( tkinter.Frame ):
    

    def assigner_texcoords(self,triangle_texcoord):
        #print("ASSIGNER TEXCOORDS MDR")
        indices_triangles = []
        #print("Selected indices :" + str(self.selected_indices) )
        for index in self.selected_indices:
            if index%3 not in indices_triangles:
                indices_triangles.append(index)
        #print("INDICE DES TRIANGLES : " + str(indices_triangles) )
        for index2 in indices_triangles:
            self.texcoord_array[index2] = ( triangle_texcoord[0] , triangle_texcoord[1] )
            self.texcoord_array[index2+1] = ( triangle_texcoord[2] , triangle_texcoord[3] ) 
            self.texcoord_array[index2+2] =  ( triangle_texcoord[4] , triangle_texcoord[5] )
        self.refresh_listboxes()

    def process_selection(self,event):
        self.selected_indices = self.vertex_listbox.curselection()

    def add_vertex(self,new_x,new_y,new_z,new_r=1.0,new_g=1.0,new_b=1.0,new_tx="NULL",new_ty="NULL"):
        self.vertex_array.append( ( round(new_x,2) , round(new_y,2) , round(new_z,2) ) )
        self.color_array.append( ( round(new_r,2) , round(new_g,2) , round(new_b,2) ) )
        self.texcoord_array.append( "NO TEXTURE" )
        self.refresh_listboxes()

    def refresh_listboxes(self):
        self.vertex_listbox.delete(0,tkinter.END)
        self.color_listbox.delete(0,tkinter.END)
        self.texcoord_listbox.delete(0,tkinter.END)
        i = 0
        while i < len( self.vertex_array ):
            self.vertex_listbox.insert(tkinter.END,str(self.vertex_array[i]))
            self.color_listbox.insert(tkinter.END,str(self.color_array[i]))
            self.texcoord_listbox.insert(tkinter.END," x : " + str(self.texcoord_array[i][0]) + " / y : " + str(self.texcoord_array[i][1]) )
            i += 1
    
    def process_scale_change(self,event):
        #print( str(self.vertexRED.get()) + "<<>>" + str(self.vertexGREEN.get()) + "<<>>" + str(self.vertexBLUE.get()) )
        for index in self.selected_indices:
            self.color_array[index] = ( round(int(self.vertexRED.get())/255,2) , round(int(self.vertexGREEN.get())/255,2) , round(int(self.vertexBLUE.get())/255,2) )
        self.refresh_listboxes()


    def __init__(self,parent):

        super().__init__(parent,width=ETERNAL_WIDTH,height=ETERNAL_HEIGHT,bg="red")

        self.selected_indices = []
        self.vertex_array = []
        self.color_array = []
        self.texcoord_array = []

        self.vertexRED = tkinter.IntVar()
        self.vertexRED.set(0)
        self.vertexGREEN = tkinter.IntVar()
        self.vertexGREEN.set(0)
        self.vertexBLUE = tkinter.IntVar()
        self.vertexBLUE.set(0)

        self.vertex_listbox = tkinter.Listbox( self , width=20, height=int(ETERNAL_HEIGHT/2) , listvariable=self.vertex_array , selectmode="multiple" )
        self.color_listbox = tkinter.Listbox( self , width=20, height=int(ETERNAL_HEIGHT/2)  , listvariable=self.color_array , selectmode="multiple" , takefocus=False )
        self.texcoord_listbox = tkinter.Listbox( self , width=20 , height=int(ETERNAL_HEIGHT/2) , listvariable=self.texcoord_array , takefocus = False )

        self.vertexREDscale = tkinter.Scale( self , variable=self.vertexRED , from_=0 , to=255 , orient='horizontal' , bg="#FF8484" , command=self.process_scale_change )
        self.vertexGREENscale = tkinter.Scale( self , variable=self.vertexGREEN , from_=0 , to=255 , orient='horizontal', bg="#8AFF83" , command=self.process_scale_change )
        self.vertexBLUEscale = tkinter.Scale( self , variable=self.vertexBLUE , from_=0 , to=255 , orient='horizontal', bg="#8CA3FF"  , command=self.process_scale_change )
        

        self.vertexBLUEscale.pack( side=tkinter.BOTTOM , fill=tkinter.X )
        self.vertexGREENscale.pack( side=tkinter.BOTTOM , fill=tkinter.X )
        self.vertexREDscale.pack( side=tkinter.BOTTOM , fill=tkinter.X )

        self.vertex_listbox.pack(side=tkinter.LEFT)
        self.color_listbox.pack(side=tkinter.LEFT)
        self.texcoord_listbox.pack(side=tkinter.LEFT)

        self.vertex_listbox.bind('<<ListboxSelect>>',self.process_selection)

        print("Vertex Storage init SUCCESFUL !")

