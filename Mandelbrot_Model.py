from multiprocessing import Pool
from  PIL import  Image, ImageDraw
import colorsys


#convertit une donnée (Teinte, Saturation, Lumière) que l'on peut trouver dans paint en RGB.
def paint_hsl_to_rgb(T,S,L):
        res = colorsys.hls_to_rgb(T/240,L/240,S/240)
        return (int(res[0]*255),int(res[1]*255),int(res[2]*255))
               
class Mandelbrot_Model:
    #Constructeur : On passe en paramètre un objet fenetre, le nombre d'itérations et la borne de module. 
    def __init__(self,fenetre,N,b):
        self.window = fenetre
        self.bound = b
        self.nmax = N
    #Calcule le nombre d'itérations de z(n+1) = z(n)^2+c avec z(0)=0 pour c passé en paramètre
    def compute_iterations(self,c):
        i=0
        z=0
        cond = abs(z)>self.bound
        while i<self.nmax and not cond:
            z = z**2+c
            cond=(abs(z)>self.bound)
            i=i+1
        return i
    #Crée un tableau avec comme entrées [z,k] avec z l'affixe du point et k le nombre d'itérations pour tous les z de la fenêtre 
    #Si save = True, on enregistre les calculs dans le fichier name.
    def create_map(self,save=False,name=""):
        map = []
        if save :
            fichier = open(name, "w")
        n_max = 0
        n_min = self.nmax
        pic = self.window
        i=pic.get_xmin()
        while i<pic.get_xmax():
            j=pic.get_ymax()
            while j>pic.get_ymin():
                c=i+1j*j
                k = self.compute_iterations(c)
                if k<=n_min:
                    n_min = k
                if k >= n_max:
                    n_max = k
                if save:
                    fichier.write(str(c)+"|"+str(k)+"\n")
                map.append([c,k]) 
                j=j-pic.p_y()
            i=i+pic.p_x()
        if save:
            fichier.write(str(n_min)+"|"+str(n_max)+"|0\n")
            fichier.close()
        return (map,n_min,n_max)
    #Même fonction que ci-dessus mais utilisant le multiprocessing.     
    def create_map_mp(self,save=False,name=""):
        pic = self.window
        p = Pool(processes=3)  #processes est le nombre de coeurs à utiliser.
        if save :
            fichier = open(name, "w")
            
        ensemble = []
        map = []
        i=pic.get_xmin()
        while i<pic.get_xmax():
            j=pic.get_ymax()
            while j>pic.get_ymin():
                c=i+1j*j  
                ensemble.append(c)            
                j=j-pic.p_y()
            i=i+pic.p_x() 
        result = p.map(self.compute_iterations, ensemble)
        n_min = min(result)
        n_max = self.nmax
        k=0
        for e in ensemble:
            if save:
                fichier.write(str(e)+"|"+str(result[k])+"\n")
            map.append([e,result[k]])
            k=k+1
        if save:
            fichier.write(str(n_min)+"|"+str(n_max)+"|0\n")
            fichier.close()
        p.close()
        p.join()
        return (map,n_min,n_max)
    #Permet de récupérer une map écrite dans un fichier name.
    def open_map(self,name):
        fichier = open(name, "r")
        lignes = fichier.readlines()
        N = len(lignes)
        k=1
        map = []
        nmin,nmax =0,0
        for l in lignes:
            m = l.split("|")
            if k == N:
                nmin = int(m[0])
                nmax = int(m[1])
            else :
                map.append([complex(m[0]),int(m[1])])
            k=k+1
        fichier.close()
        return (map,nmin,nmax)

    #Ma version de la fonction de couleurs
    def color_map(self,n):
        lbc = 250
        COLOR1 = 35
        COLOR2 = 140
        if n ==self.nmax:
            return (0,0,0)
        if n % lbc == 0:
            return paint_hsl_to_rgb(240,35,130)
        elif n % lbc < lbc / 2:
            return paint_hsl_to_rgb(COLOR1,240 , round(240/(lbc/2)*(n%lbc)))
        else :
            return paint_hsl_to_rgb(COLOR2, 240, round(240-240/(lbc/2)*(n%lbc-lbc/2)))
       
    #Crée une image à partir de mandel_map qui doit être une map crée par create_map ou create_map_mp, ou bien chargée depuis un fichier. Enregistre l'image dans "nom.png", et si show=True, l'image s'affiche à la fin de l'execution.
    def create_image_mandelbrot(self,mandel_map,nom,show=False):
        pic = self.window
        surface = Image.new('RGB',(self.window.get_width(),self.window.get_height())) 
        draw = ImageDraw.Draw(surface)
        map = mandel_map[0]
        nmin = mandel_map[1]
        nmax = mandel_map[2]
        for z in map:
            draw.point(pic.picture_coordinates(z[0]),self.color_map(z[1]))
        if show:
            surface.show()
        surface.save(nom+".png","png")