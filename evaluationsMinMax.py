# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 14:30:32 2023

@author: Mael
"""
import numpy as np
from math import inf
import Victoire as v
from variablesGlobales import BLANC,NOIR,BORD,VIDE

A = np.array([[BORD, BORD, BORD, BORD ,BORD, BORD, BORD, BORD, BORD, BORD],
            [BORD,NOIR, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, BLANC, NOIR, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, NOIR, BLANC, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
         	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BLANC, VIDE, BORD],
            [BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD, BORD, BORD]])

listePoidCase=[[BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD],
               [BORD, 5000, -250,30,10,10,30, -250,  5000, BORD],
               [BORD,-250, -250, 0, 0, 0, 0, -250, -250, BORD],
               [BORD,  30,    0, 1, 2, 2, 1 ,   0,   30, BORD],
               [BORD,  10,    0, 2,16,16, 2,    0,   10, BORD],
               [BORD,  10,    0, 2,16,16, 2,    0,   10, BORD],
               [BORD,  30,    0, 1, 2, 2, 1 ,   0,   30, BORD],
               [BORD,-250, -250, 0, 0, 0, 0, -250, -250, BORD],
               [BORD, 5000, -250,30,10,10,30, -250,  5000, BORD],
               [BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD]]

def evaluation1(grille:np.array, score:list,joueur):
    #print(score[joueur-1])
    return score[joueur-1]



def evaluation2(grille:np.array, score:list,joueur):
    placement=evalPlacement(grille, listePoidCase)
    materiel=evalMateriel(score)
    victoire= evalFinPartie(score)
    #print(placement,materiel,victoire)
    evaluation=placement+materiel+victoire
    #print(grille,evaluation )


    return evaluation


def evalMateriel (score:list):
    """
    est mesurée par le nombre de pions d’une couleur donnée
    renvoi la difference entre le nombre de pion noir et de pion blanc:
    
    si le renvoie est > 0 noir a plus de pion que blanc
    """
    return score[1]-score[0]


def evalPlacement(grille,listePoidCase:list):
    Copie = listePoidCase.copy()
    valeurPlacement=0
    
    #jouer près des coins est avantageux si le coin est prit
    if grille [1][1] != VIDE :
        Copie[1][2] , Copie[2][1] = 1000,1000
        
    if grille [1][8] != VIDE : 
        Copie[1][7] , Copie[2][8] = 1000,1000
        
    if grille [8][1] != VIDE :
        Copie[7][1] , Copie[8][2] = 1000,1000
        
    if grille [8][8] != VIDE : 
        Copie[8][7] , Copie[7][8] = 1000,1000
        
        
    #jouer sur les bordures est avantageux   
    if grille [1][1] != VIDE and grille [1][2] != VIDE :
        Copie [1][3] = 500
        
    if grille [1][1] != VIDE and grille [2][1] != VIDE :
        Copie [3][1] = 500
        
    if grille [1][8] != VIDE and grille [1][7] != VIDE :
        Copie [1][6] = 500 
    
    if grille [1][8] != VIDE and grille [2][8] != VIDE :
        Copie [3][8] = 500
        
    if grille [8][1] != VIDE and grille [7][1] != VIDE :
        Copie [6][1] = 500   
        
    if grille [8][1] != VIDE and grille [8][2] != VIDE :
        Copie [8][3] = 500    
    
    if grille [8][8] != VIDE and grille [8][7] != VIDE :
        Copie [8][6] = 500 
        
    if grille [8][8] != VIDE and grille [7][8] != VIDE :
        Copie [6][8] = 500 
        
        
    for i in range(1,len(grille)-1):
        for j in range(1,len(grille)-1):
            if grille[i][j]==NOIR:
                valeurPlacement += Copie[i][j]
            elif grille[i][j]== BLANC:
                valeurPlacement -= Copie[i][j]
                
    return valeurPlacement
    


def evalFinPartie(score:list):
    finPartie=v.finPartieMinMax(score,False)
    if finPartie == NOIR:
        return +inf
    elif finPartie == BLANC:
        return-inf
    else:
        return 0


def retournerEvaluationFinPartie(gagnant,joueur):
    
    if gagnant == BLANC:
        if joueur==BLANC:
            return (+inf,None)
        else:
            return (-inf,None)
    elif gagnant == NOIR:
        if joueur==NOIR:
            return (+inf,None)
        else:
            return (-inf,None)
    
    elif gagnant== "exaequo":
        return (0,None)