#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import remapclasses3 as moje
import pytest
import numpy as np


def test_invalid_values():
    mat = np.ones((2, 2))
    vec = [[0, 0], [1, 1]]
    with pytest.raises(Exception):  # beginneighbor musí být číslo
        moje(mat, mat, vec, [1, 2, 3, 4])
    with pytest.raises(Exception):      # beginneighbor nesmí být větší jak
        moje(mat, mat, vec, 2)             # max řádek neighbors
    with pytest.raises(Exception):
        moje(mat, mat, vec, -2)
    with pytest.raises(Exception):  # img musí být 2d matice
        moje(0, mat, vec, 0)
    with pytest.raises(Exception):  # objclass musí být 2d matice
        moje(mat, 0, vec, 0)
    with pytest.raises(Exception):  # neighbors musí být mattice se
        moje(mat, mat, 0, 0)        # souřadnicemi


def test_zaporne_souradnice():
    mat = np.ones((2, 2))
    with pytest.raises(Exception):
        moje(mat, mat, [-1, 0], 0)
    with pytest.raises(Exception):
        moje(mat, mat, [0, -1], 0)


def test_img_only_ones_or_zeros():
    vec = [[0, 0], [1, 1]]
    mat = np.ones((2, 2))
    mat[1, 1] = 5
    with pytest.raises(Exception):
        moje(mat, mat, vec, 0)


def test_remap():
    img = np.array([[0, 1, 0, 0],
                    [1, 1, 1, 1],
                    [1, 1, 0, 1],
                    [1, 0, 0, 1]])

    objclass = np.array([[0, 2, 0, 0],
                         [2, 2, 2, 2],
                         [2, 1, 0, 5],
                         [2, 0, 0, 2]])

    moje(img, objclass, [[3, 1], [3, 2]], 0)
    assert (objclass == np.array([[0, 5, 0, 0],
                                  [5, 5, 5, 5],
                                  [5, 5, 0, 5],
                                  [5, 0, 0, 2]])).all()
    img = np.array([[0, 1, 0, 0],
                    [1, 1, 1, 1],
                    [1, 1, 0, 1],
                    [1, 0, 0, 1]])

    objclass = np.array([[0, 2, 0, 0],
                         [2, 2, 2, 2],
                         [2, 1, 0, 2],
                         [5, 0, 0, 2]])

    moje(img, objclass, [[0, 2], [0, 3]], 0)
    assert (objclass == np.array([[0, 5, 0, 0],
                                  [5, 5, 5, 5],
                                  [5, 5, 0, 5],
                                  [5, 0, 0, 2]])).all()
