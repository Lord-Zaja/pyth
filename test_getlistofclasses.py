#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import getlistofclasses as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):
        moje(-1)
    with pytest.raises(Exception):
        moje(np.ones((3,3,3,3)))
    with pytest.raises(Exception):
        moje(np.ones((2,2,2)))
        

def test_dim_of_return_value():
    assert 1 == np.shape(moje(np.random.rand(50,75)))[1]
    
def test_ones_and_zeros():
    assert (moje(np.ones((50,75))) == [1])
    assert (np.size(moje(np.zeros((50,75)))) == 0)
    
    