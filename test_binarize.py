#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import binarize as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):
        moje(-1)
    with pytest.raises(Exception):
        moje(np.ones((3, 3, 3, 3)))
    with pytest.raises(Exception):
        moje(np.ones((2, 2, 2)))


def test_dim_of_return_value():
    assert np.shape(np.ones((10, 5))) == np.shape(moje(np.ones((10, 5))))


def test_ones_and_zeros():
    assert (np.ones((50, 75)) == moje(np.ones((50, 75)))).all()
    assert (np.zeros((50, 75)) == moje(np.zeros((50, 75)))).all()
