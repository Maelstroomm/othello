# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:31:42 2023

@author: alois
"""
from variablesGlobales import VIDE,NOIR,BLANC,BORD

def finPartie (score :tuple,coupsPossiblesPrecedant:list,coupsPossibles:list): 
    """
    

    Parameters
    ----------
    score : tuple (scoreBlanc, scoreNoir)
    coupsPossiblesPrecedant : list : liste des coordonnées des coups possible pour le joueur d'avant
    coupsPossibles : list :  liste des coordonnées des coups possible pour le joueur actuel


    Returns
    -------
    la valeur du gangnant : si il y a un gagnant 
    False:  si il n'y a pas de gagnant  
    "exaequo" : si il y a exaequo
    """
    if score[0]+score[1]==64 or (coupsPossiblesPrecedant == [] and coupsPossibles== []):
        #print(score[0]+score[1])
        if score[0] > score [1]:
            print ("Le gagnant est le joueur blanc.")
            return BLANC
        elif score[0] == score[1]:
            print ("exaequo, aucun joueur n'a gagné.") 
            return "exaequo"
        else :
            print ("Le gagnant est le joueur noir.")
            return NOIR
     
        
    elif score [0]==0 :
        print ("Le gagnant est le joueur noir.")
        return NOIR
    
    elif score [1] == 0:
        print ("Le gagnant est le joueur blanc.")
        return BLANC
    return False




def finPartieMinMax (score :tuple,listeCoups:bool=False,coupsPossiblesPrecedant:list=[None],coupsPossibles:list=[None]): 
    """
    

    Parameters
    ----------
    score : tuple (scoreBlanc, scoreNoir)
    coupsPossiblesPrecedant : list : liste des coordonnées des coups possible pour le joueur d'avant
    coupsPossibles : list :  liste des coordonnées des coups possible pour le joueur actuel


    Returns
    -------
    la valeur du gangnant : si il y a un gagnant 
    False:  si il n'y a pas de gagnant  
    "exaequo" : si il y a exaequo
    """
    if score[0]+score[1]==64 or (listeCoups and coupsPossiblesPrecedant == [] and coupsPossibles== []):
        #print(score[0]+score[1])
        if score[0] > score [1]:
            return BLANC
        elif score[0] == score[1]:
            return "exaequo"
        else :
            return NOIR
      
    elif score [0]==0 :
        return NOIR
    
    elif score [1] == 0:
        return BLANC
    return False