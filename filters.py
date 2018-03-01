"""
Luis Bernabe
luis_berna@ciencias.unam.mx
"""

from Tkinter import *
#from PIL import Image
from PIL import ImageTk, Image
from tkFileDialog import *
import math
import cv2
import convolucion

# nwpath es el nombre de la imagen que quiere ser transformada en la nueva imagen
# res devuelve el nombre de la nueva imagen ya con la manipulacion requerida
#ajsdafwsfowjfscjwecwcowcdpkw
def escalaDeGrises(nwpath,xt={}):
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
def brillo(nwpath,xt={}):
    im=Image.open(nwpath)
    pixels=im.load()
    ancho,alto=im.size
    constante=xt.get('constante')
    for i in range (0,ancho):
       for j in range (0,alto):
        r,g,b=pixels[i,j]
        cr,cg,cb=r+constante,g+constante,b+constante

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
def altoConstraste(nwpath,xt={}):
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
def inverso(nwpath,xt={}):
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
def componente(nwpath,xt={}):
    im=Image.open(nwpath)
    canal=xt.get('canal')
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
def mosaico(nwpath,xt={}):
    global origenx,origeny,xMatriz,yMatriz
    finura=xt.get('finura')
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


def blur(nwpath,tam,xt={}):
    matrizTres=[[0.0,0.2,0.0],[0.2,0.2,0.2],[0.0,0.2,0.0]]
    matrizCinco=[[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]]
    if tam == 3:
        convolucion.convol_matriz(nwpath,matrizTres,"Blur_3",1)
    elif tam ==5:
        convolucion.convol_matriz(nwpath,matrizCinco,"Blur_5",1/13)

def motionBlur(nwpath,tam,xt={}):
    matrizNueve=[[1,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]]
    matrizTres=[[1,0,0],[0,1,0],[0,0,1]]

    if tam == 3:
        convolucion.convol_matriz(nwpath,matrizTres,"Motion_Blur_3",1/3)
    elif tam ==9:
        convolucion.convol_matriz(nwpath,matrizNueve,"Motion_Blur_9",1/9)

def findEdges(nwpath,orientacion,xt={}):
    matrizHorizontal=[[0,0,-1,0,0],[0,0,-1,0,0],[0,0,2,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    matrizVertical=[[0,0,-1,0,0],[0,0,-1,0,0],[0,0,4,0,0],[0,0,-1,0,0],[0,0,-1,0,0]]
    matrizCuatroCinco=[[-1,0,0,0,0],[0,-2,0,0,0],[0,0,6,0,0],[0,0,0,-2,0],[0,0,0,0,-1]]

    if orientacion == 180:
        convolucion.convol_matriz(nwpath,matrizHorizontal,"Bordes_Horizontales",1)
    elif orientacion == 90:
        convolucion.convol_matriz(nwpath,matrizVertical,"Bordes_Verticales",1)
    elif orientacion == 45:
        convolucion.convol_matriz(nwpath,matrizCuatroCinco,"Bordes_45",1)

def sharpen(nwpath,tam,xt={}):
    matrizTres=[[-1,-1,-1],[-1,-9,-1],[-1,-1,-1]]
    matrizCinco=[[-1,-1,-1,-1,-1],[-1,2,2,2,-1],[-1,2,8,2,-1],[-1,2,2,2,-1],[-1,-1,-1,-1,-1]]
    if tam == 3:
        convolucion.convol_matriz(nwpath,matrizTres,"sharpen_3",1)
    elif tam ==5:
        convolucion.convol_matriz(nwpath,matrizCinco,"sharpen_5",1/8)

def emboss(nwpath,tam,xt={}):
    matrizTres=[[-1,-1,0],[-1,0,1],[0,1,1]]
    matrizCinco=[[-1,-1,-1,-1,0],[-1,-1,-1,0,-1],[-1,-1,0,-1,-1],[-1,0,-1,-1,-1],[0,-1,-1,-1,-1]]
    if tam == 3:
        convolucion.convol_matriz(nwpath,matrizTres,"emboss_3",1)
    elif tam ==5:
        convolucion.convol_matriz(nwpath,matrizCinco,"emboss_5",1)


def inicio():
    path=raw_input("\n\n\nIngresa el nombre de la imagen que quieres procesar\n")
    print "Iniciando Blur"
    blur(path,5,{})
    print "Blur listo\nIniciando Motion Blur"
    motionBlur(path,3,{})
    print "Motion Blur listo\nIniciando Find Edges"
    findEdges(path,90,{})
    print "Find Edges listo\nIniciando Sharpen"
    sharpen(path,5,{})
    print "Sharpen listo\nIniciando emboss"
    findEdges(path,5,{})
    print "Emboss listo"


"""    print "Iniciando Escala de Grises"
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
"""

inicio()
#brillo("jemma.png",{'constante':-90})
#escalaDeGrises("av.jpg",{})
#motionBlur("av.jpg",9,{})
#findEdges("jemma.png",45,{})

#emboss("aos.jpeg",5,{})
