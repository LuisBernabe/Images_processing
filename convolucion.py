from Tkinter import *
from PIL import ImageTk, Image
from tkFileDialog import *
import math
import cv2

#como precondicion la matriz debe ser cuadrada e impar
def convol_matriz(path,matriz,name,fac):
    global origenx,origeny,xMatriz,yMatriz,resR,resG,resB
    im=Image.open(path)
    pixels=im.load()
    alto,ancho=im.size #alto y ancho
    origenx=0
    origeny=0
    resR=0
    resG=0
    resB=0
    yMatriz=len(matriz)#renglones
    xMatriz=len(matriz[0])#Columnas
    factor=len(matriz)**2


    #print "alto:",alto,"\nancho:",ancho,"\nyMatriz:",yMatriz,"\nxMatriz",xMatriz

    while yMatriz < alto:
        while xMatriz < ancho:
            for i in range(origeny,yMatriz):
                for j in range(origenx,xMatriz):
                    r,g,b=pixels[i,j]
                    resR+=r
                    resG+=g
                    resB+=b
            pixels[get_center(origeny,yMatriz),get_center(origenx,xMatriz)]=(resR/factor,resG/factor,resB/factor)
            xMatriz+=1
            origenx+=1
            resR=0
            resG=0
            resB=0
            #print "***********************"
        yMatriz+=1
        origeny+=1
        origenx=0
        xMatriz=len(matriz[0])
    res=name+"_"+path
    im.save(res)
    return res

def get_center(inicio,final):
    res=inicio+((final-inicio)-1)/2
    return res


##convol_matriz("jemma.png",[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],"Desenfoque")
#print get_center(4,7)
