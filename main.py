import time
import Window_Model as W
import Mandelbrot_Model as M
import Newton_Model as Newton



if __name__ == '__main__':

    start_time= time.time()
    
    x0 = -0.743643887037151  # Coordonnées du point centre du zoom
    y0 = 0.13182590420533
    eps = (3/2**10) 
    
    
    Nb_images = 10
    
    for k in range(10,10+Nb_images):
        pic = W.Window(x0-eps,y0-eps,x0+eps,y0+eps,600,600) #création de la fenêtre graphique
        mandel = M.Mandelbrot_Model(pic,3200,10)  #On crée un objet Mandelbrot_Model avec les paramètres souhaités
        the_map = mandel.create_map_mp(True, "zoom_"+str(k)+".txt")
        mandel.create_image_mandelbrot(the_map,"zoom_"+str(k),True)
        print("image ",k," créée")
        eps = eps/2
        
        
    #the_map = mandel.create_map_mp(True,"600_iter.txt") #On crée la map
    
     #On crée l'image
    
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))