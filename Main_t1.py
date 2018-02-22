
"""
Tarea 1
Nombre: Luis Gerardo Bernabe Gomez
Correo: luis_berna@ciencias.unam.mx
No.Cuenta:312225430
"""
from Tkinter import *
#from PIL import Image
from PIL import ImageTk, Image
from tkFileDialog import *
import math
import cv2

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
def escalaDeGrises(nwpath):
   im=Image.open(nwpath)
   pixels=im.load()
   ancho,alto=im.size
   for i in range (0,ancho):
      for j in range (0,alto):
       r,g,b=pixels[i,j]
       valor=(r,r,r)
       pixels[i,j]=valor
   res="Gris_"+nwpath
   im.save(res)
   return res

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
#signo dado que esta en un rango de +- 127 el brillo, el signo nos ayuda a saber si se sumara o restara a los componentes RGB
#constante valor que se le sumara o restara segun sea el caso a los componentes RGB
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
def brillo(nwpath,signo,constante):
    im=Image.open(nwpath)
    pixels=im.load()
    ancho,alto=im.size
    for i in range (0,ancho):
       for j in range (0,alto):
        r,g,b=pixels[i,j]
        if signo == "+":
            cr,cg,cb=r+constante,constante+g,constante+b
        else:
            cr,cg,cb=r-constante,g-constante,b-constante

        if cr < 0 or cg < 0 or cb < 0 :
            valor=(0,0,0)
        elif cr > 255 or cg > 255 or cb >255:
            valor=(255,255,255)
        else:
            valor=(constante+r,constante+g,constante+b)

        pixels[i,j]=valor
    res="Brillo_"+nwpath
    im.save(res)
    return res

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
def altoConstraste(nwpath):
    im=Image.open(escalaDeGrises(nwpath))
    pixels=im.load()
    ancho,alto=im.size
    for i in range (0,ancho):
       for j in range (0,alto):
           r,g,b=pixels[i,j]
           if r >= 127:
               valor=(255,255,255)
           else:
               valor=(0,0,0)

           pixels[i,j]=valor
    res="AltoConstraste_"+nwpath
    im.save(res)
    return res

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
def inverso(nwpath):
    im=Image.open(altoConstraste(nwpath))
    pixels=im.load()
    ancho,alto=im.size
    for i in range (0,ancho):
       for j in range (0,alto):
           r,g,b=pixels[i,j]
           if r == 0:
               valor=(255,255,255)
           else:
               valor=(0,0,0)

           pixels[i,j]=valor
    res="Inverso_"+nwpath
    im.save(res)
    return res

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
#canal escoge cual componente R,G,B quiere mostrar
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
def componente(nwpath,canal):
    im=Image.open(nwpath)
    pixels=im.load()
    ancho,alto=im.size #Alto y ancho de la imagen
    for i in range (0,ancho):
       for j in range (0,alto):
           r,g,b=pixels[i,j]
           if canal== "R":
               valor=(r,0,0)
           elif canal=="G":
               valor=(0,g,0)
           elif canal=="B":
               valor=(0,0,b)
           pixels[i,j]=valor
    res="Componente"+canal+nwpath
    im.save(res)
    return res

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
#finura se tomaran sub-matrices de tamanio finura*finura para realizar el procedimiento en esta area
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
def mosaico(nwpath, finura):
    global origenx,origeny,xMatriz,yMatriz
    im=Image.open(nwpath)
    pixels=im.load()
    alto,ancho=im.size #alto y ancho
    origenx=0
    origeny=0
    yMatriz=finura
    xMatriz=finura
    listaR=[]
    listaG=[]
    listaB=[]

    while yMatriz < alto:
        while xMatriz < ancho:
            for i in range(origeny,yMatriz):
                for j in range(origenx,xMatriz):
                    #print "[",i,",",j,"]"
                    r,g,b=pixels[i,j]
                    listaR.append(r)
                    listaG.append(g)
                    listaB.append(b)
            promR=int(math.ceil(promedio(listaR)))
            promG=int(math.ceil(promedio(listaG)))
            promB=int(math.ceil(promedio(listaB)))
            #rellena la imagen con el nuevo valor
            for k in range(origeny,yMatriz):
                for l in range(origenx,xMatriz):
                    valor=(promR,promG,promB)
                    pixels[k,l]=valor

            xMatriz+=finura
            origenx+=finura
            listaR=[]
            listaB=[]
            listaG=[]
        yMatriz+=finura
        origeny+=finura
        origenx=0
        xMatriz=finura

    res="Mosaico_"+nwpath
    im.save(res)
    return res



#Metodo auxiliar que saca el promedio de una matriz
def promedio(lista):
    global res
    res=0
    tam=len(lista)
    for i in range(0,tam):
        res+=lista[i]
    resu=res//len(lista)
    return resu


def inicio():
    path=raw_input("\n\n\nIngresa el nombre de la imagen que quieres procesar\n")
    print "Iniciando Escala de Grises"
    escalaDeGrises(path)
    print "Escala de Grises listo\nIniciando Brillo"
    brillo(path,"+",87)
    print "Brillo listo\nIniciando Alto Contraste"
    altoConstraste(path)
    print "Alto Contraste listo\nIniciando Inverso"
    inverso(path)
    print "Inverso listo\nIniciando componente"
    componente(path,"B")
    print "componente listo\nIniciando mosaico\n\nEspere un momento"
    mosaico(path,25)
    print "Mosaico listo"


#inicio()
mosaico("jemma.png",10)
