#! /bin/python3
#import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from math import e, pi, floor
dimIx = 400
dimIy = 360

image = np.zeros([dimIx, dimIy], dtype = float)

for i in range(40, dimIx-40):
    for j in range(60, dimIy-60):
        image[i][j] = 255

dimF = 3
mdimF = floor(dimF/2)
blur = np.zeros([dimF,dimF], dtype = float)
g1 = 1/(2*pi)
g2 = -g1*pi

for i in range(dimF):
    for j in range(dimF):
        blur[i][j] = g1*e**(g2*(((i-mdimF)**2)+((j-mdimF)**2)))

plt.imshow(image)
plt.show()
