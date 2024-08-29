#! /bin/python3

from matplotlib import pyplot as plt
from math import e, pi, floor
import numpy as np
import cv2 as cv

image = cv.imread("./pesq/images/bug.png")

img = np.zeros([image.shape[0], image.shape[1]], dtype = float)

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        for k in range(2):
            img[i][j] += image[i][j][k]
        img[i][j] /= 3

blim = np.zeros([image.shape[0], image.shape[1]], dtype = float)

blur = np.zeros([3,3], dtype = float)

g1 = 1/((2*pi)**0.5)
g2 = -g1*pi

for i in range(3):
    for j in range(3):
        blur[i][j] = -g1*e**(g2*(((i-1)**2)+((j-1)**2)))

blur[1][1] += 1

edge = np.zeros([img.shape[0], img.shape[1]], dtype = float)

cont = 1/35

for i in range(3,img.shape[0]-3):
    for j in range(3,img.shape[1]-3):
        blim[i][j] = ((img[i][j])**3)*(cont**2)
        if (((img[i][j])**3)*(cont**2)) < 255:
            blim[i][j] = ((img[i][j])**3)*(cont**2)
        else:
            blim[i][j] = 255
        for k in range(3):
            for l in range(3):
                edge[i][j] += blur[k][l] * blim[i-k][j-l]
        edge[i][j] = abs(edge[i][j])
        if edge[i][j] <= 4:
            edge[i][j] = 0
        else:
            edge[i][j] = 255

b = np.zeros([40,40], dtype = float)

mbx = floor(b.shape[0]/2)
mby = floor(b.shape[1]/2)

for i in range(15, b.shape[0]-15):
    for j in range(15, b.shape[1]-15):
        b[i][j] = 255

fimg = np.zeros([image.shape[0], image.shape[1]], dtype = float)
bord = np.zeros([image.shape[0], image.shape[1]], dtype = float)

for i in range(mbx, image.shape[0]-mbx):
    for j in range(mby, image.shape[1]-mby):
        if edge[i][j] == 0:
            bord[i][j] = 0
        else:
            for k in range(b.shape[0]):
                for l in range(b.shape[1]):
                    bord[i+k-mbx][j+l-mby] += b[k][l]

for i in range(bord.shape[0]):
    for j in range(bord.shape[1]):
        if bord[i][j] < 1:
            bord[i][j] = 0
        else:
            bord[i][j] = 1





plt.imshow(bord)
plt.show()
