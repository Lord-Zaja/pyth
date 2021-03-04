#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 19:47:22 2021

@author: Zaja
"""

import numpy as np
from matplotlib import pyplot as plt
import cv2
import time
import bwconncomp as moje
import feret 

img_orig = plt.imread("obr3.jpg")
plt.imshow(img_orig)

#převod na černobílý obrázek
img=moje.rgb2gray(img_orig,97)
img=np.logical_not(img).astype(np.uint8)
plt.imshow(img,cmap='Greys')
print("Hledání. skládání objektů")
t=time.time()
objclass=moje.bwconncomp(img)
elapsed1=time.time()-t
print(elapsed1)
print("Byly ztraceny pixely: {}".format(not(np.allclose(img,moje.binarize(objclass)))))
listofclasses=moje.getlistofclasses(objclass)#najdi všechny třídy
print("Třídy načteny")
conncomp=list()
for c in listofclasses:
    conncomp.append(moje.getcoordlistofoneclass(objclass,c))
print("Třídy zmapovány")


obj=[i for i in conncomp if np.size(i)>5000]
#souřadnice v obj[řádek,sloupec]

t=time.time()
feretMin,feretMax=feret.getFeretDiameters(obj[0])
elapsedFeret=time.time()-t
print(elapsedFeret)

fmax=[]
fmin=[]
for o in obj:
    feretMin,feretMax=feret.getFeretDiameters(obj[0])
    fmax.append(feretMax)
    fmin.append(feretMin)



colors=np.linspace(30,255,np.size(obj))
img_col=np.zeros(((np.shape(img)[0],np.shape(img)[1])),int)
#img_col=[img_col[coords[0]][coords[1]][rgb]=color for i,color in enumerate(colors) for coords in obj[i] for rgb in range(3)]
for i,color in enumerate(colors):
    for coords in obj[i]:
        img_col[coords[0]][coords[1]]=color
plt.imshow(img_col,cmap="gnuplot2")

#opencv
#image = cv2.imread("obr3.jpg",0)
#image = cv2.threshold(image, 0, 97,
#	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
t=time.time()
num_labels, labels_im = cv2.connectedComponents(img)
elapsed2=time.time()-t
print(elapsed2)
listOfClasses=moje.getListOfClasses(labels_im)
cv2conncomp=list()
for c in listOfClasses:
    cv2conncomp.append(moje.getCoordListOfOneClass(labels_im,c))
cv2obj=[i for i in cv2conncomp if np.size(i)>5000]