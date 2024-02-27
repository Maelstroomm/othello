# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 18:43:47 2023

@author: Mael
"""
from variablesGlobales import VIDE,NOIR,BLANC,BORD

def gestionSaisieUtilisateur(s:str)->tuple:
    """
    renvoye un tuple les coordonnees de la case a jouer a partir d'une chaine de caractere s : saisie du joueur

    Parameters
    ----------
    s : str
        saisie de l'utilisateur.

    Returns
    -------
    tuple
        coordonnee (ligne,colone) du coup que veut le joueur
    ou 
    bool
        False si la saisie n'est pas valide

    """
    ligne, colone= 0,0
    s=s.upper()                 #mise en majuscule de la saisie pour eliminer les difference de casse
    lettres=["A","B","C","D","E","F","G","H"]       #possibilitees pour les lettres
    chifres=["1","2","3","4","5","6","7","8"]       #possibilitees pour les chiffres
    nbrLettre, nbrChiffre= 0,0  #compteurs
    for car in s:               #parcours de tous les caracteres de la saisie
        if car.isalpha() and car in lettres:
            nbrLettre+=1
            colone=lettres.index(car)+1   #on recupere l'indice qui correspond a l'indice de la colone choisi
        elif car.isdecimal() and car in chifres:
            nbrChiffre+=1               #on recupere l'indice qui correspond a l'indice de la ligne choisi
            ligne=chifres.index(car)+1

    #Si il n'y a qu'une seule lettre et qu'un seul chiffre, la saisie est valide
    if nbrChiffre == 1 and nbrLettre == 1:
        return ligne, colone
    else:           #sinon erreur de saisie
        print("Erreur de saisie, réessayez !!")
        return False
        
    
    return(ligne,colone)

def demandeCoordUtilisateur(joueur)->tuple:
    """
    Permet la saisie de coordonnees par l'utilisateur 
    Gere les erreur de saisie

    Parameters
    ----------
    joueur 

    Returns
    -------
    result : tuple : (ligne,colonne) coordonees du coup voulu par l'utilisateur

    """
    result=False
    #annocer le joueur qui doit jouer
    if joueur == NOIR:
        print("Joueur noir.")
    elif joueur == BLANC:
        print("Joueur blanc :")
    while not result :
                saisie=input("Entrez les coordonées de la case à jouer : ")
                result=gestionSaisieUtilisateur(saisie)
    return result





    