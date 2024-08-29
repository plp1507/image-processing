import numpy as np
import cv2 as cv
from matplotlib import image as im
from matplotlib import pyplot as plt

image = cv.imread("./images/bug.png")
#acessa a imagem e transforma em matriz 

comp = image.shape[0]
alt = image.shape[1]

ordem = np.zeros([comp, alt], dtype = int)                  
#cria a matriz que guarda os tons de cinza

for i in range(0, len(ordem)-1):
    for j in range(0, len(ordem[0])-1):
        sup = (image[i][j][0])/3 + (image[i][j][1])/3 + (image[i][j][2])/3
        ordem[i][j] = int(sup)
#calcula o tom de cinza do pixel


freq = np.zeros(256, dtype = int)

for i in range(0, len(ordem)-1):
    for j in range(0, len(ordem[0])-1):
        freq[ordem[i][j]] += 1
#contabiliza a frequência de cada tom


freq2 = np.zeros(len(freq), dtype = int)

for i in range(1, len(freq)-2):
    if i == 1:
        freq2[i] = freq[i]
    else:
        freq2[i] = int((freq[i]+freq[i+1])/2) - int((freq[i-1]+freq[i-2])/2)  
#calcula a derivada da distribuição de frequências


freq3 = np.zeros(len(freq2), dtype = int)

for i in range(0, len(freq2)-1):
    freq3[i] = freq2[i]                                                      
#cria uma matriz igual à da imagem


freq2.sort()               
#ordena as frequências em ordem crescente


mxthrD = freq2[0]
#ajusta o limite máximo do "filtro" como a menor derivada (maior derivada negativa)


mnthrD = freq2[-1]
#ajusta o limite mínimo do "filtro" como a maior derivada (maior derivada positiva)


mxthr = 0
mnthr = 0

for i in range(0, len(freq3)-1):
    if freq3[i] == mxthrD:
        mxthr = i
    if freq3[i] == mnthrD:
        mnthr = i
#procura na matriz de frequências onde essas derivadas estão e guarda os índices de onde ocorrem


nim = np.zeros([len(ordem), len(ordem[0])], dtype = int)

for i in range(0, len(ordem)-1):
    for j in range(0, len(ordem[0])-1):
        if freq[ordem[i][j]] <= freq[mxthr]:
            if freq[ordem[i][j]] >= freq[mnthr]:
                nim[i][j] = 0
        else:
            nim[i][j] = 255
#binariza a imagem com os limites do filtro



#plt.hist(x = x, bins = 256, weights = freq2)               #monta o histograma
plt.imshow(nim)                                           #mostra a nova imagem 
plt.colorbar()                                            #relação das cores no histograma
plt.show()

