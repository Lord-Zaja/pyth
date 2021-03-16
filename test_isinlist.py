#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import isinlist as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):
        moje(-1, 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2)), 0)
    with pytest.raises(Exception):
        moje(np.ones((2, 2, 2)), 0)
    with pytest.raises(Exception):
        moje(np.ones((1, 2)), [1, 2])


def test_find_one():
    matrix = np.zeros(3)
    matrix[1] = 5
    assert moje(matrix, 5)
    assert moje(matrix, 0)
    assert not(moje(matrix, 1))


def test_empty_list():
    assert not(moje([], 0))
