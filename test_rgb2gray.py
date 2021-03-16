#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import rgb2gray as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):
        moje(-1, -1)
    with pytest.raises(Exception):
        moje(np.ones((3, 3, 3, 3)), 5)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), -1)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), [1, 2])
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), 250)
    with pytest.raises(Exception):
        moje(np.ones((2, 2, 2)), 250)


def test_dim_of_return_value():
    assert np.shape(np.ones((10, 5, 3)))[
        :-1] == np.shape(moje(np.ones((10, 5, 3)), 55))
