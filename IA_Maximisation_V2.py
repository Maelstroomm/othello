# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 19:31:31 2023

@author: alois
"""

import random
import numpy as np
from variablesGlobales import VIDE,NOIR,BLANC,BORD



def IA_Maxi (coupsPossibles):
    

    m=0     ##variable qui nous permet d'obtenir le max de pions que l'on peut retourner
    taille = len (coupsPossibles)
    liste = []
    listetriee = []
    
    for i in range (taille):
            liste.append([i,len(coupsPossibles[i][1])])
            
    for j in range (len(liste)):
        if (liste[j][1]) >= m:
            m = liste[j][1]
        
    A = np.array (liste)
    
    for k in range (len(liste)-1):    
        listetriee.append (np.where (A[k][1]==m))
        
    
    b = random.randint (0,len(listetriee))
        
        
    return coupsPossibles[b][0]
    

"""
def IA_MaxiSimple (coupsPossibles):
    
    b = random.randint(0,1)
    m=0     ##variable qui nous permet d'obtenir le max de pions que l'on peut retourner
    a=0     ##variable qui nous permet d'obtenir les coordonnées ou le nombre de pions que l'on peut retourner ets maximal
    taille = len (coupsPossibles)
    
    
    for i in range (taille):
        if b == 0 :
            if len (coupsPossibles[i][1]) >= m :
                m=len(coupsPossibles[i][1])
                a=i
        else :
            if len (coupsPossibles[i][1]) > m :
                m=len(coupsPossibles[i][1])
                a=i
            
        
    return coupsPossibles[a][0]
"""