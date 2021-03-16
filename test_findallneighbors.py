#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import findallneighbors as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):
        moje(-1, 0, 0)
    with pytest.raises(Exception):
        moje(np.ones((3, 3, 3, 3)), 0, 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2, 2)), 0, 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), -1, 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), 0, -1)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), 2, 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), 0, 2)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), [1, 2], 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), 0, [1, 2])


def test_dim_of_return_value():
    assert np.shape(moje(np.ones((3, 3)), 1, 1))[1] == 2


def test_ones_and_zeros():
    assert (moje(np.ones((3, 3)), 1, 1) == [[0, 1], [2, 1], [1, 0], [1, 2]])
    assert (np.size(moje(np.zeros((3, 3)), 1, 1)) == 0)
