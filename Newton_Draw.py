from PIL import Image, ImageDraw
import math
import colorsys
#Classe qui gère le dessin et la génération de l'image à proprement parlé.

class Newton_Draw:

    def __init__(self,fenetre):
        self.window = fenetre
        self.width = self.window.get_width()
        self.height = self.window.get_height()
        self.surface = Image.new('RGB',(self.width,self.height)) 
    
    #convertit une donnée (Teinte, Saturation, Lumière) que l'on peut trouver dans paint en RGB.
    def paint_hsl_to_rgb(self,T,S,L):
        res = colorsys.hls_to_rgb(T/240,L/240,S/240)
        res2 = (int(res[0]*255),int(res[1]*255),int(res[2]*255))
        return res2
    
    #Méthode qui à un bassin b et à une vitesse v associe la couleur et la lumière qui correspond
    def color_map(self,nmin,nmax,b,v):
        lmax = 120 #lumière max
        #op = lmax*math.cos(math.pi*(v-nmin)/(2*(nmax-nmin)))**2
        #a = lmax/(nmax-nmin)**2
        #op = a*(v-nmax)**2
        eps = 1
        n0 = math.floor(90/100*(nmax-nmin))
        a = -math.log(eps/lmax)/(n0-nmin)**2
        op = lmax*math.exp(-a*(v-nmin)**2)
        
        if b==0:
            color = self.paint_hsl_to_rgb(120,80,op) #vert     
        elif b==1:
            color = self.paint_hsl_to_rgb(150,180,op) #bleu    
        elif b==2:
            color = self.paint_hsl_to_rgb(160,0,op) #gris
        else :
            color = self.paint_hsl_to_rgb(38,240,op) #jaune
        return color
        
    #Métode qui construit l'image à partir d'une newton_map. 
    def create_newton_image(self,newton_map,nom):
        pic = self.window
        draw = ImageDraw.Draw(self.surface)
        map = newton_map[0]
        nmin = newton_map[1]
        nmax = newton_map[2]
        for z in map:
            draw.point(pic.picture_coordinates(z[0]),self.color_map(nmin,nmax,z[1],z[2]))
        self.surface.save(nom+".png","png")