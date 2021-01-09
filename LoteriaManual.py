'RECONOCIMIENTO DE PATRONES'
'Lotería'
'Gonzalez Espinosa Yslen Anahi'
'Vargas Téllez Axel Dali'
import cv2
import numpy as np
from PIL import Image, ImageTk
import urllib.request
import urllib
import tkinter
from skimage import io, color, filters, measure, morphology
import matplotlib.pyplot as plt
import time

###Puntos ganadores
conteo1=np.zeros([4,4])
conteo2=np.zeros([4,4])
Leyenda=["0","Empate, TODOS GANAN","¡¡LOTERIA!! JUGADOR 1","¡¡LOTERIA!! JUGADOR 2"]
def QUIENGANA():
    #Definimos variables globales
    global conteo1
    global conteo2
    Puntuacion1=0
    Puntuacion2=0
    #Verificamos si ya se marcaron cuatro cartas en el tablero 1
    if (int(conteo1.sum())>=4):
        #Verificamos si hay 4 cartas marcadas en línea (10 condiciones)
        if (((conteo1[1,1] and conteo1[1,2] and conteo1[1,3] and conteo1[1,0])==1)
        or
        ((conteo1[2,1] and conteo1[2,2] and conteo1[2,3] and conteo1[2,0])==1)
        or
        ((conteo1[3,1] and conteo1[3,2] and conteo1[3,3] and conteo1[3,0])==1)
        or
        ((conteo1[0,0] and conteo1[0,2] and conteo1[0,3] and conteo1[0,1])==1)
        or
        ((conteo1[1,1] and conteo1[2,1] and conteo1[3,1] and conteo1[0,1])==1)
        or
        ((conteo1[1,2] and conteo1[2,2] and conteo1[3,2] and conteo1[0,2])==1)
        or
        ((conteo1[1,3] and conteo1[2,3] and conteo1[3,3] and conteo1[0,3])==1)
        or
        ((conteo1[1,0] and conteo1[2,0] and conteo1[3,0] and conteo1[0,0])==1)
        or
        ((conteo1[1,1] and conteo1[2,2] and conteo1[3,3] and conteo1[0,0])==1)
        or
        ((conteo1[0,3] and conteo1[1,2] and conteo1[2,1] and conteo1[3,0])==1)):
            Puntuacion1=1
    #Verificamos si ya se marcaron cuatro cartas en el tablero 2
    if (int(conteo1.sum())>=4):
        #Verificamos si hay 4 cartas marcadas en línea (10 condiciones)
        if (((conteo2[1,1] and conteo2[1,2] and conteo2[1,3] and conteo2[1,0])==1)
        or     
        ((conteo2[2,1] and conteo2[2,2] and conteo2[2,3] and conteo2[2,0])==1)
        or
        ((conteo2[3,1] and conteo2[3,2] and conteo2[3,3] and conteo2[3,0])==1)
        or
        ((conteo2[0,1] and conteo2[0,2] and conteo2[0,3] and conteo2[0,0])==1)
        or
        ((conteo2[1,1] and conteo2[2,1] and conteo2[3,1] and conteo2[0,1])==1)
        or
        ((conteo2[1,2] and conteo2[2,2] and conteo2[3,2] and conteo2[0,2])==1)
        or
        ((conteo2[1,3] and conteo2[2,3] and conteo2[3,3] and conteo2[0,3])==1)
        or
        ((conteo2[1,0] and conteo2[2,0] and conteo2[3,0] and conteo2[0,0])==1)
        or
        ((conteo2[1,1] and conteo2[2,2] and conteo2[3,3] and conteo2[0,0])==1)
        or
        ((conteo2[0,3] and conteo2[1,2] and conteo2[2,1] and conteo2[3,0])==1)):
            Puntuacion2=1
    #Si ambos tableros tienen 4 cartas en línea
    if (Puntuacion1==Puntuacion2==1):
        #Empate
        Ganador=1
    #Si solo el jugador 1 tiene 4 en línea
    elif (Puntuacion1>Puntuacion2):
        #Gana Jugador 1
        Ganador=2
    #Si solo el jugador 2 tiene 4 en línea
    elif (Puntuacion2>Puntuacion1):
        #Gana Jugador 2
        Ganador=3
    #Si ningún jugador tiene 4 cartas en línea
    else:
        #Nadie Gana aún
        Ganador=0
    return Ganador

###INTERFAZ
#Se carga la base de datos con los valores de píxel para cada carta
A=np.load('BASEcartasESTESI.npy')
#Se crean los tableros de forma aleatoria
tablero1=np.random.choice(54, 16, replace=False)+1
tablero2=np.random.choice(54, 16, replace=False)+1
#Se guardan los tableros
np.save("tablero1",tablero1)
np.save("Tablero2",tablero2)

B1=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
B2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

root = tkinter.Tk()  
root.iconbitmap("Tablero1.ico")
root.title("Loteria")
miframe=tkinter.Frame(root,width=1000,height=1000)
miframe.pack()

k=0
while (k<16):
    B1[k]=Image.fromarray(np.array(A[tablero1[k]])).resize((105,172))
    B2[k]=Image.fromarray(np.array(A[tablero2[k]])).resize((105,172))
    k=k+1

k=0
while (k<16):
    for i in [0,1,2,3]:
        for j in [0,1,2,3]:
            B1[k] = ImageTk.PhotoImage(image=B1[k]) 
            resultado1=tkinter.Label(miframe, image=B1[k],width=105,height=172)
            resultado1.grid(row=i,column=j)
            B2[k] = ImageTk.PhotoImage(image=B2[k]) 
            resultado2=tkinter.Label(miframe, image=B2[k],width=105,height=172)
            resultado2.grid(row=i,column=j+5)
            k=k+1

D1=Image.open("Laloteria.jpg")
D1=ImageTk.PhotoImage(image=D1) 
resultado1=tkinter.Label(miframe, image=D1,width=508,height=172)
resultado1.grid(row=0,column=4)

D2=Image.open("Jugadores.jpg")
D2=ImageTk.PhotoImage(image=D2)
resultado=tkinter.Label(miframe,image=D2,width=508,height=172)
resultado.grid(row=3,column=4)

D3=Image.open("frijol.png")
D3=ImageTk.PhotoImage(image=D3) 
Ncarta=tkinter.Label(root, text="Ahi vienen las cartas")
Ncarta.place(x=674,y=321)
WHO=tkinter.Label(root, text="Corre, corre y se va corriendo...")
WHO.place(x=674,y=301)

#Si se presiona el botón...
def clicked():
    global A
    global root
    global miframe
    global D
    global conteo1,conteo2
    #Ingresar número de carta en la consola
    n=int(input('Número de carta: '))
    Ncarta.configure(text=n)
    tablero1=np.load("tablero1.npy")
    tablero2=np.load("tablero2.npy")
    tab1=tablero1.reshape(4,4)
    tab2=tablero2.reshape(4,4)
    n=int(n)
    #Verificamos si la carta n está en el tablero 1
    for i in tablero1:
        if i==n:
            y1,x1=np.where(tab1==n)
            resultado=tkinter.Label(miframe, image=D3,width=105,height=172)
            resultado.grid(row=int(y1),column=int(x1))
            #Si si, entonces se marca con un 1 la posición correspondiente
            conteo1[y1,x1]=1
    #Verificamos si la carta n está en el tablero 2
    for i in tablero2:
        if i==n:
            y2,x2=np.where(tab2==n)
            resultado=tkinter.Label(miframe, image=D3,width=105,height=172)
            resultado.grid(row=int(y2),column=int(x2)+5)
            #Si si, entonces se marca con un 1 la posición correspondiente
            conteo2[y2,x2]=1
    #Llamamos la función que determina quién gana
    Winner=QUIENGANA()
    #Si es mayor a 0 (o sea, si es empate o un jugador gana)
    if (Winner>0):
        #Desplegamos el resultado
        WHO.configure(text=Leyenda[int(Winner)])

btn=tkinter.Button(root, text="Ingresar Número",command=clicked)
btn.place(x=674,y=258)

root.mainloop()