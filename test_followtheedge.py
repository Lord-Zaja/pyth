#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 18:31:08 2021

@author: Zajan Ondřej
"""

from bwconncomp import followtheedge as moje
import pytest
import numpy as np


def test_invalid_values():
    vec=[0,0,0,0]
    with pytest.raises(Exception): # edges musí být list o 4 prvcích
        moje([1,0],0,0,0)
    with pytest.raises(Exception):
        moje(np.ones((2,2)),0,0,0)
    with pytest.raises(Exception):
        moje(0,0,0,0)
    with pytest.raises(Exception): # lastedge musí ležet v množině {0,1,2,3}
        moje(vec,-1,0,0)
    with pytest.raises(Exception): # lastedge musí být číslo
        moje(vec,np.ones((2,2)),0,0)
    with pytest.raises(Exception): # souřadnice nesmí být vektor
        moje(vec,0,[0,0],0)
    with pytest.raises(Exception):
        moje(vec,0,0,[0,0])
    with pytest.raises(Exception): # edges není binární
        moje([1,5,1,1],0,0,0)
    
    
def test_zaporne_souradnice():
    vec=[0,0,0,0]
    with pytest.raises(Exception):
        moje(vec,0,-1,0,)
    with pytest.raises(Exception):
        moje(vec,0,0,-1)
       
    
def test_function():
    assert (0,0,0) == moje([1,1,1,1],0,0,0)
    assert moje([0,1,1,1],3,0,0) == (3,0,-1) # cesta po hranách
    assert moje([1,0,1,1],0,0,0) == (0,1,0)
    assert moje([1,1,0,1],1,0,0) == (1,0,1)
    assert moje([1,1,1,0],2,0,0) == (2,-1,0)
    assert moje([0,1,1,1],1,0,0) == (3,0,-1) # cesta po rozích
    assert moje([1,0,1,1],2,0,0) == (0,1,0)
    assert moje([1,1,0,1],3,0,0) == (1,0,1)
    assert moje([1,1,1,0],0,0,0) == (2,-1,0)

    
    
    