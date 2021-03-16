#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import findedges as moje
import pytest
import numpy as np


def test_invalid_values():
    mat = np.ones((2, 2))
    vec = [0, 0]
    with pytest.raises(Exception):  # _na musí být číslo
        moje(mat, mat, 0, 0, vec)
    with pytest.raises(Exception):
        moje(0, mat, 0, 0, 0)
    with pytest.raises(Exception):
        moje(mat, 0, 0, 0, 0)
    with pytest.raises(Exception):  # souřadnice nesmí být vektor
        moje(mat, mat, [0, 0], 0, 0)
    with pytest.raises(Exception):
        moje(mat, mat, 0, [0, 0], 0)


def test_zaporne_souradnice():
    mat = np.ones((2, 2))
    with pytest.raises(Exception):
        moje(mat, mat, -1, 0, 0)
    with pytest.raises(Exception):
        moje(mat, mat, 0, -1, 0)


def test_img_only_ones_or_zeros():
    mat = np.ones((2, 2))
    mat[1, 1] = 5
    with pytest.raises(Exception):
        moje(mat, mat, [0, 1], 0)


def test_remap():
    img = np.array([[0, 1, 0],
                    [1, 1, 1],
                    [1, 1, 0]])
    matrix = np.copy(img)
    matrix[1, 0] = 5
    assert (moje(img, matrix, 2, 1, 5) == np.array([1, 1, 1, 0])).all()
    assert (moje(img, matrix, 1, 1, 5) == [0, 0, 0, 1]).all()
    assert (moje(img, img, 1, 1, 4) == [0, 0, 0, 0]).all()
    assert (moje(np.zeros((3, 3)), matrix, 1, 1, 5) == [1, 1, 1, 1]).all()
