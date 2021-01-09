'RECONOCIMIENTO DE PATRONES'
'Lotería'
'Gonzalez Espinosa Yslen Anahi'
'Vargas Téllez Axel Dali'
import cv2
import numpy as np
from PIL import Image
import urllib.request
import urllib
from skimage import io, color, morphology
import matplotlib.pyplot as plt
import time

plt.close('all')
'OPCIÓN SI SE TIENE IP CAMERA'
# #Se coloca el url de la cámara
# url = "http://192.168.1.64:8080/shot.jpg"
# #Pausa de 5 segundos para enfocar
# time.sleep(5)
# imgResp = urllib.request.urlopen(url)
# imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
# #Se decodifica el array
# img = cv2.imdecode(imgNp,-1)
# #Se muestra la imagen
# cv2.imshow('IPWebcam',img)
# #Se guarda la imagen como png
# cv2.imwrite('imagen.png', img)
# #Se abre la imagen
# im = Image.open('imagen.png')
# #Se rota 270 grados
# angle = 270
# out = im.rotate(angle, expand=True)
# #Se muestra la imagen
# plt.imshow(out)
# #Se guarda la imagen como output
# out.save('output.jpg')
# #Se lee la imagen y se obtiene su tamaño
# image = cv2.imread('output.jpg')

'OPCION SIN IP CAMERA'
image=io.imread('carta33.jpg')
[filas,col,capa]=image.shape
#Se selecciona 1/6 de la altura y 1/4 del ancho de la imagen
n=round(filas/6)
m=round(col/4)
#Se hace un recorte para identificar el número
recorte=image[0:n,0:m,:]
original = image.copy()
#Se convierte de BGR a gris
gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
#Se convierte a binario con umbral de 60
thresh = cv2.threshold(gray, 60,255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow('imatt', thresh)
ROI_number = 0
VectorX=[]
Vector=[]
#Se aplica erosión con kernel 13
kernel = np.ones((13,13),np.uint8)
thresh=cv2.erode(thresh,kernel)
#Se aplica dilatación con kernel 7
kernel2=np.ones((7,7),np.uint8)
thresh=cv2.dilate(thresh,kernel2)
#Se identifican los contornos 
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#Se obtienen 'recuadros' delimitando los contornos de la figura
for c in cnts:
    #Se guarda el valor de inicio y final para ancho y alto
    x,y,w,h = cv2.boundingRect(c)
    #Si el recuadro marcado tiene una altura entre 100 y 255
    #y un ancho de entre 50 y 200, entonces se guardan sus valores
#(esto se hace con el fin de eliminar pequeños contornos que son identificados en la imagen y que no corresponden al número)
    if (h>100 and h<225) and (w>50 and w<200):
        Vector.append([x,y,w,h])
        VectorX.append(x)
#Se ordenan los valores en x de los rectángulos obtenidos, ya que en ocasiones cv2 a veces detectaba primero el segundo número 
VectorX=np.argsort(VectorX)
#Ya ordenados, podemos realizar el recorte y nombrar las imágenes correctamente
for u in range(len(VectorX)):  
    [x,y,w,h]=Vector[VectorX[u]]
    cv2.rectangle(thresh, (x, y), (x + w, y + h), (36,255,12), 2)
    ROI = original[y:y+h, x:x+w]
    cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
    ROI_number += 1

cv2.imshow('image', recorte)
cv2.imshow('ima', thresh)
cv2.imshow('gray',gray)

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

res=''
k=0
while k<ROI_number:
    Ima=io.imread('ROI_{}.png'.format(k))
    plt.figure()
    plt.imshow(np.uint8(Ima))
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
    plt.figure()
    plt.plot(B)
    #Comparamos el perfil obtenido con la base de datos
    C=[]
    for i in A:
        C.append(abs(i-B))
    #Buscamos el valor minimo obtenido para hallar nuestra respuesta
    R=[]    
    for i in C:
        R.append(sum(i))
    #Encontramos el mínimo
    x,y=np.where(R==min(R))
    #Almacenamos el resultado y concatenamos (por si hay dos números)
    res+=str(x[0])
    k+=1
#Muestreo del resultado
print('Es la carta: ',res)