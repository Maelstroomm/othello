# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 12:54:47 2023

@author: alois
"""


import random
from variablesGlobales import VIDE,NOIR,BLANC,BORD


def IA_Alea (coordCoupsPossibles):
    
    taille = len (coordCoupsPossibles)
    coorAlea = random.randint(0,taille-1)
    return (coordCoupsPossibles[coorAlea])
    
    
