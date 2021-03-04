#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 21:21:09 2021

@author: Zaja
"""

    while(True):   
        if(x>0 and objClass[y][x-1]!=0 and objClass[y][x-1]!=na):#místo vlevo
            x-=1
        elif(y>0 and objClass[y-1][x]!=0 and objClass[y-1][x]!=na):#místo nahoře
            y-=1
        elif(x<(np.shape(objClass)[1]-1) and objClass[y][x+1]!=0 and objClass[y][x+1]!=na):#místo vpravo
            while(x<(np.shape(objClass)[1]-1) and objClass[y][x+1]!=0 and objClass[y][x+1]!=na and (y==0 or objClass[y-1][x]==0)):
                x+=1
            if(y==0 or objClass[y-1][x]==0 or objClass[y-1][x]==na):#nemohl jsem jít nahoru
                break
            else:#můžu jít nahoru
                y-=1
        else:#nikde místo už není
            break  
        
        
def adjustBox(obj,boundingBox,primky):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 27.2.21
    Změněno: 28.2.21
    Funkce: Přizpůsobí hraniční box danému objektu, upraví boundingBox a primky
    Potřebné funkce: liesIn(), movePoinAlong(), getLines()
    Parametry
    ----------
    obk : všechny souřadnice [y,x] jednoho objektu v listu
    boundingBox: list se 4 body, [[x1,y1],[x2,y2], ..]
    primky : list, s koeficienty přímek p=a*x+b, [[a1,b1],[a2,b2], ..]
    """
    for i in range(0,3):
        if(liesIn(obj,boundingBox[i],boundingBox[(i+1)%4],primky[i])):#přímka leží v objektu
            while(liesIn(obj,boundingBox[i],boundingBox[(i+1)%4],primky[i])):#dokud přímka leží v objektu, posunuji body A,B
                #bod A posunuji po přímce p_4 směrem od bodu D
                #bod B posunuji po přímce p_2 směrem od bodu C
                
                #bod B posunuji po přímce p_1 směrem od bodu A
                #bod C posunuji po přímce p_3 směrem od bodu D
                
                #bod C posunuji po přímce p_2 směrem od bodu B
                #bod D posunuji po přímce p_4 směrem od bodu A
                
                #bod D posunuji po přímce p_3 směrem od bodu C
                #bod A posunuji po přímce p_1 směrem od bodu B
                print(vecSize(boundingBox[(i+1)%4]-boundingBox[i]))
                print(boundingBox)
                print("\n")
                boundingBox[i]=movePointAlong(primky[(i+3)%4],boundingBox[i],1,boundingBox[(i+3)%4])#není mutable?? jakto sakra
                boundingBox[(i+1)%4]=movePointAlong(primky[(i+1)%4],boundingBox[(i+1)%4],1,boundingBox[(((i+1)%4)+1)%4])
                primky=getLines(boundingBox)
            #posunuse o jeden pixel zpět, přímka leží na hraně objektu
            boundingBox[i]=movePointAlong(primky[(i+3)%4],boundingBox[i],-1,boundingBox[(i+3)%4])
            boundingBox[(i+1)%4]=movePointAlong(primky[(i+1)%4],boundingBox[(i+1)%4],-1,boundingBox[(((i+1)%4)+1)%4])
            primky=getLines(boundingBox)     
        else:#přímka neleží v objektu
            while(not(liesIn(obj,boundingBox[i],boundingBox[(i+1)%4],primky[i]))):#dokud přímka neleží v objektu, posunuji body A,B
                #bod A posunuji po přímce p_4 směrem k bodu D
                #bod B posunuji po přímce p_2 směrem k bodu C
                print("zmenšuji {}".format(i))
                print(primky[i])
                print(vecSize(boundingBox[(i+1)%4]-boundingBox[i]))
                print(boundingBox)
                printBox(boundingBox)
                print("\n")
                boundingBox[i]=movePointAlong(primky[(i+3)%4],boundingBox[i],-1,boundingBox[(i+3)%4])
                boundingBox[(i+1)%4]=movePointAlong(primky[(i+1)%4],boundingBox[(i+1)%4],-1,boundingBox[(((i+1)%4)+1)%4])
                primky=getLines(boundingBox)
            #posunuse o jeden pixel zpět, přímka leží na hraně objektu
            boundingBox[i]=movePointAlong(primky[(i+3)%4],boundingBox[i],1,boundingBox[(i+3)%4])
            boundingBox[(i+1)%4]=movePointAlong(primky[(i+1)%4],boundingBox[(i+1)%4],1,boundingBox[(((i+1)%4)+1)%4])
            primky=getLines(boundingBox)      