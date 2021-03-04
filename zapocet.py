#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 19:47:22 2021

@author: Zajan Ondřej
"""

import numpy as np
from matplotlib import pyplot as plt
import time
import bwconncomp as moje
import feret 
import cv2

# převod na matici
img_orig = plt.imread("obr3.jpg")
plt.imshow(img_orig)
plt.show()

# převod na černobílý obrázek
img = moje.rgb2gray(img_orig,97)
img = np.logical_not(img).astype(np.uint8)
plt.imshow(img,cmap='Greys')
plt.show()

# zmapování obrázku, hledání objektů
t = time.time()
objclass = moje.bwconncomp(img)
elapsed1 = time.time()-t
print("Bwconncomp time= ",elapsed1)

# to samé přes balík cv2
t=time.time()
num_labels, labels_im = cv2.connectedComponents(img)
elapsed2=time.time()-t
print("Bwconncomp CV2 time= ",elapsed2)

# uložení tříd objektů s jejich souřadnicemi do seznamu
listofclasses = moje.getlistofclasses(objclass)#najdi všechny třídy
print("Třídy načteny")
conncomp = list()
for c in listofclasses:
    conncomp.append(moje.getcoordlistofoneclass(objclass,c))
print("Třídy zmapovány")

# vyberu pouze objekty větší než 5000
conncomp = [i for i in conncomp if np.size(i)>5000]

# najdu Feretovy průměry
fmax=[]
fmin=[]
for o in conncomp:
    feretMin,feretMax=feret.getFeretDiameters(o[0])
    fmax.append(feretMax)
    fmin.append(feretMin)

# vykreslím průměry
plt.plot(fmax,fmin)