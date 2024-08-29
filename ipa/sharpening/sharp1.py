from math import e, floor, pi
from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

dimF = 3
mdimF = floor(dimF/2)
ar = dimF**2
image = cv.imread("./images/bug.png")
imag = np.zeros([image.shape[0]+2*mdimF, image.shape[1]+2*mdimF], dtype = float)

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        for k in range(0,2):
            imag[i+1][j+1] += image[i][j][k]
        imag[i+1][j+1] /= 3

#gaussian blur parameters
sigma = 1
g1 = 1/(2*pi*sigma)

blur = np.zeros([dimF, dimF], dtype = float)
norm = np.zeros([dimF, dimF], dtype = float)
edge = np.zeros([dimF, dimF], dtype = float)
shar = np.zeros([dimF, dimF], dtype = float)
norm[mdimF][mdimF] = 1
beta = 5


for i in range(dimF):
    for j in range(dimF):
        blur[i][j] = g1*e**(-(((i-mdimF)**2)+((j-mdimF)**2))*g1*pi)
        edge[i][j] = norm[i][j] - blur[i][j]
        #shar[i][j] = norm[i][j] +beta*(norm[i][j] - blur[i][j])
        shar[i][j] = (beta+1)*norm[i][j] - beta*blur[i][j]
        #shar[i][j] = norm[i][j] + beta*edge[i][j]


#convolution
sharp = np.zeros([image.shape[0], image.shape[1]], dtype = float)


for i in range(mdimF, len(imag)-mdimF-2):
    for j in range(mdimF, len(imag[0])-mdimF-2):
        for k in range(dimF):
            for l in range(dimF):
                sharp[i][j] += shar[k][l] * imag[i+k][j+l]
        if sharp[i][j] > 255:
            sharp[i][j] = 255
        if sharp[i][j] < 0:
            sharp[i][j] = 0


plt.imshow(sharp, cmap = 'gray')
plt.colorbar()
plt.show()


