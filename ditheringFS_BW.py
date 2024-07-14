import cv2 as cv
import numpy as np
from math import floor
from matplotlib import pyplot as plt

image = 'image file path'

def Dither(filePATH):

    #grayscale conversion of the original image
    originalIMG = cv.imread(filePATH)
    grsclIMG = np.zeros([originalIMG.shape[0], originalIMG.shape[1]], dtype = float)
    
    #alternative to the original grayscaled converted image 
    #utilized to change the grscl. image pixel values without affecting the original
    grsclSIMG = np.zeros([originalIMG.shape[0], originalIMG.shape[1]], dtype = float)
    
    for i in range(grsclIMG.shape[0]):
        for j in range(grsclIMG.shape[1]):
            for k in range(3):
                grsclIMG[i][j] += originalIMG[i][j][k]
            grsclIMG[i][j] /= 3
            grsclSIMG[i][j] = grsclIMG[i][j]

    #dithering
    ditherIMG = np.zeros([grsclIMG.shape[0], grsclIMG.shape[1]], dtype = float)

    for i in range(1,ditherIMG.shape[0]-1):
        for j in range(1,ditherIMG.shape[1]-1):
            #quantizing each pixel value
            oldVALUE = grsclIMG[i][j]
            newVALUE = 255*round(oldVALUE/255)
            
            #quantization error evaluation
            quantERROR = oldVALUE - newVALUE

            #quantization error diffusion
            grsclSIMG[i+1][j]   += quantERROR*7/16
            grsclSIMG[i-1][j+1] += quantERROR*3/16
            grsclSIMG[i]  [j+1] += quantERROR*5/16
            grsclSIMG[i+1][j+1] += quantERROR*1/16
            ditherIMG[i][j]      = newVALUE

    return ditherIMG

finalIMG = Dither(image)

plt.imshow(finalIMG, cmap = 'gray')
plt.show()
