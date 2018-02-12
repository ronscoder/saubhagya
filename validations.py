#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:05:44 2018

@author: ronsair
"""
import functools as fn

class Validations:
    """
    Common verfification module
    """
    def hh_equation(hh, hh_ele, hh_bal, bpl, bpl_ele, bpl_bal):
        """
        [HABITAT]
        1. Sum of sub HH equals total 
        2. Sum of sub BPL equals total BPL
        3. bpl hh not > hh
        """
        if(not int(hh_ele) + int(hh_bal) == int(hh)):
            return False, 'Total HH := ∑HH(electrified, balance)'

        if(not int(bpl_ele) + int(bpl_bal) == int(bpl)):
            return False, 'Total BPL := ∑BPL(electrified, balance)'
        
        if(hh < bpl):
            return False, 'Total BPL :<= Total HH (Imm)'
        return True, 'OK'
        
    def free_equation(bpl, free, not_free, hh_bal):
        """
        [PROPOSED]
        Free connection eligibility
        bpl + free + !free = total balance
        """
        if(not 
        bpl + free + not_free == hh_bal
        ):
            return False, 'HH Balance := Balance BPL + Free + Not Free'
        
        return True, 'OK'

    def cross_hh_equation(p_bpl_bal, p_hh_bal, h_hh_bal, h_bpl_bal):
        """
        [PROPOSED, HABITAT]
        1. balance hh[PROPOSED] = balance hh[HABITAT]
        2. balance bpl[PROPOSED] = balance bpl[HABITAT]
        """
        if(not
           p_hh_bal == h_hh_bal
           ):
            return False, 'HH Balance in [PROPOSED] := HH Balance in [HABITAT]'
        
        if(not
           p_bpl_bal == h_bpl_bal
           ):
            return False, 'BPL Balance in [PROPOSED] := BPL Balance in [HABITAT]'
        return True, 'OK'
    
    
    def record_length(len_hab, len_exi, len_pro):
        if(not
           len_hab == len_exi == len_pro):
            return False, 'Numbers of habitats should match across sheets'
        return True, 'OK'
        
    def village_details(slno_hep, 
                        village_hep,
                        census_hep,
                        habitat_hep):
        """
        [Habitat, Existing, Proposed]
        Habitat detail list
        1. Equal items
        
        """
        if(not
           fn.reduce(lambda el, res: el == slno_hep[0], slno_hep, True)):
            return False, 'Serial number should match!'
        
        if(not
           fn.reduce(lambda el, res: el == village_hep[0], village_hep, True)):
            return False, 'Village name should match'
        
        if(not
           fn.reduce(lambda el, res: el == census_hep[0], census_hep, True)):
            return False, 'Census code should match'

        if(not
           fn.reduce(lambda el, res: el == habitat_hep[0], habitat_hep, True)):
            return False, 'Habitat name should match'        
        return True, 'OK'
    
        
    def check_select_value(main_habitat,category, status, mode):
        if(not
           main_habitat in ('Yes', 'No')):
            return False, 'Main habitation column should be Yes or No'
        if(not
           category in ('I', 'II', 'III')):
            return False, 'Category should be I, II, or III'
        
        STATUS = ('Electrified through grid', 'Un-electrified', 'Electrified through off-grid', 'Uninhabited')
        if(not
           status in STATUS):
            return False, 'Status should be one of {}'.format(STATUS)
        
        return True, 'OK'

    def infra_and_category(category, status, hh, hh_ele, hh_bal, mode,infra_exi, infra_pro):
        
        """
        [Habitat, Existing, Proposed]
        [Category]
        I. No Infra Required (Just connections): 
            Status should be electrified through grid
            if hh is given
            None zero electrified HH
            Existing infra should be given
            No proposed infra should be given
        II. Significant infra required:
            Status should be unelectrified
            Electrified should be zero
            balance hh = total hh
            proposed infra should be given
        III. Mixed:
            Status should be electrified through grid
            None zero electrified HH
            Existing infra should be given
            proposed infra should be given
        """
        if(category == "I"):
            if(not
               status == "Electrified through grid"):
                return False, 'Habitat should be Electrified through grid for No infra required (I)'
            if(int(hh) > 0):
                if(not
                   hh_ele > 0):
                    return False, 'Electrified habitat should have electrified households'
                if(not
                   hh_bal > 0):
                    return False, 'Balance HH not proposed'
                if(not
                   infra_exi > 0):
                    return False, 'Electrified habitat should have existing infrastructures'
                if(infra_pro > 0):
                    return False, 'No infra required := No infra proposal'
                if(not 
                   mode == 'Grid'):
                    return False, 'Mode of electrification should be Grid for category I'
        if(category == 'II'):
            if(not
               status == 'Un-electrified'):
                return False, 'Significant infra is required only for Un-electrified habitats'
            if(hh_ele > 0):
                return False, 'Un-electrified habitats cannot have electrified households'
            if(not
               hh_bal == hh):
                return False, 'All households under Un-electrified habitats should be proposed'
            if(not
               infra_pro > 0):
                return False, 'Proposed infra not given'
            if(not
               hh_bal > 0):
                return False, 'Balance HH not proposed'
            if(not 
               mode == 'Grid'):
                return False, 'Mode of electrification should be Grid for category II'
            
        if(category == 'III'):
            if(not
               status == "Electrified through grid"):
                return False, 'Habitat should be Electrified through grid for category III'
            if(not
               hh_ele > 0):
                return False, 'Electrified habitat should have a min electrified households'
            if(not
               infra_exi > 0):
                return False, 'Electrified habitat should have existing infrastructures'
            if(not
               infra_pro > 0):
                return False, 'Proposed infra not given'
            if(not
               hh_bal > 0):
                return False, 'Balance HH not proposed'

        if(mode == 'Off-Grid'):
            if(not
               hh_bal > 0):
                return False, 'Balance HH not proposed'
            
        return True, 'OK'
            
        
        
        
        
        
        
        
        
        