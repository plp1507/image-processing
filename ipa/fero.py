#! /bin/python3

import cv2 as cv
import numpy as np
from math import e, pi, floor
from matplotlib import pyplot as plt

def mmorph(imagem):

    image = cv.imread(imagem)
    img = np.zeros([image.shape[0], image.shape[1]], dtype = float)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):  
                img[i][j] += image[i][j][k]
            img[i][j] /= 3

    edge = np.zeros([3,3], dtype = float)

    g1 = 1/((2*pi)**0.5)
    g2 = -pi*g1
    
    for i in range(3):
        for j in range(3):
            edge[i][j] = -g1*e**(g2*(((i-1)**2)+((j-1)**2)))
    
    edge[1][1] += 1 

    nimg = np.zeros([image.shape[0], image.shape[1]], dtype = float)

    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            for k in range(3):
                for l in range(3):
                    nimg[i][j] += edge[k][l]*img[i-k][j-l]
            nimg[i][j] = abs(int(nimg[i][j]))
    
    plt.imshow(nimg)
    plt.colorbar()
    plt.show()
    return

mmorph("./images/bug.png")
