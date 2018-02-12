#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 04:03:53 2018

@author: ronsair

[VERIFICATION]
JUSTIFICATION
It would be painful to verify each and every record.
It would be more painful to update changing records. 

[ONGOING UPDATE]
Source data -> Ongoing [Plan wise]
Index matching: Use permutation of habitat and village names
"""

from habitation import Habitation
from proposed import GridProposed
from existing import GridExisting
from validations import Validations as vd
import datetime

class Verifier:
    def __init__(self):
        self.datetime = str(datetime.datetime.now())
    
    def run(self):
        hab_file = input('{:25}\n>_'.format('Habitation Details file, c to cancel'))
        if(not hab_file == 'c'):
            grid_file = input('Proposed Infra file. c to cancel\n>_')
            if(not grid_file == "c"):
                self.habitation = Habitation(hab_file)
#                self.grid_existing = GridExisting(grid_file)
#                self.grid_proposed = GridProposed(grid_file)
                self.validate()

    def error(self,el,ok,msg):
        if(not ok):
            self.status.append(('E',el, msg))

    def validate(self):
        df_hab = self.habitation.df_habitat
#        df_exi = self.grid_existing.df_existing
#        df_pro = self.grid_proposed.df_proposed
        self.habitation.verify()
        self.habitation.print_status()
        ## Record length
#        el = "Checking record lengths"
#        self.error(el, *vd.record_length(len(df_hab), len(df_exi), len(df_pro)))
        
        
        
                    
        
#        if(not habfile == 'n'):
#            hab = Habitat(habfile)
#            if(hab.reformat()):
#                hab.verify()
#        
#        pfile = input('Proposed Filename: ')
#        if(not pfile == "n"):
#            p = GridProposed(pfile)
#            if(p.reformat()):
#                p.verify()
#            ex = GridExisting(p.filename)
#            if(ex.reformat()):
#                ex.verify()


# existInfrafile = input('Existing Infra Filename: ')
# ex = GridExisting(existInfrafile)
# ex.verify()

verifier = Verifier()
verifier.run()

    
    
    
    
    