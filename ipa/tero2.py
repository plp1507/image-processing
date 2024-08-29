#! /bin/python3

import numpy as np
from math import e, pi, floor
from matplotlib import pyplot as plt

dimAx = 400
dimAy = 360
mdimAx = floor(dimAx/2)
mdimAy = floor(dimAy/2)

A = np.zeros([dimAx, dimAy], dtype = float)

Ao = np.zeros([dimAx, dimAy], dtype = float)

f = 30

for i in range(dimAx):
    for j in range(dimAy):
        if i < (dimAx-f) and i > f:
            if j < (dimAy-f) and j > f:
                Ao[i][j] = 255

        if (((i-mdimAx)**2)+(((j-mdimAy)*2)**2)) <= 25600 :
            A[i][j] = 255


dimF = 3
mdimF = floor(dimF/2)
g1 = 1/(2*pi)
g2 = -g1*pi
blur = np.zeros([dimF, dimF], dtype = float)

for i in range(dimF):
    for j in range(dimF):
        blur[i][j] = -g1*e**(g2*(((i-mdimF)**2)+((j-mdimF)**2)))

blur[mdimF][mdimF] += 1

nim = np.zeros([dimAx, dimAy], dtype = float)

for i in range(mdimF, dimAx-mdimF):
    for j in range(mdimF, dimAy-mdimF):
        for k in range(dimF):
            for l in range(dimF):
                nim[i][j] += blur[k][l]*Ao[i-k][j-l]
        nim[i][j] = abs(nim[i][j])
        nim[i][j] = ((nim[i][j]**3)*0.000137)
        
        if nim[i][j] > 0:
            nim[i][j] = 255
        else:
            nim[i][j] = 0

dimB = 39

mdimB = floor(dimB/2)

b = np.zeros([dimB, dimB], dtype = float)

for i in range(dimB):
    for j in range(dimB):
        if (((i-mdimB)**2) + ((j-mdimB)**2)) <= 324:
            b[i][j] = 1

snim = np.zeros([dimAx, dimAy], dtype = float)

for i in range(dimAx):
    for j in range(dimAy):
        if nim[i][j] == 255:
            for k in range(dimB):
                for l in range(dimB):
                    snim[i-mdimB+k][j-mdimB+l] += b[k][l]

for i in range(dimAx):
    for j in range(dimAy):
        if snim[i][j] >= 1:
            snim[i][j] = 255

eros = np.zeros([dimAx, dimAy], dtype = int)
dila = np.zeros([dimAx, dimAy], dtype = int)

for i in range(dimAx):
    for j in range(dimAy):
        #erosao
        if Ao[i][j] == 255:
            eros[i][j] = snim[i][j]
        #dilataçao
        if snim[i][j] == 255:
            dila[i][j] = snim[i][j] - Ao[i][j]

plt.imshow(eros)
plt.colorbar()
plt.show()
