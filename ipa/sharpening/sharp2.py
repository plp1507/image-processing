from math import e, floor, pi
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np


def sharpen(image, filter_size, beta, sigma):
    mdimF = floor(filter_size/2)
    imag = cv.imread(image)
    img = np.zeros([imag.shape[0]+2*mdimF, imag.shape[1]+2*mdimF], dtype = float)

    for i in range(imag.shape[0]):
        for j in range(imag.shape[1]):
            for k in range(0,2):
                img[i+1][j+1] += imag[i][j][k]
            img[i+1][j+1] /= 3

    #gaussian blur parameters
    g1 = 1/(2*pi*sigma)

    blur = np.zeros([filter_size, filter_size], dtype = float)
    norm = np.zeros([filter_size, filter_size], dtype = float)
    edge = np.zeros([filter_size, filter_size], dtype = float)
    shar = np.zeros([filter_size, filter_size], dtype = float)
    norm[mdimF][mdimF] = 1

    for i in range(filter_size):
        for j in range(filter_size):
            blur[i][j] = g1*e**(-(((i-mdimF)**2)+((j-mdimF)**2))*g1*pi)
            edge[i][j] = norm[i][j] - blur[i][j]
            shar[i][j] = norm[i][j] + beta*edge[i][j]
            #shar[i][j] = (beta+1)*norm[i][j] - beta*blur[i][j]

    #convolution
    sharp = np.zeros([imag.shape[0], imag.shape[1]], dtype = float)
    
    
    for i in range(mdimF, len(imag)-mdimF-2):
        for j in range(mdimF, len(imag[0])-mdimF-2):
            for k in range(filter_size):
                for l in range(filter_size):
                    sharp[i][j] += edge[k][l] * img[i+k][j+l]
            if sharp[i][j] > 255:
                sharp[i][j] = 255
            if sharp[i][j] < 0:
                sharp[i][j] = 0

    plt.imshow(sharp, cmap = 'gray')
    plt.colorbar()
    plt.show()
    return

sharpen("./images/cure.jpg", 3, 1, 1)
