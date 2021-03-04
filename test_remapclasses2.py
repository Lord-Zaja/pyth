#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import remapclasses2 as moje
import pytest
import numpy as np


def test_invalid_values():
    mat=np.ones((2,2))
    vec=[0,0]
    with pytest.raises(Exception): # _na musí být číslo
        moje(mat,mat,vec,vec)
    with pytest.raises(Exception):
        moje(0,mat,vec,0)
    with pytest.raises(Exception):
        moje(mat,0,vec,0)
    with pytest.raises(Exception):
        moje(mat,mat,0,0)
    
    
def test_zaporne_souradnice():
    mat=np.ones((2,2))
    with pytest.raises(Exception):
        moje(mat,mat,[-1,0],0)
    with pytest.raises(Exception):
        moje(mat,mat,[0,-1],0)
    
    
def test_img_only_ones_or_zeros():
    mat=np.ones((2,2))
    mat[1,1]=5
    with pytest.raises(Exception):
        moje(mat,mat,[0,1],0)
    
    
def test_remap():
    img=np.array([[0,1,0],
                  [1,1,1],
                  [1,1,0]])
    matrix=img*2
    moje(matrix/2,matrix,[2,1],5)
    assert (matrix == np.array(img*5)).all()
    
    
    