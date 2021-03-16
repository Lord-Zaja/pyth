#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:08:34 2021

@author: Zaja
"""

import numpy as np
import math
# import hickle as hkl
from matplotlib import pyplot as plt
import cv2
import bwconncomp as moje


# hkl.dump(obj, "obj.dat")

# obj=hkl.load("obj.dat")

def getLines(boundingBox):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 27.2.21
    Změněno: 27.2.21
    Funkce: Spočítá 4 rovnice přímek mezi body uvnitř boundingBox
    Potřebné moduly: numpy as np
    Parametry
    ----------
    boundingBox : list se 4 body, [[x1,y1],[x2,y2], ..]

    Return
    -------
    list : list, s koeficienty přímek p=a*x+b, [[a1,b1],[a2,b2], ..]
    """
    # počítání přímek
    # p=a*x+b
    # p_i=[a,b]
    # return seznam seznamů [[a1,b1],[a2,b2],..]
    # return speciální případ ["y",A[1]] .. stejný sloupec
    # A-p1-B
    primky = np.empty((0, 2), int)
    for i in range(0, 4):  # čtyři přímky
        A = boundingBox[i]
        B = boundingBox[(i+1) % 4]
        if(A[1] == B[1]):  # body leží ve stejném soupci
            primky = np.vstack((primky, ["y", A[1]]))
            # primky.append(list(map(list,zip("y",A[1]))))
        else:
            a = (A[0]-B[0])/(A[1]-B[1])
            primky = np.vstack((primky, [a, A[0]-a*A[1]]))
            # primky.append(list(map(list,zip(a,A[0]-a*A[1]))))
    return primky


def liesIn(obj, A, B, primka):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 27.2.21
    Změněno: 27.2.21
    Funkce: Leží přímka uvnitř objektu obj?
    Potřebné moduly: numpy as np
    Parametry
    ----------
    obj : všechny souřadnice [y,x] jednoho objektu v listu
    A : startovná bod [y,x] přímky
    B : koncový bod [y,x] přímky
    primka : koeficienty přímky p=a*x+b, [a,b]

    Return
    -------
    bool : pravda/nepravda
    """
    if(primka[0] == "y"):
        if(A[0] <= B[0]):
            od = A[0]
            do = B[0]
        else:
            od = B[0]
            do = A[0]
        for y in range(od, do+1):
            coord = np.array([y, int(float(primka[1]))])
            if(not(np.size(obj[np.all((obj-coord) == 0, axis=1)]) == 0)):
                return True
    else:
        if(A[1] <= B[1]):
            od = A[1]
            do = B[1]
        else:
            od = B[1]
            do = A[1]
        for x in range(od, do+1):
            coord = np.array([int(float(primka[0])*x+float(primka[1])), x])
            # prvek coord leží uvnitř objektu
            if(not(np.size(obj[np.all((obj-coord) == 0, axis=1)]) == 0)):
                return True
    return False


def movePointAlong(primka, bod, smer, spolecnyBod):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 27.2.21
    Změněno: 27.2.21
    Funkce: Posuň bod po prímce primka od bodu smer_od_bodu
    Parametry
    ----------
    primka : koeficienty přímky p=a*x+b, [a,b]
    bod : bod [y,x], který chci posunout
    smer : 1/-1, 1: směr ven, -1: směr dovnitř
    spolecnyBod : bod [y,x] ležící na přímce primka

    Return
    -------
    list : [y,x] souřadnice posunutého bodu
    """
    if(bod[1] == spolecnyBod[1]):  # oba body ve stejném sloupci
        if(bod[0] > spolecnyBod[0]):
            s = 1
        else:
            s = -1
        s = s*smer
        bod = [bod[0]+s, bod[1]]
    elif(bod[0] == spolecnyBod[0]):  # oba ve stejném řádku
        if(bod[1] > spolecnyBod[1]):
            s = 1
        else:
            s = -1
        s = s*smer
        bod = [bod[0], bod[1]+s]
    else:
        delta_x = 1.0/float(primka[0])
        if(bod[1] > spolecnyBod[1]):  # kladný směr
            s = 1*delta_x
        else:
            s = -1*delta_x
        s = s*smer
        x = bod[1]+s
        bod = [int(float(primka[0])*x+float(primka[1])), x]
    return bod


def teziste(obj):
    x = 0
    y = 0
    for coord in obj:
        x += coord[1]
        y += coord[0]
    return [y/np.shape(obj)[0], x/np.shape(obj)[0]]


def rotuj(body, osa, uhel):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 27.2.21
    Změněno: 27.2.21
    Funkce: Rotuje body uvnitř adjustBox podle matice rotace R
    Parametry
    ----------
    boundingBox : list se 4 body, [[x1,y1],[x2,y2], ..]
    R : matice rotace 2x2
    """
    R = np.array([[np.cos(uhel), -np.sin(uhel)], [np.sin(uhel), np.cos(uhel)]])
    for i in range(0, 4):
        body[i] = np.dot(R, (body[i]-osa).T)+osa


def vecSize(vec):
    return math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])


def getFirstEdgePoint(obj, binaryObjMatrix):
    for coord in obj:
        neighbors = moje.findallneighbors(binaryObjMatrix, coord[1], coord[0])
        # jeden nebo více pixelů jsou černé, pak sousedím s hranou
        if(np.shape(neighbors)[0] != 4):
            return [coord[0], coord[1]]


def getObjEdges(obj):
    binary = binarize3dto2d(obj2Matrix(obj))
    mapa = np.zeros(np.shape(binary), bool)
    mapaCoords = np.empty((0, 2), int)
    [startY, startX] = getFirstEdgePoint(obj, binary)
    x = startX
    y = startY
    edges = moje.findedges(binary, binary, x, y, 0)
    if(edges[0]):
        lastEdge = 0
    elif(edges[1]):
        lastEdge = 1
    elif(edges[2]):
        lastEdge = 2
    elif(edges[3]):
        lastEdge = 3
    mapa[y][x] = 1
    mapaCoords = np.vstack((mapaCoords, [y, x]))
    lastEdge, x, y = moje.followtheedge(edges, lastEdge, x, y)
    while(not(x == startX and y == startY)):
        mapa[y][x] = 1
        mapaCoords = np.vstack((mapaCoords, [y, x]))
        edges = moje.findedges(binary, binary, x, y, 0)
        lastEdge, x, y = moje.followtheedge(edges, lastEdge, x, y)
    return mapa, mapaCoords


def getPointLineVec(bod, primka):
    """
    Autor: Zajan Ondřej
    Vytvořeno: 28.2.21
    Změněno: 28.2.21
    Funkce: V
    Parametry
    ----------
    bod : [y,x]
    primka :

    Return
    -------
    list : [y,x] bod na přímce primka
    """
    if(primka[0] == "y"):
        return [bod[0], int(float(primka[1]))]
    elif(abs(float(primka[0])) < 0.0001):
        return [int(float(primka[1])), bod[1]]
    else:
        a = float(primka[0])
        b = float(primka[1])
        c = bod[1]+a*bod[0]
        y = (c+b/a)/(a+1/a)
        x = c-a*y
        return [int(y), int(x)]


def getPointOfMaxDistancePointsLine(points, primka):
    maxDistance = 0
    maxPoint = np.empty((0, 2), int)
    for coord in points:
        currentDistance = vecSize(coord-getPointLineVec(coord, primka))
        if(currentDistance > maxDistance):
            maxDistance = currentDistance
            maxPoint = coord
    return maxPoint


def getPointOfMinDistancePointsLine(points, primka):
    minDistance = math.inf
    minPoint = np.empty((0, 2), int)
    for coord in points:
        currentDistance = vecSize(coord-getPointLineVec(coord, primka))
        if(currentDistance < minDistance):
            minDistance = currentDistance
            minPoint = coord
    return minPoint


def getAdjustVector(edge_points, hlavniPrimka, A, B, vedlejsiPrimka, C, smer):
    points = np.empty((0, 2), int)
    AC = vecSize(A-C)  # vzdálenost třetího bodu C od přímky
    if(smer == 1):
        for coord in edge_points:
            lineCX = vecSize(coord-getPointLineVec(coord, vedlejsiPrimka))
            lineAX = vecSize(coord-getPointLineVec(coord, hlavniPrimka))
            if(lineCX > AC and lineAX < lineCX):
                # bod leží za hlavní přímkou směrem od objektu
                points = np.vstack((points, coord))
        maxPoint = getPointOfMaxDistancePointsLine(points, hlavniPrimka)
        if(np.size(maxPoint) == 0):
            return [0, 0]
        else:
            return (maxPoint-getPointLineVec(maxPoint, hlavniPrimka))
    else:
        for coord in edge_points:
            lineCX = vecSize(coord-getPointLineVec(coord, vedlejsiPrimka))
            lineAX = vecSize(coord-getPointLineVec(coord, hlavniPrimka))
            # bod leží za hlavní přímkou směrem k objektu (uvnitř boundingboxu)
            if(lineAX < AC and lineCX < AC):
                points = np.vstack((points, coord))
        minPoint = getPointOfMinDistancePointsLine(points, hlavniPrimka)
        if(np.size(minPoint) == 0):
            return [0, 0]
        else:
            return (minPoint-getPointLineVec(minPoint, hlavniPrimka))


def adjustBox(obj, edge_points, boundingBox, primky):
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
    for i in range(0, 4):
        # přímka leží v objektu
        if(liesIn(obj, boundingBox[i], boundingBox[(i+1) % 4], primky[i])):
            fixVec = getAdjustVector(edge_points, primky[i], boundingBox[i],
                                     boundingBox[(i+1) % 4], primky[(i+2) % 4],
                                     boundingBox[(i+3) % 4], 1)
            boundingBox[i] += fixVec
            boundingBox[(i+1) % 4] += fixVec
            if(np.shape(fixVec)[0] != 0):
                primky = getLines(boundingBox)
        else:  # přímka neleží v objektu
            fixVec = getAdjustVector(edge_points, primky[i], boundingBox[i],
                                     boundingBox[(i+1) % 4], primky[(i+2) % 4],
                                     boundingBox[(i+3) % 4], -1)
            boundingBox[i] += fixVec
            boundingBox[(i+1) % 4] += fixVec
            if(np.shape(fixVec)[0] != 0):
                primky = getLines(boundingBox)


def binarize3dto2d(seznam):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 19.2.21

    Funkce: Projde každý prvek matice seznam a pokud najde nenulový prvek,
            přepíše ho na jedničku.

    Potřebné moduly: numpy as np

    Parametry
    =========

    seznam - matice, kterou chci upravit

    return - upravená kopie matice seznam
    """
    if np.size(np.shape(seznam)) != 3:
        raise Exception("Matice seznam má špatný rozměr")
    matrix = np.zeros(np.shape(seznam)[:2]).astype(np.uint8)
    # uint8 aby matice fungovala s cv2
    for _y, row in enumerate(seznam):
        for _x, prvek in enumerate(row):
            if (prvek != 0).any():
                matrix[_y][_x] = 1
    return matrix


def obj2Matrix(obj):
    matrix = np.zeros((obj[np.argmax(obj, axis=0)[0]][0]+100,
                       obj[np.argmax(obj, axis=0)[1]][1]+100,
                       3)).astype(np.uint8)
    for coord in obj:
        matrix[coord[0]][coord[1]] = [0, 0, 255]
    return matrix


def printLineInMatrix(obj, matrix, primka):
    for x in range(obj[np.argmin(obj, axis=0)[1]][1],
                   obj[np.argmin(obj, axis=0)[1]][1]):
        coord = movePointAlong(primka, [1, 1], 1,)
        matrix[coord[0]][coord[1]] = 1
    return matrix


def printBox(obj, boundingBox):
    matrix = obj2Matrix(obj)
    for i in range(0, 4):
        cv2.line(matrix, (boundingBox[i][1], boundingBox[i][0]), (boundingBox[(
            i+1) % 4][1], boundingBox[(i+1) % 4][0]), (255, 0, 0), 2)
    plt.imshow(matrix)
    plt.show()


def printLines(obj, od, do):
    matrix = obj2Matrix(obj)
    for a, b in zip(od, do):
        if((a == b).all()):
            color = (255, 255, 255)
            size = 2
        else:
            color = (0, 255, 0)
            size = 1
        cv2.line(matrix, (a[1], a[0]), (b[1], b[0]), color, size)
    plt.imshow(matrix)
    plt.show()


def printPoints(obj, points):
    matrix = obj2Matrix(obj)
    for coord in points:
        matrix[coord[0]][coord[1]] = [255, 0, 0]
    plt.imshow(matrix)
    plt.show()


def getFeretDiameters(obj):
    obj = np.array(obj, int)
    # [řádek,sloupec]
    # A - [min řádek, min sloupec]
    # B - [min řádek, max sloupec]
    # C - [max řádek, max sloupec]
    # D - [max řádek, min sloupec]
    boundingBox = np.array([[obj[np.argmin(obj, axis=0)[0]][0],
                             obj[np.argmin(obj, axis=0)[1]][1]],
                            [obj[np.argmin(obj, axis=0)[0]][0],
                             obj[np.argmax(obj, axis=0)[1]][1]],
                            [obj[np.argmax(obj, axis=0)[0]][0],
                             obj[np.argmax(obj, axis=0)[1]][1]],
                            [obj[np.argmax(obj, axis=0)[0]][0],
                             obj[np.argmin(obj, axis=0)[1]][1]]
                            ])
    # boundingbox=[A,B,C,D]

    feretMax = vecSize(boundingBox[0]-boundingBox[2])
    feretMin = feretMax

    step = 2

    theta = step*(math.pi/180)  # 2 stupně v [rad]

    mapa, edge_points = getObjEdges(obj)
    for angle in range(0, 90, step):
        # budu rotovat obdélník po 2 stupních celkem o pí/2
        # print(angle)
        # printBox(obj,boundingBox)
        primky = getLines(boundingBox)
        adjustBox(obj, edge_points, boundingBox, primky)
        new_min = min(
            vecSize(boundingBox[1]-boundingBox[0]),
            vecSize(boundingBox[2]-boundingBox[1]))
        if(new_min < feretMin):
            feretMin = new_min
        rotuj(boundingBox, teziste(obj), theta)
    return feretMin, feretMax


# feretMin,feretMax=getFeretDiameters(obj)
