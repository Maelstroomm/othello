# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:37:51 2023

@author: alois
"""

import numpy as np
from variablesGlobales import VIDE,NOIR,BLANC,BORD


def initialiserGrille():
    """
    A est le tableau de 8*8 que que l'on utilise en début de partie avec 2 pions
    de chaque couleur en diagonale au centre du plateau'

    Returns
    -------
    A : Tableau
    """

    A = np.array([[BORD, BORD, BORD, BORD ,BORD, BORD, BORD, BORD, BORD, BORD],
                [BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, BLANC, NOIR, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, NOIR, BLANC, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
             	[BORD,VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, BORD],
                [BORD,BORD,BORD,BORD,BORD,BORD,BORD,BORD, BORD, BORD]])
    


    return A

      

def afficherGrille (grille):
    
    """
    permet l'affichage du tableau créé ci dessus sous la forme d'un cadrillage avec les valeurs 0,1 ou 2 pour signifier 
    de quelle culeur est la case
    
    le contour de 9 permet justement de délimiter la grille de manière plus précise sans avoir à devoir gérer les indices
    
    """
	
    print("     k     a     b     c     d     e     f     g     h     m")
    
    for i in range(len(grille)):
        print("	    |     |     |     |     |     |     |     |     |")
        print(i,"  " ,grille[i][0], " | ",grille[i][1], " | ", grille[i][2], " | ",grille[i][3], " | ",grille[i][4], " | ",
              grille[i][5], " | ",grille[i][6], " | ",grille[i][7], " | ", grille[i][8], " | ", grille[i][9])
        if i!=9:
            print("   _____|_____|_____|_____|_____|_____|_____|_____|_____|_____")
        else:
            print("	    |     |     |     |     |     |     |     |     |")
