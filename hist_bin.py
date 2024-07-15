'''
Histogram and image binarization - by Pedro Lucca

The following code has the goal of obtaining an image's tone frequency distribution (the histogram)
and utilizes this tool to binarize said image. The algorithm finds the biggest positive and negative
change in the tone distribution and applies the value 0 (pure black, in color) to the pixels within
the two bounds and 255 (pure white, in color) to the ones outside, essentially separating the region
with most tonal content*.

*this statement is not always true and depends on the image utilized...
'''

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def Hist(filePATH):
    image = cv.imread(filePATH)
    grsclIMG = np.zeros([image.shape[0], image.shape[1]], dtype = int)
    float_grsclIMG = np.zeros([image.shape[0], image.shape[1]], dtype = float)
    freq = np.zeros(256, dtype = int)
    normFREQ = np.zeros(256, dtype = float)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):
                float_grsclIMG[i][j] += image[i][j][k]
            float_grsclIMG[i][j] /= 3
            grsclIMG[i][j] = int(float_grsclIMG[i][j])
            freq[grsclIMG[i][j]] += 1

    for i in range(255):
        normFREQ[i] = freq[i]/(image.shape[0]*image.shape[1])

    return normFREQ

def Binarize(filePATH, tolerance):
    freq = Hist(filePATH)
    image = cv.imread(filePATH)
    grsclIMG = np.zeros([image.shape[0], image.shape[1]], dtype = int)
    float_grsclIMG = np.zeros([image.shape[0], image.shape[1]], dtype = float)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(3):
                float_grsclIMG[i][j] += image[i][j][k]
            float_grsclIMG[i][j] /= 3
            grsclIMG[i][j] = int(float_grsclIMG[i][j])

    dfSORT = np.zeros(256, dtype = float)
    dfreq = np.zeros(256, dtype = float)
    dfSORT[0] = freq[0]
    dfreq[0] = freq[0]

    for i in range(1, 256):
        dfSORT[i] = freq[i] - freq[i-1]
        dfreq[i] = dfSORT[i]

    dfSORT.sort()
    max_thresholdD = dfSORT[0+tolerance]
    min_thresholdD = dfSORT[255-tolerance]

    mxthrPOS = np.where(dfreq == max_thresholdD)[0][0]
    mnthrPOS = np.where(dfreq == min_thresholdD)[0][0]

    finalIMG = np.zeros([image.shape[0], image.shape[1]], dtype = int)

    for i in range(finalIMG.shape[0]):
        for j in range(finalIMG.shape[1]):
            if grsclIMG[i][j] >= mnthrPOS and grsclIMG[i][j] <= mxthrPOS:
                finalIMG[i][j] = 0
            else:
                finalIMG[i][j] = 255

    return finalIMG

binIMG = Binarize('../../Pictures/Metro_SPB_Avtovo.jpg', 127)

#plt.hist(x = np.arange(256), bins = 256, weights = binIMG)
plt.imshow(binIMG)
plt.colorbar()
plt.show()
