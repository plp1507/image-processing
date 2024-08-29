#! /bin/python3

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from math import e, pi, floor


def edg(pict, beta, cont):
    imagem = cv.imread(pict)
    image = np.zeros([imagem.shape[0], imagem.shape[1]], dtype = float)

    for i in range(imagem.shape[0]):
        for j in range(imagem. shape[1]):
            for k in range(2):
                image[i][j] += imagem[i][j][k]
            image[i][j] /= 3

    #gaussian blur parameters
    sigma = 1
    sig2 = sigma**2
    g1 = 1/(2*pi*sig2)
    g2 = -g1*pi

    dimF = 3
    mdimF = 1

    blur = np.zeros([dimF, dimF], dtype = float)
    norm = np.zeros([dimF, dimF], dtype = float)
    edge = np.zeros([dimF, dimF], dtype = float)

    norm[mdimF][mdimF] = beta

    for i in range(dimF):
        for j in range(dimF):
            blur[i][j] = g1*(e**(g2*(((i-mdimF)**2)+((j-mdimF)**2))))
            edge[i][j] = norm[i][j] - beta*blur[i][j]

    contV = cont/65536


    nimg = np.zeros([imagem.shape[0], imagem.shape[1]], dtype = float)

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            nimg[i][j] = (nimg[i][j]**3)*contV


    for i in range(mdimF, len(nimg)-mdimF):
        for j in range(mdimF, len(nimg[0])-mdimF):
            for k in range(dimF):
                for l in range(dimF):
                    nimg[i][j] += edge[k][l]*image[i-k][j-l]
            nimg[i][j] = abs(nimg[i][j])

            if nimg[i][j] >255 :
                nimg[i][j] = 255


    nimI = np.zeros([imagem.shape[0], imagem.shape[1]], dtype = int)
    freq = np.zeros(256, dtype = int)

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            nimI[i][j] = int(nimg[i][j])
            freq[nimI[i][j]] += 1

    dfrq = np.zeros(256, dtype = int)
    dfrS = np.zeros(256, dtype = int)

    for i in range(256):
        if i > 0:
            dfrq[i] = freq[i] - freq[i-1]
        else:
            dfrq[i] = 0
        dfrS[i] = dfrq[i]

    dfrS.sort()

    for i in range(256):
        if dfrq[i] == dfrS[-1]:
            mxthr = i
        if dfrq[i] == dfrS[0]:
            mnthr = i

    for i in range(len(nimI)):
        for j in range(len(nimI[0])):
            if nimI[i][j] < mnthr or nimI[i][j] > mxthr:
                nimI[i][j] = 0
            else:
                nimI[i][j] = 255

    return nimI

plt.imshow(edg("../images/Untitled.jpeg", 2, 1), cmap = 'gray')
plt.show()
