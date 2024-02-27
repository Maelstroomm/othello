# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 11:15:01 2023

@author: Mael
"""
import Creation_grille_et_affichage as c
import gestion_des_coups as g
import Victoire as v
import utilisateur_console as u
import evaluationsMinMax as e
import numpy as np
from math import inf
from variablesGlobales import VIDE,NOIR,BLANC,BORD,HUMAIN,IA_MINMAX

def remplirPlateauFils(grille:np.array, coupsPossibles:list,score:list, joueur)->list:
    """
    Pour une grille donne, renvoie une liste de toutes les grille fils 
    (cad une liste de grille avec un coup en plus, avec tous les coups possibles)

    Parameters
    ----------
    grille : np.array
        grille a la situation initiale (racine)
    coupsPossibles :list : liste de listes contenant tous les coups possibles ainsi que les pions a retourner si on joue le coup associe
    score : list : score associee a la grille initiale (racine)
    joueur :  pour savoir qui joue et quelle couleur de pion ajouter a la grille

    Returns
    -------
    listeFils : list
        liste de liste : liste tous les coup possibles au tour suivant
    listeIndices : list
       liste de coordonnees (ligne, colone) des emplacements joués au tour suivant
    listeScores :list :liste des scores (scoreBlanc, scoreNoir) associe au coup joue

    """
    
    listeFils=[]            #liste qui va contenir l'ensemble des grilles possibles apres avoir jouer 1 coup
    listeIndices=[]         #liste qui va contenir l'ensemble des coordonnees (ligne, colone)des emplacements joués apres avoir jouer 1 coup
    listeScores=[]           #liste qui va contenir l'ensemble des scores [scoreblanc, scoreNoir] de tous les coupspossibles apres avoir jouer 1 coup
    
    for coup in coupsPossibles:
        #on fait une vrai copie de la grille
        nouveauFils=grille.copy()
        #on fait une vrai copie de la liste des scores
        nouveauScore=score[:]
        
        coordcoup=coup[0]
        pionsARetourner=coup[1]
        
        #placement du pion  
        g.placerPion(nouveauFils,joueur,coordcoup,nouveauScore)
        
        #retourner tous les pion a retourner
        g.retournerPion(nouveauFils, joueur, pionsARetourner, nouveauScore)#retourner les pions 

                
        listeFils.append(nouveauFils)   #on ajoute cette grille posible a la liste des grilles possibles
        listeIndices.append((coordcoup[0],coordcoup[1]))      #on ajoute les coodronnees du coup joue a la liste des indices
        listeScores.append(nouveauScore)
        nouveauFils=[]  
    

    return listeFils, listeIndices, listeScores


def negaMax(grille:np.array, evalMax: bool, joueur,score :list, profondeurMax:int, profondeur:int=0, coupsPossiblesPrecedant:list=[],alpha=float('-inf'),beta=float('inf')):
    """
    Version plus compacte qui execute l'algo min max avec coupure alpha beta
    fonction recursive
    Renvoie le meilleur coup a jouer

    Parameters
    ----------
    grille : np.array
        plateau de depart
    evalMax : bool
        =True si noeud max ; =False si noeud min
    joueur : TYPE
        joueur pour qui on applle initilament le negamax : donc joueur est tout le temps une IA
    score : list
    profondeurMax : int
        nombre de coup maximal que l'on va anticiper'
    profondeur : int, optional
        Profondeur actuelle dans l'abre des possibilites. The default is 0.
    coupsPossiblesPrecedant : list, optional
        DESCRIPTION. The default is [].
    alpha : TYPE, optional
        DESCRIPTION. The default is float('-inf').
    beta : TYPE, optional
        DESCRIPTION. The default is float('inf').

    Returns
    -------
    value : int
        evaluation du meilleur coup a jouer
    indicesFils[indice] :tuple
         tuple de coordonnees du meilleur coup a jouer

    """
    
    #Cas d'arret
    if profondeur>=profondeurMax :
        #print(grille)
        if joueur == NOIR :
            #print("evaluation : ",grille,e.evaluation2(grille, score,joueur))
            retour= ( e.evaluation2(grille, score,joueur),None)
        elif joueur == BLANC :
            #print("evaluation : ",grille,-e.evaluation2(grille, score,joueur))
            retour = (- e.evaluation2(grille, score,joueur),None)
        
        if evalMax:
            return (retour[0],retour[1])
        else :
            return (-retour[0],retour[1])
    else: 
        #print("Néga max profondeur: ", profondeur, alpha, beta )
        #calcul des coups possibles
        if evalMax:
            coupsPossibles=g.calculCoupAutorise(grille, joueur)
        else:
            coupsPossibles=g.calculCoupAutorise(grille, g.joueurAdverse(joueur))
        
        #Fin de partie : cas d'arret
        finPartie=v.finPartieMinMax(score,True, coupsPossiblesPrecedant, coupsPossibles)
        if finPartie!=False:
            return e.retournerEvaluationFinPartie(finPartie,joueur)
                
        #cas recursif  
        else:
            if evalMax:
                
                result=remplirPlateauFils(grille, coupsPossibles,score, joueur)# fonction qui va renvoyer toutes les possibilité pour le prochain coup et une liste d'indice
      
            else:
                result=remplirPlateauFils(grille, coupsPossibles,score, g.joueurAdverse(joueur))
            
            plateauxFils=result[0]
            indicesFils=result[1]
            scoresFils=result[2]
            
            
            #si aucun coup n'est possible : 
            if coupsPossibles==[]:
                #print("ia bloque")
                plateauxFils.append(grille) #le seul fils est la grille en cours
                indicesFils.append((None,None)) #avec aucun coup jouer
                scoresFils.append(score[:])#et le même score que celui actuel
            
            #print(len(plateauxFils), "noeuds")
            value=-inf
            listeValues=[]
            for i in range(len(plateauxFils)):
                nega=-negaMax(plateauxFils[i], not evalMax, joueur, scoresFils[i], profondeurMax,profondeur+1,coupsPossibles,-beta,-alpha)[0]
                #print(profondeur,"évaluation noeud", i ,":",nega, ", coup : ", indicesFils[i])
                value=max(value, nega)
                alpha = max(alpha, value)
                #print(value, alpha, beta)
                listeValues.append(value)
                
                if alpha >=beta:
                    #print("coupure")
                    break
        
        indice=listeValues.index(value)
        return value, indicesFils[indice]
                
                
                
                
                
                
                
                
                
                
    
    
