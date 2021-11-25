#classe qui gère la fenêtre graphique et les transformations géométriques entre la réalité et l'image.
class Window: 
    #Constructeur : On donne les coordonnées et la largeur et la hauteur.
    def __init__(self,xmin,ymin,xmax,ymax,width,height):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.width = width
        self.height = height
    
    #Calcule les coordonnées d'une affixe z de [xmin,xmax]x[ymin,ymax] dans une image de taille width,height
    def picture_coordinates(self,z):
        return (round((z.real-self.xmin)/(self.xmax-self.xmin)*self.width),round((self.ymax-z.imag)/(self.ymax-self.ymin)*self.height))
            
    #calcule la valeur d'un pas de un pixel en abscisse. (possibilité de repère non carré)
    def p_x(self):
        return (self.xmax-self.xmin)/self.width
    #calcule la valeur d'un pas de 1px pixel en ordonnées.   
    def p_y(self):
        return (self.ymax-self.ymin)/self.height
    def get_xmin(self):
        return self.xmin
    def get_xmax(self):
        return self.xmax
    def get_ymin(self):
        return self.ymin
    def get_ymax(self):
        return self.ymax
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height 