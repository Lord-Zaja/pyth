#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import getcoordlistofoneclass as moje
import pytest
import numpy as np


def test_invalid_values():
    with pytest.raises(Exception):
        moje(-1,5)
    with pytest.raises(Exception):
        moje(np.ones((2,2)),-1)
    with pytest.raises(Exception):
        moje(np.ones((2,2)),[1,2])
    with pytest.raises(Exception):
        moje(np.ones((3,3,3,3)),1)
    with pytest.raises(Exception):
        moje(np.ones((2,2,2)),1)
        

def test_dim_of_return_value():
    assert 2 == np.shape(moje(np.ones((10,5)),1))[1]
    
def test_ones():#pro každý pixel byla zapsána souřadnice
    matrix=np.ones((50,75))
    testmatrix=np.zeros(np.shape(matrix))
    coords=moje(matrix,1)
    for coord in coords:
        testmatrix[coord[0]][coord[1]]=1
    assert (testmatrix == matrix).all()
    