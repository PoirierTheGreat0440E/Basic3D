import tkinter
import tkinter.filedialog
import numpy
from PIL import ImageTk, Image

ETERNAL_WIDTH = 1200
ETERNAL_HEIGHT = 630

class gestionneur_texture( tkinter.Frame ):

    def __init__(self,*args,**kwargs):
        
        super().__init__(*args,**kwargs)

        self.texturiseur = None
        self.fichier_selection = None
        self.liste_points = []

        self.button1 = tkinter.Button(self,text="Charger une image",command=self.charger_image)
        self.button1.pack(side=tkinter.TOP,fill=tkinter.X)

        self.titre = tkinter.Label(self,text="")
        self.titre.pack(side=tkinter.TOP,fill=tkinter.X)

        self.listbox = tkinter.Listbox(self)
        self.listbox.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)

    def charger_image(self):
        try:
            self.fichier_selection = tkinter.filedialog.askopenfile( initialdir="./" )
            image = Image.open(self.fichier_selection.name).resize( (128,128) )
            image_tk_1 = ImageTk.PhotoImage(image)
            self.titre.configure(image=image_tk_1)
            self.titre.image = image_tk_1
            self.titre.bind( '<Double-Button-1>' , self.ouvrir_canvas )
        except FileNotFoundError as FNFE:
            print("Le fichier n'a pas été trouvé :(")
        except ValueError as VE:
            print("VALUE ERROR")
        except TypeError as TE:
            print("TYPE ERROR")

    def ouvrir_canvas(self,event):
        self.texturiseur = Texturiseur( self , chemin=self.fichier_selection.name , liste_debut=self.liste_points  )
        self.texturiseur.mainloop()

    def rafraichir_liste(self,liste_don):
        self.liste_points = liste_don
        self.listbox.delete(0,tkinter.END)
        i = 0
        parite = 1
        while i < len(self.liste_points):
            if i%3 == 0:
                parite *= -1
            self.listbox.insert(tkinter.END,str(self.liste_points[i]))
            if parite < 0 :
                self.listbox.itemconfig(tkinter.END,bg="#f5f6fa")
            else:
                self.listbox.itemconfig(tkinter.END,bg="white")
            i += 1

    def communiquer_triangle(self,triangle):
        print("TRIANGLE DONNE : " + str(triangle))
        self.master.communiquer_triangle(triangle)

class Texturiseur(tkinter.Toplevel):

    def __init__(self,*args,chemin="",liste_debut=[],**kwargs):
        super().__init__(*args,**kwargs)
        self.image = Image.open(chemin)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.title("Texturiseur : " + str(chemin) )
        self.geometry(str(self.image.size[0])+"x"+str(self.image.size[1])+"+20+20")
        self.resizable(False,False)
        self.canvas = tkinter.Canvas(self,width=self.image.size[0],height=self.image.size[1],bg="beige")
        self.canvas.create_image( ( int(self.image.size[0]/2) , int(self.image.size[1]/2) ) , image=self.image_tk )
        self.canvas.bind('<Button-1>',self.process_button_1)
        self.canvas.bind('<Button-3>',self.process_button_3)
        self.liste_points = liste_debut
        self.dictionnaire_polygones = dict()
        self.canvas.pack()
        self.reanimer()

    def process_button_1(self,event):
        print(event)
        self.liste_points.append( (event.x,event.y) )
        self.master.rafraichir_liste(self.liste_points)
        self.reanimer()

    def process_button_3(self,event):
        selection_id = self.canvas.find_closest( event.x , event.y , 5 )
        try:
            item_choisi =  self.dictionnaire_polygones[selection_id[0]]
            self.master.communiquer_triangle( item_choisi )
        except KeyError as KE:
            #print("Key Error but its okay lol")
            pass

    def reanimer(self):
        self.dictionnaire_polygones = dict()
        self.canvas.create_image( ( int(self.image.size[0]/2) , int(self.image.size[1]/2) ) , image=self.image_tk )
        i = 0
        try:
            while i < len(self.liste_points):
                nouvel_id = self.canvas.create_polygon( self.liste_points[i][0] , self.liste_points[i][1] , self.liste_points[i+1][0] , self.liste_points[i+1][1] , self.liste_points[i+2][0] , self.liste_points[i+2][1] , outline="black" , fill="", width=3, activeoutline="red" )
                self.dictionnaire_polygones[nouvel_id] = (   self.liste_points[i][0] ,  self.liste_points[i][1] , self.liste_points[i+1][0] , self.liste_points[i+1][1] , self.liste_points[i+2][0] , self.liste_points[i+2][1])
                i += 3
        except Exception as E:
            pass
        for point in self.liste_points:
            self.canvas.create_oval( point[0]-3 , point[1]-3 , point[0]+3 , point[1]+3 , outline="black" , fill="red" )

if __name__ == "__main__":

    root = tkinter.Tk()
    MF1 = MasterFrame(root)
    MF1.pack()
    root.mainloop()
