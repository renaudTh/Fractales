#Coeur du modèle : gère tous les calculs de la méthode de Newton.

class Newton:
        
    #Le polynôme avec lequel on travaille
    def P(self,z):
        #a = -0.00508+0.33136*1j
        #l = 1/4-a**2      
        return z**3-2*z+2
    #le polynôme dérivé
    def P1(self,z):
        # a = -0.00508+0.33136*1j
        # l = 1/4-a**2      
        return 3*z**2-2
    #Constructeur : prend en entré un objet Window et les racines de P    
    def __init__(self,racines,fenetre):
        self.fenetre = fenetre
        self.racines = racines
    #Méthode de newton appliquée en z0 : Renvoie l'indice du bassin d'attraction b et le nombre d'itération.    
    def select_region(self,z0,nmax,eps):
        i=0
        z=z0
        b = -1
        diff = [abs(z-r) for r in self.racines]      
        c = any([d<eps for d in diff])
        while i<nmax and not c:
            z = z-self.P(z)/self.P1(z)
            diff = [abs(z-r) for r in self.racines]           
            c = any([d<eps for d in diff])
            i=i+1       
        if c : b = diff.index(min(diff)) 
        return (b,i)   
    #crée un tableau de tableau qui contient [z,b,n] où z est un complexe, b l'indice du bassin d'attraction et n le nombre d'itération. Calcule à la volée les nombres minimal et maximal d'itérations. Permet de sauver les calculs dans un fichier.    
    def create_map(self,nmax,eps,save=False,name=""):
        map = []
        if save :
            fichier = open(name, "w")
        n_max = 0
        n_min = nmax
        pic = self.fenetre
        i=pic.get_xmin()
        
        while i<pic.get_xmax():
            j=pic.get_ymax()
            while j>pic.get_ymin():
                z0=i+1j*j
                l = self.select_region(z0,nmax,eps)
                if l[0]>-1 and l[1]<=n_min:
                    n_min = l[1]
                if l[0]>-1 and l[1] >= n_max:
                    n_max = l[1] 
                if save:
                    fichier.write(str(z0)+"|"+str(l[0])+"|"+str(l[1])+"\n")
                map.append([z0,l[0],l[1]]) 
                j=j-pic.p_y()
            i=i+pic.p_x()
        if save:
            fichier.write(str(n_min)+"|"+str(n_max)+"|0\n")
            fichier.close()
        return (map,n_min,n_max)
    #Ouvre un fichier et renvoie le même résultat que la méthode create_map.
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
                map.append([complex(m[0]),int(m[1]),int(m[2])])
            k=k+1
        fichier.close()
        return (map,nmin,nmax)