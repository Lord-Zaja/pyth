#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import bwconncomp as moje
from bwconncomp import getlistofclasses
from bwconncomp import getcoordlistofoneclass
from bwconncomp import binarize
import pytest
import numpy as np
import cv2


def test_invalid_values():
    with pytest.raises(Exception):  # img musí být 2d matice
        moje(0)
    with pytest.raises(Exception):
        moje(np.zeros((2, 2, 2)))


def test_img_only_ones_or_zeros():
    mat = np.ones((2, 2))
    mat[1, 1] = 5
    with pytest.raises(Exception):
        moje(mat)


def test_funkce():
    img = np.array([[0, 1, 0, 0],
                    [1, 1, 0, 1],
                    [1, 1, 0, 1],
                    [1, 0, 0, 1]])

    objclass = np.array([[0, 1, 0, 0],
                         [1, 1, 0, 2],
                         [1, 1, 0, 2],
                         [1, 0, 0, 2]])

    moje(img)
    assert (moje(img) == objclass).all()
    img = np.random.rand(100, 100)
    img[img > 0.5] = 1
    img[img != 1] = 0
    img = img.astype(np.uint8)

    objclass = moje(img)
    assert (binarize(objclass) == img).all()
    moje_tridy = getlistofclasses(objclass)
    moje_conncomp = []
    for trida in moje_tridy:
        moje_conncomp.append(getcoordlistofoneclass(objclass, int(trida)))

    num_labels, labels_im = cv2.connectedComponents(img, None, 4)
    assert (binarize(labels_im) == img).all()
    cv_tridy = getlistofclasses(labels_im)
    cv_conncomp = []
    for trida in cv_tridy:
        cv_conncomp.append(getcoordlistofoneclass(objclass, int(trida)))

    moje_conncomp = [i for i in moje_conncomp if np.size(i) > 20]
    cv_conncomp = [i for i in cv_conncomp if np.size(i) > 20]
    assert np.size(moje_conncomp) == np.size(cv_conncomp)
