#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 17:56:41 2021

@author: Zaja
"""

import numpy as np
#from ipyparallel import Client
#cli=Client()
#cli.ids

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
            if (int(pix[0])+int(pix[1])+int(pix[2])) > mez:
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
    #coordListOfOneClass=np.empty((0,2),int)
    res=np.where(objClass==myc)
    return list(map(list,zip(res[0],res[1])))
    # for y,row in enumerate(objClass):
    #     for x, c in enumerate(row):
    #       if(c==myc):
    #         coordListOfOneClass=np.vstack((coordListOfOneClass,[x,y]))
    # return coordListOfOneClass

def getListOfClasses(objClass):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 12.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    return - pole obsahující všechny třídy - popis objektu
    """ 
    pole=np.empty((0,1),int)
    objClass=np.array(objClass)
    for row in objClass:
        for c in row:
          if(c!=0): 
              if(not(np.any(pole==c))):
                  pole=np.vstack((pole,c))
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

def findAllNeighbors(img,x,y):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 16.2.21
    img - původní černobílý obrázek
    x,y - souřadnice zkoumaného pixelu, x: sloupec, y: řádek
    neighbors - seznam obsahující v každé položce obě souřadnice souseda bodu x,y
    """
    neighbors=list()
    if(x!=0 and img[y][x-1]):#pixel vlevo
       neighbors.append([x-1,y])
    if(x!=np.shape(img)[1] and img[y][x+1]):#pixel vpravo
       neighbors.append([x+1,y])
    if(y!=0 and img[y-1][x]):#pixel nahoře
       neighbors.append([x,y-1])
    if(y!=np.shape(img)[0] and img[y+1][x]):#pixel dole
       neighbors.append([x,y+1])
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
    neighborClasses=list()
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

def remapClasses2(img,objClass,xynow,na):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 13.2.21
    Upraveno: 19.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    xynow - nynější souřadnice v matici
    z - z čeho změnit třídu
    na - na co změnit třídu
    return - matice objClass, všude místo "z" je "na"
    """ 
    #přepíše všechny dané třídy v jednom řádku v rámci jednoho objektu
    #posunuji se doleva a postupně přepisuji, dokud nenarazím na nulu
    #ke třeba opravit: kontrolvoat, jestli nějaké prvky nemají nahoře souseda, pokud ano, poslat na souseda nahoře funkci remapClasses3
    dole1=-1
    dole2=-1
    y=xynow[1]
    objClass[y][xynow[0]]=na#první prvek kde začínám ještě nemá třídu, je nula
    if(y!=(np.shape(objClass)[0]-1) and (img[y+1][xynow[0]]==0 or objClass[y+1][xynow[0]]==na)):#dole je hrana
        dole1=xynow[0]
    for x in range(xynow[0]-1,-1,-1):
        if(img[xynow[1]][x]==0):#vyjel jsem z objektu => konec
            break
        objClass[xynow[1]][x]=na
        if(xynow[1]>0 and img[xynow[1]-1][x]!=0 and objClass[xynow[1]-1][x]!=na):#nahoře je nepřepsaný soused
            remapClasses3(img,objClass,[[x,xynow[1]],[x,xynow[1]-1]],1)   
        if(y!=(np.shape(objClass)[0]-1) and (img[y+1][x]==0 or objClass[y+1][x]==na or objClass[y+1][x]==0)):#dole je hrana
            if(dole1==-1):
                dole1=x
            # elif(dole2!=-1):#našel jsem dole blok, který je třeba přepsat -- hrana -- nic -- hrana
            #     edges2=np.zeros(4)
            #     lastEdge=1#začínám s hranou vpravo
            #     y2=y+1
            #     x2=dole2
            #     while(True): 
            #         if(y2<y):#překročím startovní y => break
            #             break
            #         edges2=findEdges(img,objClass,x2,y2,na)
            #         if(np.sum(edges2)==4 and objClass[y2][x2]==na):#vše přepsáno
            #             break
            #         if(edges2[1]):#vpravo není žádné místo => přepíšu třídy daného řádku
            #             remapClasses2(img,objClass,[x2,y2],na)
            #         lastEdge,x2,y2=followTheEdge(edges2,lastEdge,x2,y2)
            #     dole2=-1
        elif(dole1!=-1):#místo, kde končí hrana
            dole2=x
        #elif(dole2!=-1):#našel jsem dole blok, který je třeba přepsat
            edges2=np.zeros(4)
            lastEdge=1#začínám s hranou vpravo
            y2=y+1
            x2=dole2
            while(True): 
                if(y2<y):#překročím startovní y => break
                    break
                edges2=findEdges(img,objClass,x2,y2,na)
                if(np.sum(edges2)==4 and objClass[y2][x2]==na):#vše přepsáno
                    break
                if(edges2[1]):#vpravo není žádné místo => přepíšu třídy daného řádku
                    remapClasses2(img,objClass,[x2,y2],na)
                lastEdge,x2,y2=followTheEdge(edges2,lastEdge,x2,y2)
            dole2=-1
            dole1=-1
            
        #if(objClass[xynow[1]][x]==z):
        #    objClass[xynow[1]][x]=na
        #if(x!=0):
        #    if(objClass[xynow[1]][x-1]==0):
        #        return objClass
    return objClass

def binarize(seznam):
    matrix=np.zeros(np.shape(seznam)[:2]).astype(np.uint8)
    for y,row in enumerate(seznam):
        for x,prvek in enumerate(row):
            if((prvek!=0).any()):
                matrix[y][x]=1
    return matrix

def findEdges(img,objClass,x,y,na):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 19.2.21
    Upraveno: 
    """
    #[nahoře,vpravo,dole,vlevo]
    edges=np.zeros(4)
    if(y==0 or img[y-1][x]==0 or objClass[y-1][x]==na or objClass[y-1][x]==0):#up
        edges[0]=1
    if(x==np.shape(objClass)[1] or img[y][x+1]==0 or objClass[y][x+1]==na or objClass[y][x+1]==0):#right
        edges[1]=1
    if(y==np.shape(objClass)[0] or img[y+1][x]==0 or objClass[y+1][x]==na or objClass[y+1][x]==0):#down
        edges[2]=1
    if(x==0 or img[y][x-1]==0 or objClass[y][x-1]==na or objClass[y][x-1]==0):#left
        edges[3]=1
    return edges

def followTheEdge(edges,lastEdge,x,y):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 19.2.21
    Upraveno: 
    #sleduje hrany po směru hodinových ručiček
    """
    if(np.sum(edges)==0):#žádná hrana (roh)
        if(lastEdge==0):#poslední hrana nahoře => jdi nahoru, strana vlevo
            y-=1
            lastEdge=3
        elif(lastEdge==1):#poslední hrana vpravo => jdi doprava, strana nahoře
            x+=1
            lastEdge=0
        elif(lastEdge==2):#poslední hrana dole => jdi dolu, strana vpravo
            y+=1
            lastEdge=1
        elif(lastEdge==3):#poslední hrana vlevo => jdi vlevo, strana dole
            x-=1
            lastEdge=2                
    elif(np.sum(edges)==1):#jedna hrana
        if(edges[lastEdge]): 
            if(edges[0]):#hrana nahoře => jdi doprava
                x+=1
                lastEdge=0
            elif(edges[1]):#hrana vpravo => jdi dolu
                y+=1
                lastEdge=1
            elif(edges[2]):#harna dole => jdi doleva
                x-=1
                lastEdge=2
            elif(edges[3]):#hrana vlevo => jdi nahoru
                y-=1
                lastEdge=3
        else:#jako pokud není žádná hrana
            if(lastEdge==0):#poslední hrana nahoře => jdi nahoru, strana vlevo
                y-=1
                lastEdge=3
            elif(lastEdge==1):#poslední hrana vpravo => jdi doprava, strana nahoře
                x+=1
                lastEdge=0
            elif(lastEdge==2):#poslední hrana dole => jdi dolu, strana vpravo
                y+=1
                lastEdge=1
            elif(lastEdge==3):#poslední hrana vlevo => jdi vlevo, strana dole
                x-=1
                lastEdge=2  
    elif((np.sum(edges)==2) and ((edges[0] and edges[2]) or (edges[1] and edges[3]))):#dvě hrany naproti sobě
        if(edges[lastEdge]):
            if(lastEdge==0 and edges[0]):#pokračuji po hraně nahoře vpravo
                x+=1
            elif(lastEdge==1 and edges[1]):#pokarčuji po pravé hraně dolu
                y+=1
            elif(lastEdge==2 and edges[2]):#pokračuj po dolní hraně doleva
                x-=1
            elif(lastEdge==3 and edges[3]):#pokračuj po levé hraně nahoru
                y-=1
        else:
            if(lastEdge==0):#poslední hrana nahoře => jdi nahoru, strana vlevo
                y-=1
                lastEdge=3
            elif(lastEdge==1):#poslední hrana vpravo => jdi doprava, strana nahoře
                x+=1
                lastEdge=0
            elif(lastEdge==2):#poslední hrana dole => jdi dolu, strana vpravo
                y+=1
                lastEdge=1
            elif(lastEdge==3):#poslední hrana vlevo => jdi vlevo, strana dole
                x-=1
                lastEdge=2      
    elif(np.sum(edges)==2):#dvě hrany a nejsou naproti sobě - roh
        if(edges[lastEdge]):#jdu po existující hraně
            if(edges[0] and edges[1]):#pravý horní roh => šel jsem vpravo, půjdu dolu
                y+=1
                lastEdge=1
            elif(edges[1] and edges[2]):#pravý dolní roh => šel jsem dolu, půjdu doleva
                x-=1
                lastEdge=2
            elif(edges[2] and edges[3]):#levý dolní roh => šel jsem vlevo, půjdu nahoru
                y-=1
                lastEdge=3
            elif(edges[3] and edges[0]):#levý horní roh => šel jsem nahoru, půjdu doprava
                x+=1
                lastEdge=0
        else:#hrana zmizela => jako pokud není hrana žádná
            if(lastEdge==0):#poslední hrana nahoře => jdi nahoru, strana vlevo
                y-=1
                lastEdge=3
            elif(lastEdge==1):#poslední hrana vpravo => jdi doprava, strana nahoře
                x+=1
                lastEdge=0
            elif(lastEdge==2):#poslední hrana dole => jdi dolu, strana vpravo
                y+=1
                lastEdge=1
            elif(lastEdge==3):#poslední hrana vlevo => jdi vlevo, strana dole
                x-=1
                lastEdge=2  
    elif(np.sum(edges)==3):#slepá ulička
        if(not(edges[0])):#cesta nahoru => zabloudil jsem zezhora => hrana vlevo a jdu nahoru
            y-=1
            lastEdge=3
        elif(not(edges[1])):#cesta doparva => zabloudil jsem zprava => hrana nahoře a jdi doprava
            x+=1
            lastEdge=0
        elif(not(edges[2])):#cesta dolu => zabloudil jsem zezdola => hrana vparvo a jdi dolu
            y+=1
            lastEdge=1
        elif(not(edges[3])):#cesta doleva => zabloudil jsem zleva => hrana dole a jdi doleva
            x-=1
            lastEdge=2
    elif(np.sum(edges)>3):
        return -1,-1,-1
    return lastEdge,x,y

def remapClasses3(img,objClass,neighbors,beginNeighbor):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 14.2.21
    Upraveno: 19.2.21
    objClass - matice popisující objekty pomocí očíslování bloků jedniček
    neighbors - sousedi původního prvku
    beginNeighbor - číslo souseda (1/0) u kterého začínám, číslo souseda nahoře od aktuálního prvku
    return - matice objClass, všude v ostrůvku místo "z" je "na"
    """
    y=neighbors[beginNeighbor][1]#souřadnice začínajícího horního souseda
    x=neighbors[beginNeighbor][0]
    na=objClass[neighbors[int(not(beginNeighbor))][1]][neighbors[int(not(beginNeighbor))][0]]#na co chci třídy přepsat
    #přepsání prvku, pro kterého byly zjištěny dva sousedi
    objClass[y+1][x]=na
    edges=np.zeros(4)
    #print("Startovní pozice= {}".format([x,y]))
    #dostaň se nejkarjnějšího levého/pravého horního rohu
    #doleva,nahoru, doprava dokud nemůžu nahoru pak nahoru
    while(True):   
        edges=findEdges(img,objClass,x,y,na)
        if(not(edges[3])):#místo vlevo => jdi doleva
            x-=1
            edges=findEdges(img,objClass,x,y,na)
            if(not(edges[2])):#pokud je dole místo, musím sledovat pravou hranu a všechno zde přepsat 
                lastEdge=1
                x2=x
                y2=y+1
                while(True): 
                    if(y2<y):#překročím startovní y => break
                        break
                    edges2=findEdges(img,objClass,x2,y2,na)
                    if(np.sum(edges2)==4 and objClass[y2][x2]==na):#vše přepsáno
                        break
                    if(edges2[1]):#vpravo není žádné místo => přepíšu třídy daného řádku
                        remapClasses2(img,objClass,[x2,y2],na)
                    lastEdge,x2,y2=followTheEdge(edges2,lastEdge,x2,y2)
        elif(not(edges[0])):#místo nahoře
            y-=1
        elif(not(edges[1])):#místo vpravo
            while(x<(np.shape(objClass)[1]-1) and objClass[y][x+1]!=0 and objClass[y][x+1]!=na and (y==0 or objClass[y-1][x]==0)):
                x+=1
            if(y==0 or objClass[y-1][x]==0 or objClass[y-1][x]==na):#nemohl jsem jít nahoru
                break
            else:#můžu jít nahoru
                y-=1
        else:#nikde místo už není
            break  
    #print("Pravý horní roh= {}".format([x,y]))
    #postupně se posunuj po pravém kraji od shora a přepisuj řádky
    #nahoru pokud nahoře je nepřepsaná třída,
    #doprava,
    #dolu,
    #doleva dokud nemůžu dolu, pak nahoru, 
    edges=np.zeros(4)
    lastEdge=0#začínám s hranou nahoře vždy
    while(True): 
        if(y>neighbors[beginNeighbor][1]):#překročím startovní y => break
            break
        edges=findEdges(img,objClass,x,y,na)
        if(edges[1] and lastEdge!=3):#vpravo není žádné místo a nejdu nahoru=> přepíšu třídy daného řádku
            remapClasses2(img,objClass,[x,y],na) 
        if(np.sum(edges)==4):#žádná cesta => break
            break
        lastEdge,x,y=followTheEdge(edges,lastEdge,x,y) 
    #print("Skončeno v bodě= {}".format([x,y]))

def remapClasses4(img,objClass,xybegin,na):
    #rekurze nefunguje
    #najdi všechny sousedy
    #na všechny co se mají přepsat pošli remapClasses4
    objClass[xybegin[1]][xybegin[0]]=na
    neighbors=findAllNeighbors(img, xybegin[1], xybegin[0])
    for idx,n in enumerate(neighbors):
        if(objClass[n[1]][n[0]]!=na):
            remapClasses4(img,objClass,n,na)
                              
def bwconncomp(img):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 5.1.21
    Upraveno: 14.2.21
    img - původní černobílý obrázek
    return - seznam obsahující souřadnice objektů
    """
    #studuji řádek po řádku, případně přepisuji třídu v jednom řádku v rámci jednho objektu 
    #pokud je v objektu "ostrůvek" musím projet celý "ostrůvek" znovu
    #efektivněji: ?
    #posunovat se dokud nenarzím na objekt 
    # => projedu celý objekt
    #posunuji se od místa, kde jsem narazil na objekt, ignoruji třídy již zapsaných objektů
    neighbors=list()
    nOClasses=0     #počet objektů
    pix=np.zeros(2)
    objClass=np.zeros(np.shape(img))
    for row_idx,row in enumerate(img):
        for col_idx, pix in enumerate(row):
            if(pix): 
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
                                remapClasses3(img,objClass,neighbors,1)
                                #print("Island remaped")
                            else:
                                remapC=np.setdiff1d(remapC,min(remapC))#třídy, které přepíšu
                                remapClasses2(img,objClass,[col_idx,row_idx],keepC)#menší třída je nahoře
                        else:#menší je u druhého souseda
                            if(neighbors[0][1]<neighbors[1][1]):#menší třída je dole
                                remapClasses3(img,objClass,neighbors,0)
                            else:
                                remapC=np.setdiff1d(remapC,min(remapC))#třídy, které přepíšu
                                remapClasses2(img,objClass,[col_idx,row_idx],keepC)
                        nOClasses-=1
                                           
                        #keepC=findMinClass(neighbors,objClass)#tuhle funkci tady nepotřebuji
                        #for c in remapC:
                        #    remapClasses2(objClass,[col_idx,row_idx],c,keepC)
    return objClass


        
#plt.imshow(image,cmap="Greys")
#image=rgb2gray(image,97)



















