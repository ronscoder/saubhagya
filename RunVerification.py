#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 04:03:53 2018

@author: ronsair

It would be painful to verify each and every record.
It would be more painful to update changing records. 
"""

from habitat import Habitat
from proposed import GridProposed
from existing import GridExisting

habfile = input('Habitation Filename: ')
if(not habfile == 'n'):
    hab = Habitat(habfile)
    if(hab.reformat()):
        hab.verify()

pfile = input('Proposed Filename: ')
if(not pfile == "n"):
    p = GridProposed(pfile)
    if(p.reformat()):
        p.verify()
    ex = GridExisting(p.filename)
    if(ex.reformat()):
        ex.verify()


# existInfrafile = input('Existing Infra Filename: ')
# ex = GridExisting(existInfrafile)
# ex.verify()

    
    
    
    
    