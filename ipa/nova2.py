#! /bin/python3

from matplotlib import pyplot as plt
from math import e, pi, floor
import numpy as np
import cv2 as cv

#image = cv.imread("./images/boats.jpeg")
image = cv.imread("./images/bug.png")
#image = cv.imread("./images/mountain.jpeg")

img = np.zeros([image.shape[0], image.shape[1]], dtype = float)

#conversao para escala de cinza
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        for k in range(2):
            img[i][j] += image[i][j][k]
        img[i][j] /= 3

blim = np.zeros([image.shape[0], image.shape[1]], dtype = float)

#declaraçao dos parametros do filtro gaussiano e detecçao de borda
blur = np.zeros([3,3], dtype = float)

g1 = 1/((2*pi)**0.5)
g2 = -g1*pi

for i in range(3):
    for j in range(3):
        blur[i][j] = -g1*e**(g2*(((i-1)**2)+((j-1)**2)))

blur[1][1] += 1

edge = np.zeros([img.shape[0], img.shape[1]], dtype = float)

cont = 1/35

#aplicaçao de contraste e obtenção das bordas da imagem original
for i in range(3,img.shape[0]-3):
    for j in range(3,img.shape[1]-3):
        
        #contraste
        if (((img[i][j])**3)*(cont**2)) < 255:
            blim[i][j] = ((img[i][j])**3)*(cont**2)
        else:
            blim[i][j] = 255

        #convolução com o filtro
        for k in range(3):
            for l in range(3):
                edge[i][j] += blur[k][l] * blim[i-k][j-l]
        edge[i][j] = abs(edge[i][j])
        if edge[i][j] <= 4:
            edge[i][j] = 0
        else:
            edge[i][j] = 255

#declaraçao do elemento estruturante
b = np.zeros([40,40], dtype = int)

mbx = floor(b.shape[0]/2)
mby = floor(b.shape[1]/2)

for i in range(5, b.shape[0]-5):
    for j in range(5, b.shape[1]-5):
        b[i][j] = 1

bord = np.zeros([image.shape[0], image.shape[1]], dtype = float)

#aplicaçao da dilataçao nas bordas
for i in range(mbx, image.shape[0]-mbx):
    for j in range(mby, image.shape[1]-mby):
        if edge[i][j] == 0:
            bord[i][j] = 0
        else:
            for k in range(b.shape[0]):
                for l in range(b.shape[1]):
                    bord[i+k-mbx][j+l-mbx] += b[k][l]

#binarização da borda dilatada
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        if bord[i][j] == 0:
            bord[i][j] = 0
        else:
            bord[i][j] = 255

#plt.savefig("bdil.png")

#aplicaçao da erosao na figura preenchida com bordas dilatadas

edg2 = np.zeros([image.shape[0], image.shape[1]], dtype = float)

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        for k in range(3):
            for l in range(3):
                edg2[i][j] += bord[i+k-mbx][j+l-mby]*blur[k][l]
        edg2[i][j] = abs(edg2[i][j])
        if edg2[i][j] <= 6:
            edg2[i][j] = 0
        else:
            edg2[i][j] = 255



fimg = np.zeros([image.shape[0], image.shape[1]], dtype = float)

for i in range(b.shape[0]):
    for j in range(b.shape[1]):
        b[i][j] = 0

for i in range(12, b.shape[0]-12):
    for j in range(12,  b.shape[1]-12):
        b[i][j] = 1


for i in range(mbx, image.shape[0] - mbx):
    for j in range(mby, image.shape[1] - mby):
        if edg2[i][j] == 0:
            fimg[i][j] = 0
        else:
            for k in range(b.shape[0]):
                for l in range(b.shape[1]):
                    fimg[i+k-b.shape[0]][j+l-b.shape[1]] -= b[k][l]

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        fimg[i][j] += bord[i][j]
        if fimg[i][j] != 255:
            fimg[i][j] = 0
        else:
            fimg[i][j] = img[i][j]

plt.imshow(fimg)
plt.show()
