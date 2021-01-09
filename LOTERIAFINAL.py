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

###- - - - - - - > FUNCIÓN PARA ENCONTRAR EL GANADOR
conteo1=np.zeros([4,4])  #La matriz donde se "cuenta" el tablero
conteo2=np.zeros([4,4])
Leyenda=["0","¡¡LOTERIA!! JUGADOR 1","¡¡LOTERIA!! JUGADOR 2","Empate, TODOS GANAN"]
#Cuando se gane se mostrara una de estas leyendas dependiendo el caso
def QUIENGANA():
    global conteo1  #Se declara global la variable para poder usarla dentro de la función
    global conteo2
    Puntuacion1=0   #Se declaran las variables de puntuación
    Puntuacion2=0
    if (int(conteo1.sum())>=4):    #Condiciones para gane del jugador 1
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
    if (int(conteo1.sum())>=4):  #Condiciones para gane del jugador 2
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
    if (Puntuacion1==1 and Puntuacion2==1):   #En caso de empate
        Ganador=3
    elif (Puntuacion1>Puntuacion2):     #En caso de ganar el jugador 1
            Ganador=1
    elif(Puntuacion1<Puntuacion2):      #En caso de ganar el jugador 2
            Ganador=2    
    else:
            Ganador=0
    return Ganador     #Se retorna el valor para saber el ganador

###- - - - - - - > FUNCIÓN PARA DETECTAR PERFILES DE NUMEROS
def SacadodePerfilNumero():
    #Se coloca el url de la cámara
    url = "http://10.0.0.11:8080/shot.jpg"
    #Pausa de 5 segundos para enfocar
    time.sleep(5)
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    #Se decodifica el array
    img = cv2.imdecode(imgNp,-1)
    #Se guarda la imagen como png
    cv2.imwrite('imagen.png', img)
    #Se abre la imagen
    im = Image.open('imagen.png')
    #Se rota 270 grados
    angle = 270
    out = im.rotate(angle, expand=True)
    #Se muestra la imagen
    #Se guarda la imagen como output
    out.save('output.jpg')
    ########IMAGEN CAPTURADA POR EL TELEFONO
    plt.imshow(out)
    #Se lee la imagen y se obtiene su tamaño
    image = cv2.imread('output.jpg')
    [filas,col,capa]=image.shape
    n=round(filas/6)
    m=round(col/4)
    #Se hace un recorte para identificar el número
    recorte=image[0:n,0:m,:]
    original = image.copy()
    gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 60,255, cv2.THRESH_BINARY_INV)[1]
    ROI_number = 0
    VectorX=[]
    Vector=[]
    kernel = np.ones((13,13),np.uint8)
    thresh=cv2.erode(thresh,kernel)
    kernel2=np.ones((7,7),np.uint8)
    thresh=cv2.dilate(thresh,kernel2)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    Res=[0,1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if (h>100 and h<225) and (w>50 and w<200):
            Vector.append([x,y,w,h])
            VectorX.append(x)
    
    VectorX=np.argsort(VectorX)
    for u in range(len(VectorX)):  
        [x,y,w,h]=Vector[VectorX[u]]
        cv2.rectangle(thresh, (x, y), (x + w, y + h), (36,255,12), 2)
        ROI = original[y:y+h, x:x+w]
        cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        ROI_number += 1
    
    #CARGA DE LA DATA (Perfiles de los numeros)
    A=[0,1,2,3,4,5,6,7,8,9]
    A[0] = np.load('perfil0.npy')
    A[1] = np.load('perfil1.npy')
    A[2] = np.load('perfil2.npy')
    A[3] = np.load('perfil3.npy')
    A[4] = np.load('perfil4.npy')
    A[5] = np.load('perfil5.npy')
    A[6] = np.load('perfil6.npy')
    A[7] = np.load('perfil7.npy')
    A[8] = np.load('perfil8.npy')
    A[9] = np.load('perfil9.npy')
    res=''     #Variable que dara el numero detectado
    k=0
    while k<ROI_number:
        Ima=io.imread('ROI_{}.png'.format(k))
        gris=np.uint8(color.rgb2gray(Ima)*255)
        umbral= 60
        binario=(gris<umbral).astype(int)
        binario=morphology.binary_erosion(binario) 
        binario=morphology.binary_dilation(binario) #Eliminación de huecos y manchas 
        ima2=binario  #Recorte del numero
        
        #OBTENCIÓN DE LOS PERFILES DEL NUMERO
        perfiles=[]
        for i in range(ima2.shape[0]):
            for j in range(ima2.shape[1]):
                if (ima2[i,j]==1):
                    perfiles.append(j)
                    break
        
        for i in range(ima2.shape[0]):
            for j in range(ima2.shape[1]-1,0,-1):
                if (ima2[i,j]==1):
                    perfiles.append(j)
                    break
        
        #NORMALIZAMOS
        maximo=max(perfiles)
        for i in range(len(perfiles)):
            perfiles[i]=perfiles[i]/maximo
        
        #Estandarizamos el tamaño del vector del perfil a 200 valores maximo
        B=list(np.array(Image.fromarray(np.array(perfiles)).resize((1,200))))
        
        #Comparamos el perfil obtenido con la base de datos
        C=[]
        for i in A:
            C.append(abs(i-B))
        #Buscamos el valor minimo obtenido para hallar nuestra respuesta
        R=[]    
        for i in C:
            R.append(sum(i))
        #Mostramos el resultado obtenido
        x,y=np.where(R==min(R))
        res+=str(x[0])
        k+=1
    return res,out

###- - - - - - - > FUNCIÓN PARA DETECTAR PERFILES PARTE INFERIOR DE LA CARTA
def SacadodePerfilLetras(Ima):
    A= np.load('letrascartas.npy')   #Data de los perfiles de las palabras
    res=''
    #Ima=io.imread('output.jpg')  #Cambiamos de placa a conveniencia
    gris=np.uint8(color.rgb2gray(Ima)*255)
    #PREPROCESADO Y BINARIZACIÓN
    umbral= 60  #Umbral automatico
    binario=(gris<umbral).astype(int)
    binario=morphology.binary_erosion(binario)      #Eliminación de huecos y manchas 
    binario=morphology.binary_dilation(binario)
    [filas,col]=binario.shape
    n=round(filas/7)
    #Se hace un recorte para identificar el número
    recorte=binario[filas-n:filas,:]
    
    #OBTENCIÓN DE LOS PERFILES DEL NUMERO
    ima2=np.uint8(recorte)
    perfiles=[]
    for j in range(ima2.shape[1]):
        for i in range(ima2.shape[0]-1,0,-1):
            if (ima2[i,j]==1):
                perfiles.append(i)
                break    
    
    #NORMALIZAMOS
    maximo=max(perfiles)
    for i in range(len(perfiles)):
        perfiles[i]=perfiles[i]/maximo
    
    #Estandarizamos el tamaño del vector del perfil a 200 valores maximo
    B=list(np.array(Image.fromarray(np.array(perfiles)).resize((1,200))))
    
    #Comparamos el perfil obtenido con la base de datos
    C=[]
    for i in A:
        C.append(abs(i-B))
    #Buscamos el valor minimo obtenido para hallar nuestra respuesta
    R=[]    
    for i in C:
        R.append(sum(i))
    #Mostramos el resultado obtenido
    x,y=np.where(R==min(R))
    #print(str(x[0]))
    res+=str(x[0])
    res=int(res)+1
    #print('Es la carta: ',res)
    return res


###INTERFAZ
#Se carga la base de datos de las cartas para hacer el tablero
A=np.load('BASEcartasESTESI.npy')
#Se hace la selección aleatoria del numero de carta entre 1 y 54
tablero1=np.random.choice(54, 16, replace=False)+1
tablero2=np.random.choice(54, 16, replace=False)+1
np.save("tablero1",tablero1)  #Se guardan porque se usan despues con el conteo
np.save("Tablero2",tablero2)

#Se declara una lista que guardara cada carta del tablero
B1=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]   #Jugador 1
B2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]   #Jugador 2

root = tkinter.Tk()     #Declaramos la ventana de la interfaz
root.iconbitmap("Tablero1.ico")    #Le ponemos un icono
root.title("Loteria")     #titulo
miframe=tkinter.Frame(root,width=1000,height=1000)  #Declaramos el frame donde cargaremos los tableros
miframe.pack()
#En el siguiente while se muestra en la interfaz cada componente de ambos tableros
k=0
while (k<16):
    for i in [0,1,2,3]:
        for j in [0,1,2,3]:
            B1[k]=Image.fromarray(np.array(A[tablero1[k]])).resize((105,172))  #Reajuste para que quepan
            B2[k]=Image.fromarray(np.array(A[tablero2[k]])).resize((105,172))
            B1[k] = ImageTk.PhotoImage(image=B1[k]) 
            resultado1=tkinter.Label(miframe, image=B1[k],width=105,height=172)
            resultado1.grid(row=i,column=j)
            B2[k] = ImageTk.PhotoImage(image=B2[k]) 
            resultado2=tkinter.Label(miframe, image=B2[k],width=105,height=172)
            resultado2.grid(row=i,column=j+5)
            k=k+1
#end 
#Se carga en la interfaz el titulo 
D1=Image.open("Laloteria.jpg")
D1=ImageTk.PhotoImage(image=D1) 
resultado1=tkinter.Label(miframe, image=D1,width=508,height=172)
resultado1.grid(row=0,column=4)

#Se carga en la interfaz el señalador de jugadores
D2=Image.open("Jugadores.jpg")
D2=ImageTk.PhotoImage(image=D2)
resultado=tkinter.Label(miframe,image=D2,width=508,height=172)
resultado.grid(row=3,column=4)

#Se carga en la imagen del frijol para marcar las cartas
D3=Image.open("frijol.png")
D3=ImageTk.PhotoImage(image=D3) 
Ncarta=tkinter.Label(root, text="Ahi vienen las cartas")    #Aqui se mostrara el numero de la carta identificada
Ncarta.place(x=524,y=321)
WHO=tkinter.Label(root, text="Corre, corre y se va corriendo...")  #otro texto...
WHO.place(x=524,y=301)

def clicked():      #Función que se activa cuando demos clic en el boton
    global A,root,miframe,D,conteo1,conteo2   #Se cargan las variables como locales para usarlas en la función
    # global root
    # global miframe
    # global D
    # global conteo1,conteo2
    n,Entrada1=SacadodePerfilNumero()    #Se obtiene el perfil por numeros
    #print(n)
    n2=SacadodePerfilLetras(np.array(Entrada1))  #Se obtiene el perfil por palabras
    #print(n2)
    if (n==n2):   #Si son iguales no hay problema, sino entonces se confia mas en perfiles numeros
        n=n2
    Ncarta.configure(text=n)  #Se muestra que numero es
    tablero1=np.load("tablero1.npy")
    tablero2=np.load("tablero2.npy")
    tab1=tablero1.reshape(4,4)    #Los tableros pasan de vector a matriz para identificar 
    tab2=tablero2.reshape(4,4)     #posición en el tablero
    n=int(n)
    for i in tablero1:     
        if i==n:         #Si la carta leida en el tablero 1 entonces pone el frijol
            y1,x1=np.where(tab1==n)
            resultado=tkinter.Label(miframe, image=D3,width=105,height=172)
            resultado.grid(row=int(y1),column=int(x1))
            conteo1[y1,x1]=1    #Se registra en el contador
    #end
    for i in tablero2:
        if i==n:         #Si la carta leida en el tablero 1 entonces pone el frijol
            y2,x2=np.where(tab2==n) 
            resultado=tkinter.Label(miframe, image=D3,width=105,height=172)
            resultado.grid(row=int(y2),column=int(x2)+5)
            conteo2[y2,x2]=1   #Se registra en el contador
    #end
    Winner=QUIENGANA()   #Se comprueba si alguien ya gano
    #print(Winner)
    if (int(Winner)>0):     #Si hay un ganador entonces mostrara quien fue
        WHO.configure(text=Leyenda[int(Winner)])
#end

#Se declara el botón que ejecutara la función (toma de foto, y determinación de si existe en los tableros)
btn=tkinter.Button(root, text="TOMAR FOTO",command=clicked)   
btn.place(x=524,y=258)

root.mainloop()   #Para correr la interfaz

