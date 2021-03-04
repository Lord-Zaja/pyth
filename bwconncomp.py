#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 17:56:41 2021

@author: Zajan Ondřej
"""

import numpy as np


def rgb2gray(img, mez):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 5.1.21

    Funkce: Převede barevný obrázek na černobílý

    Potřebné moduly: numpy as np

    Parametry
    =========

    img - původní černobílý obrázek

    mez - při překročení, pixel je vyhodnocen jako černý <1,255>

    return - binární obrázek - matice
    """
    if np.size(np.shape(img)) != 3 or np.shape(img)[2] != 3:
        raise Exception("Matice img má špatný rozměr")
    if np.size(np.shape(mez)) != 0:
        raise Exception("Mez musí být číslo")
    if mez > 255 or mez < 0:
        raise Exception("Mez musí ležet v intevalu <0;255>")
    mez = mez * 3
    binary_img = np.zeros(np.shape(img)[0:2])
    for row_idx, row in enumerate(img):
        for col_idx, pix in enumerate(row):
            if (int(pix[0])+int(pix[1])+int(pix[2])) > mez:
                binary_img[row_idx, col_idx] = 1  # jednička je zde jako černá
    return binary_img

def binarize(seznam):
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
    if np.size(np.shape(seznam)) != 2:
        raise Exception("Matice seznam má špatný rozměr")
    matrix = np.zeros(np.shape(seznam)[:2]).astype(np.uint8)
    #uint8 aby matice fungovala s cv2
    for _y, row in enumerate(seznam):
        for _x, prvek in enumerate(row):
            if (prvek != 0).any():
                matrix[_y][_x] = 1
    return matrix

def getcoordlistofoneclass(objclass, myc):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 12.2.21

    Funkce: V matici objclass najde všechny prvky myc a vrátí jejich souřadnice

    Potřebné moduly: numpy as np

    Parametry
    =========

    objClass - matice popisující objekty pomocí očíslování bloků jedniček

    myc - moje hledaná třída

    return - pole obsahující v každém prvku pole souřadnic [x,y] každého pixelu
     v dané třídě
    """
    if np.size(np.shape(objclass)) != 2:
        raise Exception("Matice objclass má špatný rozměr")
    if np.size(np.shape(myc)) != 0:
        raise Exception("Myc musí být číslo")
    if myc <= 0:
        raise Exception("Myc musí být větší než nula")
    res = np.where(objclass == myc)
    return list(map(list, zip(res[0], res[1])))


def getlistofclasses(objclass):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 12.2.21

    Funkce: Vrátí množinu čísel uvnitř matice objclass

    Potřebné moduly: numpy as np

    Parametry
    =========

    objClass - matice popisující objekty pomocí očíslování bloků jedniček

    return - pole obsahující všechny třídy - popis objektu
    """
    if np.size(np.shape(objclass)) != 2:
        raise Exception("Matice objclass má špatný rozměr")
    pole = np.empty((0, 1), int)
    objclass = np.array(objclass)
    for row in objclass:
        for trida in row:
            if trida != 0:
                if not np.any(pole == trida):
                    pole = np.vstack((pole, trida))
    return pole


def findallneighbors(img, _x, _y):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 16.2.21

    Funkce: Najde v matici img na souřadnicích _x,_y sousední prvky
            obsahující jedničku. Funkce kouká do všech směrů mimo diagonální.

    Potřebné moduly: numpy as np

    Parametry
    =========

    img - původní černobílý obrázek

    _x,_y - souřadnice zkoumaného pixelu, x: sloupec, y: řádek

    neighbors - seznam obsahující v každé položce obě souřadnice souseda bodu
                x,y
    """
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice img má špatný rozměr")
    # if ((img != 0) & (img !=1 )).any():
    #     raise Exception("Matice img není binární")
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice objclass má špatný rozměr")
    if _x < 0 or _x >= np.shape(img)[1]:
        raise Exception("Souřadnice _x neleží v matici img")
    if _y < 0 or _y >= np.shape(img)[0]:
        raise Exception("Souřadnice _y neleží v matici img")
    if np.size(np.shape(_x)) != 0:
        raise Exception("Souřadnice _x musí být číslo")
    if np.size(np.shape(_y)) != 0:
        raise Exception("Souřadnice _y musí být číslo")
    neighbors = list()
    if _x != 0 and img[_y][_x-1]:  # pixel vlevo
        neighbors.append([_x-1, _y])
    if _x != np.shape(img)[1] and img[_y][_x+1]:  # pixel vpravo
        neighbors.append([_x+1, _y])
    if _y != 0 and img[_y-1][_x]:  # pixel nahoře
        neighbors.append([_x, _y-1])
    if _y != np.shape(img)[0] and img[_y+1][_x]:  # pixel dole
        neighbors.append([_x, _y+1])
    return neighbors


def findneighbors(img, _x, _y):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 12.2.21

    Funkce: Najde v matici img na souřadnicích _x,_y sousední prvky
            obsahující jedničku. Funkce kouká pouze nahoru na doleva.

    Parametry
    =========

    img - původní černobílý obrázek

    x,y - souřadnice zkoumaného pixelu

    neighbors - seznam obsahující v každé položce obě souřadnice souseda bodu
                x,y
    """
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice img má špatný rozměr")
    # if ((img != 0) & (img !=1 )).any():
    #     raise Exception("Matice img není binární")
    if np.size(np.shape(_x)) != 0:
        raise Exception("Souřadnice _x musí být číslo")
    if np.size(np.shape(_y)) != 0:
        raise Exception("Souřadnice _y musí být číslo")
    if _x < 0 or _x >= np.shape(img)[1]:
        raise Exception("Souřadnice _x neleží v matici img")
    if _y < 0 or _y >= np.shape(img)[0]:
        raise Exception("Souřadnice _y neleží v matici img")
    neighbors = list()
    if _x != 0 and img[_y][_x-1]:  # pixel vlevo
        neighbors.append([_x-1, _y])
    if _y != 0 and img[_y-1][_x]:  # pixel nahoře
        neighbors.append([_x, _y-1])
    return neighbors


def isinlist(seznam, prvek):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 12.2.21

    Funkce: Hledá prvek uvnitř listu seznam

    Potřebné moduly: numpy as np

    Parametry
    =========

    seznam - zkoumaný list

    prvek - číselná hodnota, kterou v sezmanu hledám

    return - True/False - hodnota nalezena/nenalezena
    """
    if np.size(np.shape(seznam)) != 1:
        raise Exception("List seznam má špatný rozměr")
    if np.size(np.shape(prvek)) != 0:
        raise Exception("Prvek musí být číslo")
    fin = np.array(seznam)
    if np.size(fin) == 0:
        return False
    if np.size(fin) == 1:
        return bool(fin == prvek)
    for i in fin:
        if i == prvek:
            return True
    return False


def findneighborclasses(neighbors, objclass):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 12.2.21

    Funkce: Vrátí množinu daných hodnot tříd uvnitř objclass na souřadnicích
            uvnitř listu neighbors

    Potřebné moduly: numpy as np

    Potřebné funkce: isinlist()

    Parametry
    =========

    neighbors - seznam souřadnic sousedních jedniček

    objClass - matice popisující objekty pomocí očíslování bloků jedniček

    return - Množina tříd
    """
    if np.size(np.shape(neighbors)) != 2 or np.shape(neighbors)[1] != 2:
        raise Exception("Neighbors seznam má špatný rozměr")
    if np.size(np.shape(objclass)) != 2:
        raise Exception("Objclass seznam má špatný rozměr")
    neighborclasses = list()
    if np.shape(neighbors)[0] == 1:
        return objclass[neighbors[0][1]][neighbors[0][0]]
    neighborclasses = objclass[neighbors[0][1]][neighbors[0][0]]
    for coord in neighbors[1:]:
        if coord[0] < 0 or coord[1] < 0:
            raise Exception("Neexistující soused - záporná souřadnice")
        if not isinlist([neighborclasses], objclass[coord[1]][coord[0]]):
            neighborclasses = np.vstack(
                (neighborclasses, objclass[coord[1]][coord[0]]))
    return neighborclasses  # list čísel různých tříd (min 1 max 4)


def remapclasses2(img, objclass, xynow, _na):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 13.2.21

    Upraveno: 19.2.21

    Funkce: Přepíše všechny dané třídy v jednom řádku v rámci jednoho objektu.
            Funkce dále zkoumá, jestli jsou všechny prvky nad přepisovanými
            prvky přepsány. Při "zablokování cesty" směrem dolu prvky dole
            přepíše.

    Potřebné moduly:    numpy as np

    Potřebné funkce:    remapclasses3(), findedges(), followtheedge()

    Parametry
    =========

    objClass - matice popisující objekty pomocí očíslování bloků jedniček

    xynow - nynější souřadnice v matici

    z - z čeho změnit třídu

    na - na co změnit třídu

    return - matice objClass, všude místo "z" je "na"
    """
    if np.size(np.shape(objclass)) != 2:
        raise Exception("Objclass seznam má špatný rozměr")
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice img má špatný rozměr")
    # if ((img != 0) & (img !=1 )).any():
    #     raise Exception("Matice img není binární")
    if np.size(np.shape(_na)) != 0:
        raise Exception("Prvek musí být číslo")
    if xynow[0] < 0 or xynow[0] >= np.shape(img)[1]:
        raise Exception("Souřadnice x z xynow neleží v matici img")
    if xynow[1] < 0 or xynow[1] >= np.shape(img)[0]:
        raise Exception("Souřadnice y z xynow neleží v matici img")
    # if ((img!=0) & (img!=1)).any():
    #     raise Exception("Matice img není binární")
    dole1 = -1
    dole2 = -1
    _y = xynow[1]
    # první prvek kde začínám ještě nemá třídu, je nula
    objclass[_y][xynow[0]] = _na
    # dole je hrana
    if _y != (np.shape(objclass)[0]-1) and (img[_y+1][xynow[0]] == 0 or
                                            objclass[_y+1][xynow[0]] == _na):
        dole1 = xynow[0]
    for _x in range(xynow[0]-1, -1, -1):
        if img[xynow[1]][_x] == 0:  # vyjel jsem z objektu => konec
            break
        objclass[xynow[1]][_x] = _na
        # nahoře je nepřepsaný soused
        if (xynow[1] > 0 and img[xynow[1]-1][_x] != 0 and
           objclass[xynow[1]-1][_x] != _na):
            remapclasses3(img, objclass, [[_x, xynow[1]], [_x, xynow[1]-1]], 1)
        # dole je hrana
        if _y != (np.shape(objclass)[0]-1) and (img[_y+1][_x] == 0 or
                                                objclass[_y+1][_x] == _na or
                                                objclass[_y+1][_x] == 0):
            if dole1 == -1:
                dole1 = _x
        elif dole1 != -1:  # místo, kde končí hrana
            dole2 = _x
            edges2 = np.zeros(4)
            lastedge = 1  # začínám s hranou vpravo
            _y2 = _y + 1
            _x2 = dole2
            while True:
                if _y2 < _y:  # překročím startovní y => break
                    break
                edges2 = findedges(img, objclass, _x2, _y2, _na)
                # vše přepsáno
                if np.sum(edges2) == 4 and objclass[_y2][_x2] == _na:
                    break
                if edges2[1]:
                    # vpravo není žádné místo => přepíšu třídy daného řádku
                    remapclasses2(img, objclass, [_x2, _y2], int(_na))
                lastedge, _x2, _y2 = followtheedge(edges2, lastedge, _x2, _y2)
            dole2 = -1
            dole1 = -1
    return objclass


def findedges(img, objclass, _x, _y, _na):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 19.2.21

    Upraveno: 20.2.21

    Funkce: Najde "hrany" v dané souřadnici _x,_y
            (hrana: nepřepsaný prvek, mimo objekt, nidky nepřepsaná třída)

    Potřebné moduly: numpy as np

    Parametry
    =========

    img - Binární matice původního obrázku

    objclass - matice tříd (labelů)

    _x,_y - souřadnic zkoumaného pixelu

    _na - na jaké číslo zrovna třídy přepisuji

    return - List o velikosti 4, určující kde se vyskytují hrany.
            (nahoře, vpravo, dole, vlevo)
    """
    if np.size(np.shape(objclass)) != 2:
        raise Exception("Objclass seznam má špatný rozměr")
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice img má špatný rozměr")
    # if ((img != 0) & (img !=1 )).any():
    #     raise Exception("Matice img není binární")
    if np.size(np.shape(_na)) != 0:
        raise Exception("Prvek musí být číslo")
    if np.size(np.shape(_x)) != 0:
        raise Exception("Souřadnice _x musí být číslo")
    if np.size(np.shape(_y)) != 0:
        raise Exception("Souřadnice _y musí být číslo")
    if _x < 0 or _x >= np.shape(img)[1]:
        raise Exception("Souřadnice _x neleží v matici img")
    if _y < 0 or _y >= np.shape(img)[0]:
        raise Exception("Souřadnice _y neleží v matici img")
    # [nahoře,vpravo,dole,vlevo]
    edges = np.zeros(4)
    if (_y == 0 or img[_y-1][_x] == 0 or objclass[_y-1][_x] == _na or
            objclass[_y-1][_x] == 0):  # up
        edges[0] = 1
    if (_x == np.shape(objclass)[1]-1 or img[_y][_x+1] == 0 or
            objclass[_y][_x+1] == _na or objclass[_y][_x+1] == 0):  # right
        edges[1] = 1
    if (_y == np.shape(objclass)[0]-1 or img[_y+1][_x] == 0 or
            objclass[_y+1][_x] == _na or objclass[_y+1][_x] == 0):  # down
        edges[2] = 1
    if (_x == 0 or img[_y][_x-1] == 0 or objclass[_y][_x-1] == _na or
            objclass[_y][_x-1] == 0):  # left
        edges[3] = 1
    return edges


def followtheedge(edges, lastedge, _x, _y):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 19.2.21

    Upraveno: 20.2.21

    Funkce: Sleduje hrany po směru hodinových ručiček. Při zavolání udělá
            pouze jeden krok.

    Potřebné moduly:    numpy as np

    Parametry
    =========

    edges - hrany daného pixelu numpy array (1,4)

    lastedge - číslo hrany při posledním kroku (0-3, nahoře,vpravo,dole,vlevo)

    _x,_y - souřadnice zkoumaného pixelu

    return - nové hodnoty lastedge, _x, _y
    """
    edges = np.array(edges)
    if np.size(np.shape(edges)) != 1 or np.size(edges) != 4:
        raise Exception("Array edges má špatný rozměr")
    if ((edges != 1) & (edges != 0)).any():
        raise Exception("Edges není binární")
    if np.size(np.shape(lastedge)) != 0:
        raise Exception("Lastedge musí být číslo")
    if (lastedge != 0) & (lastedge != 1) & (lastedge != 2) & (lastedge != 3):
        raise Exception("Lastedge musí leže v množině {0,1,2,3}")
    if np.size(np.shape(_x)) != 0:
        raise Exception("Souřadnice _x musí být číslo")
    if np.size(np.shape(_y)) != 0:
        raise Exception("Souřadnice _y musí být číslo")
    if _x < 0:
        raise Exception("Souřadnice _x nesmí být záporná")
    if _y < 0:
        raise Exception("Souřadnice _y nesmí být záporná")
    if np.sum(edges) == 0:  # žádná hrana (roh)
        if lastedge == 0:  # poslední hrana nahoře => jdi nahoru, strana vlevo
            _y -= 1
            lastedge = 3
        elif lastedge == 1:
            # poslední hrana vpravo => jdi doprava, strana nahoře
            _x += 1
            lastedge = 0
        elif lastedge == 2:  # poslední hrana dole => jdi dolu, strana vpravo
            _y += 1
            lastedge = 1
        elif lastedge == 3:  # poslední hrana vlevo => jdi vlevo, strana dole
            _x -= 1
            lastedge = 2
    elif np.sum(edges) == 1:  # jedna hrana
        if edges[lastedge]:
            if edges[0]:  # hrana nahoře => jdi doprava
                _x += 1
                lastedge = 0
            elif edges[1]:  # hrana vpravo => jdi dolu
                _y += 1
                lastedge = 1
            elif edges[2]:  # harna dole => jdi doleva
                _x -= 1
                lastedge = 2
            elif edges[3]:  # hrana vlevo => jdi nahoru
                _y -= 1
                lastedge = 3
        else:  # jako pokud není žádná hrana
            if lastedge == 0:
                # poslední hrana nahoře => jdi nahoru, strana vlevo
                _y -= 1
                lastedge = 3
            elif lastedge == 1:
                # poslední hrana vpravo => jdi doprava, strana nahoře
                _x += 1
                lastedge = 0
            elif lastedge == 2:
                # poslední hrana dole => jdi dolu, strana vpravo
                _y += 1
                lastedge = 1
            elif lastedge == 3:
                # poslední hrana vlevo => jdi vlevo, strana dole
                _x -= 1
                lastedge = 2
    # dvě hrany naproti sobě
    elif(np.sum(edges) == 2) and ((edges[0] and edges[2]) or (edges[1] and
                                                              edges[3])):
        if edges[lastedge]:
            if lastedge == 0 and edges[0]:  # pokračuji po hraně nahoře vpravo
                _x += 1
            elif lastedge == 1 and edges[1]:  # pokarčuji po pravé hraně dolu
                _y += 1
            elif lastedge == 2 and edges[2]:  # pokračuj po dolní hraně doleva
                _x -= 1
            elif lastedge == 3 and edges[3]:  # pokračuj po levé hraně nahoru
                _y -= 1
        else:
            if lastedge == 0:
                # poslední hrana nahoře => jdi nahoru, strana vlevo
                _y -= 1
                lastedge = 3
            elif lastedge == 1:
                # poslední hrana vpravo => jdi doprava, strana nahoře
                _x += 1
                lastedge = 0
            elif lastedge == 2:
                # poslední hrana dole => jdi dolu, strana vpravo
                _y += 1
                lastedge = 1
            elif lastedge == 3:
                # poslední hrana vlevo => jdi vlevo, strana dole
                _x -= 1
                lastedge = 2
    elif np.sum(edges) == 2:  # dvě hrany a nejsou naproti sobě - roh
        if edges[lastedge]:  # jdu po existující hraně
            if edges[0] and edges[1]:
                # pravý horní roh => šel jsem vpravo, půjdu dolu
                _y += 1
                lastedge = 1
            elif edges[1] and edges[2]:
                # pravý dolní roh => šel jsem dolu, půjdu doleva
                _x -= 1
                lastedge = 2
            elif edges[2] and edges[3]:
                # levý dolní roh => šel jsem vlevo, půjdu nahoru
                _y -= 1
                lastedge = 3
            elif edges[3] and edges[0]:
                # levý horní roh => šel jsem nahoru, půjdu doprava
                _x += 1
                lastedge = 0
        else:  # hrana zmizela => jako pokud není hrana žádná
            if lastedge == 0:
                # poslední hrana nahoře => jdi nahoru, strana vlevo
                _y -= 1
                lastedge = 3
            elif lastedge == 1:
                # poslední hrana vpravo => jdi doprava, strana nahoře
                _x += 1
                lastedge = 0
            elif lastedge == 2:
                # poslední hrana dole => jdi dolu, strana vpravo
                _y += 1
                lastedge = 1
            elif lastedge == 3:
                # poslední hrana vlevo => jdi vlevo, strana dole
                _x -= 1
                lastedge = 2
    elif np.sum(edges) == 3:  # slepá ulička
        if not edges[0]:
            # cesta nahoru => zabloudil jsem zezhora =>
            # hrana vlevo a jdu nahoru
            _y -= 1
            lastedge = 3
        elif not edges[1]:
            # cesta doparva => zabloudil jsem zprava =>
            # hrana nahoře a jdi doprava
            _x += 1
            lastedge = 0
        elif not edges[2]:
            # cesta dolu => zabloudil jsem zezdola => hrana vparvo a jdi dolu
            _y += 1
            lastedge = 1
        elif not edges[3]:
            # cesta doleva => zabloudil jsem zleva => hrana dole a jdi doleva
            _x -= 1
            lastedge = 2
    return lastedge, _x, _y


def remapclasses3(img, objclass, neighbors, beginneighbor):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 14.2.21

    Upraveno: 19.2.21

    Funkce: Přepisuje třídy uvnitř objclass na aktuální hodnotu.
            Funkce sleduje hrany.
            Funkce nejdříve docestuje do nejkrajnějšího levého horního rohu,
            přičemž sleduje, zda jsou při cestě doleva nepřepsané třídy.
            Případně celý spodní blok přepíše.
            Funkce pak cestuje po kraji nepřepsaného objektu a vše přepisuje
            pomocí remapclasses2.

    Potřebné moduly:    numpy as np

    Potřebné funkce:    findedges(), remapclasses2(), followtheedge()

    Parametry
    =========

    objClass - matice popisující objekty pomocí očíslování bloků jedniček

    neighbors - sousedi původního prvku

    beginNeighbor - číslo souseda (1/0) u kterého začínám, číslo souseda nahoře
                    od aktuálního prvku
    """
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice img má špatný rozměr")
    # if ((img != 0) & (img !=1 )).any():
    #     raise Exception("Matice img není binární")
    if np.size(np.shape(objclass)) != 2:
        raise Exception("Objclass seznam má špatný rozměr")
    if np.size(np.shape(neighbors)) != 2 or np.shape(neighbors)[1] != 2:
        raise Exception("Neighbors seznam má špatný rozměr")
    for coord in neighbors:
        _x=coord[0]
        _y=coord[1]
        if np.size(np.shape(_x)) != 0:
            raise Exception("Souřadnice _x musí být číslo")
        if np.size(np.shape(_y)) != 0:
            raise Exception("Souřadnice _y musí být číslo")
        if _x < 0:
            raise Exception("Souřadnice _x nesmí být záporná")
        if _y < 0:
            raise Exception("Souřadnice _y nesmí být záporná")
    if (beginneighbor >= np.shape(neighbors)[0] or
            beginneighbor <= -np.shape(neighbors)[0]):
        raise Exception("Beginneighbor neleží v neighbors")

    _y = neighbors[beginneighbor][1]  # souřadnice začínajícího horního souseda
    _x = neighbors[beginneighbor][0]
    _na = objclass[neighbors[int(not beginneighbor)][1]][neighbors[int(
        not beginneighbor)][0]]  # na co chci třídy přepsat
    # přepsání prvku, pro kterého byly zjištěny dva sousedi
    objclass[_y+1][_x] = _na
    edges = np.zeros(4)
    # dostaň se nejkarjnějšího levého/pravého horního rohu
    # doleva,nahoru, doprava dokud nemůžu nahoru pak nahoru
    while True:
        edges = findedges(img, objclass, _x, _y, _na)
        if not edges[3]:  # místo vlevo => jdi doleva
            _x -= 1
            edges = findedges(img, objclass, _x, _y, _na)
            if not edges[2]:
                # pokud je dole místo, musím sledovat pravou hranu
                # a všechno zde přepsat
                lastedge = 1
                _x2 = _x
                _y2 = _y+1
                while True:
                    if _y2 < _y:  # překročím startovní y => break
                        break
                    edges2 = findedges(img, objclass, _x2, _y2, _na)
                    # vše přepsáno
                    if np.sum(edges2) == 4 and objclass[_y2][_x2] == _na:
                        break
                    if edges2[1]:
                        # vpravo není žádné místo => přepíšu třídy daného řádku
                        remapclasses2(img, objclass, [_x2, _y2], int(_na))
                    lastedge, _x2, _y2 = followtheedge(edges2, lastedge,
                                                       _x2, _y2)
        elif not edges[0]:  # místo nahoře
            _y -= 1
        elif not edges[1]:  # místo vpravo
            while (_x < (np.shape(objclass)[1]-1) and
                   objclass[_y][_x+1] != 0 and objclass[_y][_x+1] != _na and
                   (_y == 0 or objclass[_y-1][_x] == 0)):
                _x += 1
            # nemohl jsem jít nahoru
            if _y == 0 or objclass[_y-1][_x] == 0 or objclass[_y-1][_x] == _na:
                break
            else:  # můžu jít nahoru
                _y -= 1
        else:  # nikde místo už není
            break
    # postupně se posunuj po pravém kraji od shora a přepisuj řádky
    # nahoru pokud nahoře je nepřepsaná třída,
    # doprava,
    # dolu,
    # doleva dokud nemůžu dolu, pak nahoru,
    edges = np.zeros(4)
    lastedge = 0  # začínám s hranou nahoře vždy
    while True:
        if _y > neighbors[beginneighbor][1]:  # překročím startovní y => break
            break
        edges = findedges(img, objclass, _x, _y, _na)
        # vpravo není žádné místo a nejdu nahoru => přepíšu třídy daného řádku
        if edges[1] and lastedge != 3:
            remapclasses2(img, objclass, [_x, _y], int(_na))
        if np.sum(edges) == 4:  # žádná cesta => break
            break
        lastedge, _x, _y = followtheedge(edges, lastedge, _x, _y)


def bwconncomp(img):
    """
    Autor: Zajan Ondřej

    Vytvořeno: 5.1.21

    Upraveno: 14.2.21

    Funkce: Vrátí matici velikosti img, do které zapíše ke každému objektu z
            img unikátní číslo (třídu).
            Funkce sleduje řádek po řádku, ale někdy rekurzivně "zabloudí"
            i mimo daný řádek.

    Potřebné moduly: numpy as np

    Potřebné funkce:    findneighbors(), findneighborclasses(), remapclasses2(),
                        remapclasses3()

    Parametry
    =========

    img - původní černobílý obrázek

    return - Matice s třídami na souřadnicích objektů z img
    """
    if np.size(np.shape(img)) != 2:
        raise Exception("Matice img má špatný rozměr")
    # if ((img != 0) & (img !=1 )).any():
    #     raise Exception("Matice img není binární")
    neighbors = list()
    noclasses = 0  # aktuální třída
    pix = np.zeros(2)
    objclass = np.zeros(np.shape(img))
    for row_idx, row in enumerate(img):
        for col_idx, pix in enumerate(row):
            if pix:
                neighbors = findneighbors(img, col_idx, row_idx)
                if np.shape(neighbors)[0] == 0:  # žádný soused, nový objekt
                    noclasses += 1  # nový objekt
                    objclass[row_idx, col_idx] = noclasses
                else:
                    remapc = findneighborclasses(neighbors, objclass)
                    if np.size(remapc) == 1:
                        # všichni sousedi sdílí stejnou třídu
                        # pak přepíšu pouze třídu u nynějšího pixelu
                        objclass[row_idx][col_idx] = remapc
                    else:
                        keepc = min(remapc)  # třída, kterou chci všude zapsat
                        if keepc == objclass[neighbors[0][1]][neighbors[0][0]]:
                            # menší třída je u prvního souseda
                            if neighbors[0][1] > neighbors[1][1]:
                                # menší třída je dole
                                remapclasses3(img, objclass, neighbors, 1)
                            else:
                                # třídy, které přepíšu
                                remapc = np.setdiff1d(remapc, min(remapc))
                                # menší třída je nahoře
                                remapclasses2(img, objclass, [
                                              col_idx, row_idx], int(keepc))
                        else:  # menší je u druhého souseda
                            if neighbors[0][1] < neighbors[1][1]:
                                # menší třída je dole
                                remapclasses3(img, objclass, neighbors, 0)
                            else:
                                # třídy, které přepíšu
                                remapc = np.setdiff1d(remapc, min(remapc))
                                remapclasses2(img, objclass, [
                                              col_idx, row_idx], int(keepc))
                        noclasses -= 1
    return objclass
