#! /bin/python3

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
from math import pi, e, floor

image = cv.imread('./images/cure.jpg')

dimF = 3
mdimF = floor(dimF/2)
ar = dimF**2

jpim = np.zeros([image.shape[0]+2*mdimF, image.shape[1]+2*mdimF], dtype = float) 

for i in range( len(image)-1):
    for j in range(len(image[0])-1):
        for k in range(0, 2):
            jpim[i+mdimF][j+mdimF] += image[i][j][k]
        jpim[i+mdimF][j+mdimF] /= 3

filt = np.zeros([dimF, dimF], dtype = float)
sigma = 1
sig2 = sigma**2

gauss1 = 1/(2*pi*sig2)
gauss2 = gauss1*pi

edge = np.zeros([dimF, dimF], dtype = float)
blur = np.zeros([dimF, dimF], dtype = float)
shar = np.zeros([dimF, dimF], dtype = float)
norm = np.zeros([dimF, dimF], dtype = float)

norm[mdimF][mdimF] = 1
beta = 3

#sharpening mask
for i in range(dimF):
    for j in range(dimF):
        blur[i][j] = gauss1*e**((((i-mdimF)**2)+((j-mdimF)**2))*gauss2)
        edge[i][j] = norm[i][j] - blur[i][j]
        shar[i][j] = norm[i][j] + edge[i][j]

sharp = np.zeros([image.shape[0], image.shape[1]], dtype = float)

for i in range(mdimF, image.shape[0]-mdimF):
    for j in range(mdimF, image.shape[1]-mdimF):
        for k in range(dimF):
            for l in range(dimF):
                sharp[i+mdimF][j+mdimF] += ar * blur[k][l] * jpim[i+k][j+l]
        if sharp[i][j] > 255:
            sharp[i+mdimF][j+mdimF] = 255
        if sharp[i+mdimF][j+mdimF] < 0:
            sharp[i+mdimF][j+mdimF] = 0
        #sharp[i+mdimF][j+mdimF] = jpim[i][j] - sharp[i+mdimF][j+mdimF]

#sharp[0][0] = 255

plt.imshow(sharp, cmap = 'gray')
plt.colorbar()
plt.show()

