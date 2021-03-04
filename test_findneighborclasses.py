#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import findneighborclasses as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):#nesmí být číslo, musí mít správný rozměr
        moje(-1,np.ones((2,2)))
    with pytest.raises(Exception):
        moje(np.ones((2,2)),-1)
    with pytest.raises(Exception):
        moje(np.ones((2,2)),np.ones((3,3,3)))
    
def test_zaporne_souradnice():
    with pytest.raises(Exception):
        moje([-1,1],np.ones((2,2)))
    with pytest.raises(Exception):
        moje([1,-1],np.ones((2,2)))
    
def test_find_one():
    matrix=np.zeros((3,3))
    matrix[0,1]=1
    matrix[1,2]=2
    matrix[2,2]=2
    matrix[0,0]=1
    assert (moje([[1,0],[2,1]],matrix) == [[1],[2]]).all()
    
def test_empty_neighbors():
    with pytest.raises(Exception):
        moje([],np.ones((2,2)))

    
    