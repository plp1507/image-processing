#Sharpening filter - by Pedro Lucca

from math import e, pi
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

def Sharpen(imgPATH, beta):
    image = cv.imread(imgPATH)

    grsclIMG = np.zeros([image.shape[0], image.shape[1]], dtype = float) 
    
    #conversion to grayscale
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):
                grsclIMG[i][j] += image[i][j][k]
            grsclIMG[i][j] /= 3
    
    #multiplying constant of the normal distribution function
    #*assuming standard deviation equal to 1
    gaussCONST = 1/(2*pi)

    sharpFILT = np.zeros([3, 3], dtype = float)

    #sharpening mask/filter:
    #*is equal to: impulse + beta*(impulse - blurring mask),
    #*impulse is equal to a square matrix with the value 1 in the center cell
    #*blurring mask is equal to the normal distribution matrix
    #*impulse - blurring mask is equal to the edge detection mask
    for i in range(3):
        for j in range(3):
            sharpFILT[i][j] = -(beta*gaussCONST)
            sharpFILT[i][j] *= e**(-(((i-1)**2)+((j-1)**2))*gaussCONST*pi)
    sharpFILT[1][1] += (beta + 1)
    
    #beta is a multiplying constant for the filteri, defined as a non-negative real number
    #refers to how much the edge is added to the original image
    #or, simply, as the intensity of the filter

    sharpenedIMG = np.zeros([image.shape[0], image.shape[1]], dtype = float)

    #convolution between image and sharpening mask
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):
                for l in range(3):
                    if (i+k) > (image.shape[0]-2) or (j+l) > (image.shape[1]-2):
                        sharpenedIMG[i][j] += grsclIMG[i][j]
                    else:
                        sharpenedIMG[i][j] += sharpFILT[k][l] * grsclIMG[i+k][j+l]
            #value clamping
            if sharpenedIMG[i][j] > 255:
                sharpenedIMG[i][j] = 255
            if sharpenedIMG[i][j] < 0:
                sharpenedIMG[i][j] = 0

    return sharpenedIMG

finalIMG = Sharpen('''image file path''' ,'''beta''')

plt.imshow(finalIMG, cmap = "gray")
plt.colorbar()
plt.show()
