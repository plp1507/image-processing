#! /bin/python3

import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np



imag = cv.imread("../images/Untitled.jpeg")

image = np.zeros([imag.shape[0], imag.shape[1]], dtype = int)

for i in range(len(image)):
    for j in range(len(image[0])):
        for k in range(2):
            image[i][j] += imag[i][j][k]
        image[i][j] /= 3

a =5/65536

for i in range(imag.shape[0]):
    for j in range(imag.shape[1]):
        image[i][j] = int((image[i][j]**3)*a)
        if image[i][j] > 255:
             image[i][j] = 255


freq = np.zeros(256, dtype = int)

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        freq[image[i][j]] += 1


x = np.arange(256)

image[0][0] = 255

#plt.hist(x = x, bins = 256, weights = freq)
plt.imshow(image, cmap = 'gray')
plt.show()
