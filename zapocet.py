#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 17:56:41 2021

@author: Zaja
"""

import numpy as np
from matplotlib import pyplot as plt
import cv2

def rgb2gray(img,mez):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 5.1.21
    img - původní černobílý obrázek
    mez - při překročení, pixel je vyhodnocen jako černý <1,255>
    return - binární obrázek - matice
    """
    mez=mez*3
    binary_img=np.zeros(np.shape(img)[0:2])
    for row_idx,row in enumerate(img):
        for col_idx, pix in enumerate(row):
            if((int(pix[0])+int(pix[1])+int(pix[2]))>mez):
                binary_img[row_idx,col_idx]=1#jednička je zde jako černá
    return binary_img

def getCoordListOfOneClass(objClass,myc):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    myc - moje hledaná třída
    return - pole obsahující v každém prvku pole souřadnic [x,y] každého pixelu v dané třídě
    """ 
    coordListOfOneClass=list()
    for y,row in enumerate(objClass):
        for x, c in enumerate(row):
          if(c==myc):
            coordListOfOneClass=np.vstack((coordListOfOneClass,[x,y]))
    return coordListOfOneClass

def getListOfClasses(objClass):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    return - pole obsahující všechny třídy - popis objektu
    """ 
    pole=list()
    for y,row in enumerate(objClass):
        for x, c in enumerate(row):
          if(c!=0): 
              if(not(np.any(pole==c))):
                  pole.append(c)
                  #print(c)
    return pole

def findNeighbors(img,x,y):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    img - původní černobílý obrázek
    x,y - souřadnice zkoumaného pixelu
    neighbors - seznam obsahující v každé položce obě souřadnice souseda bodu x,y
    """
    neighbors=list()
    if(x!=0 and img[y][x-1]):#pixel vlevo
       neighbors.append([x-1,y])
    #if(x!=np.shape(img)[0] and img[y][x+1]):#pixel vpravo   o těchto pixelech zatím nic nevím
    #   neighbors.append([x+1,y])
    if(y!=0 and img[y-1][x]):#pixel nahoře
       neighbors.append([x,y-1])
    #if(y!=np.shape(img)[1] and img[y+1][x]):#pixel dole   o těchto pixelech zatím nic nevím
    #   neighbors.append([x,y+1])
    return neighbors
       
def isInList(S,x):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    L - seznam
    x - číselná hodnota, kterou v sezmanu hledám
    return - True/False - hodnota nalezena/nenalezena
    """
    L=np.array(S)
    if(np.size(L)==0):
        return False
    if(np.size(L)==1):
        if(L==x):
            return True
        else:
            return False
    for i in L:
       if(i==x):
           return True
    return False
       
def findNeighborClasses(neighbors,objClass):  
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    neighbors - seznam souřadnic sousedních jedniček
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    neighborClasses - množina sousedních tříd pixelů ze seznamu neighbors
    """  
    neigborClasses=list()
    if(np.shape(neighbors)[0]==0):
        return -1
    if(np.shape(neighbors)[0]==1):
        return objClass[neighbors[0][1]][neighbors[0][0]]
    neighborClasses=objClass[neighbors[0][1]][neighbors[0][0]]
    for coord in neighbors[1:]:
       if(not(isInList(neighborClasses,objClass[coord[1]][coord[0]]))):
           neighborClasses=np.vstack((neighborClasses,objClass[coord[1]][coord[0]]))
    return neighborClasses #list čísel různých tříd (min 1 max 4)

def findMinClass(neighbors,objClass):       
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    neighbors - seznam souřadnic sousedních jedniček
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    minumum - nejmenší hodnota třídy ze sousedních jedniček
    """
    return min(findNeighborClasses(neighbors,objClass))

def remapClasses(objClass,xynow,z,na):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    xynow - nynější souřadnice v matici
    z - z čeho změnit třídu
    na - na co změnit třídu
    return - matice objClass, všude místo "z" je "na"
    """ 
    #přepíše všechny dané třídy v jednom řádku
    for y,row in enumerate(objClass):
        for x, c in enumerate(row):
          if(c==z):
              c=na
          if(x==xynow[0] and y==xynow[1]):
              return objClass
    return objClass

def remapClasses2(objClass,xynow,z,na):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 13.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    xynow - nynější souřadnice v matici
    z - z čeho změnit třídu
    na - na co změnit třídu
    return - matice objClass, všude místo "z" je "na"
    """ 
    #přepíše všechny dané třídy v jednom řádku v rámci jednoho objektu
    #posunuji se doleva a postupně přepisuji, dokud nenarazím na nulu
    #ke třeba opravit: kontrolvoat, jestli nějaké prvky nemají nahoře souseda, pokud ano, poslat na souseda nahoře funkci remapClasses3
    objClass[xynow[1]][xynow[0]]=na#první prvek kde začínám ještě nemá třídu, je nula
    for x in range(xynow[0],-1,-1):
        if(objClass[xynow[1]][x]==z):
            objClass[xynow[1]][x]=na
        if(x!=0):
            if(objClass[xynow[1]][x-1]==0):
                return objClass
    return objClass

def binarize(seznam):
    matrix=np.array(seznam)
    for y,row in enumerate(matrix):
        for x,prvek in enumerate(row):
            if(prvek!=0):
                matrix[y][x]=1
    return matrix

def remapClasses3(objClass,neighbors,beginNeighbor):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 14.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček

    return - matice objClass, všude v ostrůvku místo "z" je "na"
    """
    y=neighbors[beginNeighbor][1]
    x=neighbors[beginNeighbor][0]
    #přepsání prvku, pro kterého byly zjištěny dva sousedi
    objClass[y+1][x]=objClass[neighbors[int(not(beginNeighbor))][1]][neighbors[int(not(beginNeighbor))][0]]
    
    #print("Startovní pozice= {}".format([x,y]))
    #dostaň se nejkarjnějšího levého/pravého horního rohu
    #doleva,nahoru, doprava dokud nemůžu nahoru pak nahoru
    while(True):   
        if(x>0 and objClass[y][x-1]!=0):#místo vlevo
            x-=1
        elif(y>0 and objClass[y-1][x]!=0):#místo nahoře
            y-=1
        elif(x<(np.shape(objClass)[1]-1) and objClass[y][x+1]!=0):#místo vpravo
            while(x<(np.shape(objClass)[1]-1) and objClass[y][x+1]!=0 and (y==0 or objClass[y-1][x]==0)):
                x+=1
            if(y==0 or objClass[y-1][x]==0):#nemohl jsem jít nahoru
                break
            else:#můžu jít nahoru
                y-=1
        else:#nikde místo už není
            break  
    #print("Pravý horní roh= {}".format([x,y]))
    #postupně se posunuj po pravém kraji od shora a přepisuj řádky
    #nahoru pokud nahoře je nepřepsaná třída,doprava,dolu,doleva dokud nemůžu dolu, pak dolu
    while(True): 
        if(y>neighbors[beginNeighbor][1]):#překročím startovní y => break
            break
        if(x==(np.shape(objClass)[1]-1) or objClass[y][x+1]==0):#vpravo není žádné místo => přepíšu třídy daného řádku
            remapClasses2(objClass,[x,y],objClass[neighbors[beginNeighbor][1]][neighbors[beginNeighbor][0]],objClass[neighbors[int(not(beginNeighbor))][1]][neighbors[int(not(beginNeighbor))][0]])
        if(y>0 and objClass[y-1][x]!=0 and objClass[y-1][x]!=objClass[neighbors[int(not(beginNeighbor))][1]][neighbors[int(not(beginNeighbor))][0]]):
            y-=1        
        elif(x<(np.shape(objClass)[1]-1) and objClass[y][x+1]!=0):#místo vpravo
            x+=1
        elif(y<(np.shape(objClass)[0]-1) and objClass[y+1][x]!=0):#místo dole
            y+=1
        elif(x>0 and objClass[y][x-1]!=0):#místo vlevo
            while(x>0 and objClass[y][x-1]!=0 and (y==(np.shape(objClass)[0]) or objClass[y+1][x]==0)):
                x-=1
            if(y==(np.shape(objClass)[0]) or objClass[y+1][x]==0):#nemohl jsem jít dolu
                break
            else:#můžu jít dolu
               y+=1    
        else:#nikde místo už není
            break  
    #print("Skončeno v bodě= {}".format([x,y]))
        
def bwconncomp(img):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 5.1.21
    Upraveno: 12.2.21
    img - původní černobílý obrázek
    return - seznam obsahující souřadnice objektů
    """
    #studuji řádek po řádku, případně přepisuji třídu v jednom řádku v rámci jednho objektu 
    #pokud je v objektu "ostrůvek" musím projet celý "ostrůvek" znovu
    #efektivněji: ?
    #posunovat se dokud nenarzím na objekt 
    # => projedu celý objekt
    #posunuji se od místa, kde jsem narazil na objekt, ignoruji třídy již zapsaných objektů
    i=0
    p=0
    conncomp=list()
    neighbors=list()
    nOClasses=0     #počet objektů
    pix=np.zeros(2)
    objClass=np.zeros(np.shape(img))
    for row_idx,row in enumerate(img):
        for col_idx, pix in enumerate(row):
            if(row_idx==1 and col_idx==22):
                #print("break")
                pass
            if(pix): 
                #print(nOClasses)
                neighbors=findNeighbors(img,col_idx,row_idx)
                if(np.shape(neighbors)[0]==0):#žádný soused, nový objekt
                    nOClasses+=1#nový objekt
                    objClass[row_idx,col_idx]=nOClasses
                else:
                    remapC=findNeighborClasses(neighbors,objClass)
                    #jestli jsou všichni sousedi nula, vytvoř novou třídu a zapiš do všech sousedů 
                    #to se stát nikdy nemůže, nepsat   
                    if(np.size(remapC)==1):#všichni sousedi sdílí stejnou třídu
                        if(remapC==0):
                            print("Jeden soused a je nulový!")
                            print("Bod: {}".format([col_idx,row_idx]))
                            return -1
                        objClass[row_idx][col_idx]=remapC#pak přepíšu pouze třídu u nynšjí pixel
                    else: 
                        keepC=min(remapC)#třída, kterou chci všude zapsat
                        if(keepC==0):
                            print("Dva sousedi a nejmenší je nulový!")
                            print("Bod: {}".format([col_idx,row_idx]))
                            print("výpis všech tříd: {}".format(remapC))
                            return -1
                        #vyjímka nastane, pokud uvnitř objektu exituje ostrůvek=>remapClasses3 pro ostrůvek pouze
                        if(keepC==objClass[neighbors[0][1]][neighbors[0][0]]):#menší je u prvního souseda
                            if(neighbors[0][1]>neighbors[1][1]):#menší třída je dole
                                #print([col_idx,row_idx])
                                remapClasses3(objClass,neighbors,1)
                                i+=1
                                #print("Island remaped")
                            else:
                                remapC=np.setdiff1d(remapC,min(remapC))#třídy, které přepíšu
                                remapClasses2(objClass,[col_idx,row_idx],remapC,keepC)
                                p+=1
                        else:#menší je u druhého souseda
                            if(neighbors[0][1]<neighbors[1][1]):#menší třída je dole
                                remapClasses3(objClass,neighbors,0)
                                i+=1
                            else:
                                remapC=np.setdiff1d(remapC,min(remapC))#třídy, které přepíšu
                                remapClasses2(objClass,[col_idx,row_idx],remapC,keepC)
                                p+=1
                        nOClasses-=1
                                           
                        #keepC=findMinClass(neighbors,objClass)#tuhle funkci tady nepotřebuji
                        #for c in remapC:
                        #    remapClasses2(objClass,[col_idx,row_idx],c,keepC)
    print("hotovo")
    print("p= {}".format(p))
    print("i= {}".format(i))
    print("Byly ztraceny pixely: {}".format(not(np.allclose(img,binarize(objClass)))))
    listOfClasses=getListOfClasses(objClass)#najdi všechny třídy
    for c in listOfClasses:
        conncomp=np.vstack((conncomp,getCoordListOfOneClass(objClass,c)))
    return conncomp

img_orig = plt.imread("obr3.jpg")
#print(len(img))
#print(np.shape(img))
#plt.imshow(img)

#převod na černobílý obrázek
print("Převod na černobílý obrázek")
img=rgb2gray(img_orig,97)
print("Velikost obráztku= {}".format(np.shape(img)))
img=np.logical_not(img).astype(int)
plt.imshow(img,cmap='Greys')
print("Hledání. skládání objektů")
conncomp=bwconncomp(img)
ret, labels = cv2.connectedComponents(img)





















