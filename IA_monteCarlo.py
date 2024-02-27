# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:50:35 2023

@author: Mael
"""
import numpy as np
import gestion_des_coups as g
import IA_aleatoire as a
import Victoire as v
import time

def monteCarlo(grille : np.array,joueur,score :list,nbrePartie:int=100)->tuple:
    """
    Fonction qui renvoie le meilleur coup a jouer grace à la methode probabiliste de monte carlo
    Pour chaque coup possibles dans la grille actuelle, la fonction simule le deroulement d'un nombre n de partie pour chaque coup.
    Au final le coup qui a permis à l'ia de gagner le plus de fois est retourne et c'est le meilleur coup
    
    
    Parameters
    ----------
    grille : np.array
        plateau de jeu actuel
    joueur : TYPE
        joueur qui doit jouer
    score : list
    nbrePartie : int, default  is 100
        nombre de partie que l'ia va simuler pour chacun des coups possibles

    Returns
    -------
    tuple du meilleur coup a jouer

    """
    
    
    
    #calculer les coups possibles
    coupsPossibles=g.calculCoupAutorise(grille, joueur)
    
    maxi=float('-inf')
    meilleurCoup=None
    #parcours de tous les coups possibles
    for coup in coupsPossibles:
        now=time.time()
        copieGrille=grille.copy()   #vraie copie du plateau actuel
        nouveauScore=score[:]       #vraie copie du score actuel
        
        #jouer des parties aleatoires        
        perform=partieAleatoire(copieGrille,joueur,nouveauScore,coup,nbrePartie) #liste des gagnants pour ce coup#si perform >0 l'ia à plus gagnee si perform <0 elle a plus perdu
        
        #sauvegarder les performance de l'ia si elles sont meilleures
        if perform >maxi:
            maxi=perform
            meilleurCoup=coup[0]
        #print("coup :",coup[0], "; performance :",perform , "; temps :",time.time()-now)

    #print("coup chosis :", meilleurCoup,maxi)
    return meilleurCoup



def partieAleatoire(grilleinitiale:np.array,joueur, score:list, coup:tuple,nbrePartie:int)->int:
    """
    Fonction qui simule un nombre 'nbrePartie' de partie aleatoires en jouant le coup 'coup' en premier
    
    
    
    Parameters
    ----------
    grilleinitiale : np.array
        grille de depart
    joueur : TYPE
        joueur qui doit jouer en premier
    score : list
    coup : tuple
        coord du premier coup a jouer
    nbrePartie : int
        nombre de parties aleatoires a simuler

    Returns
    -------
    performanceIA : int
        difference entre le nombre de partie gagne par l'ia comparer a son adversaire

    """
    #nombre de partie deja simulees
    partie=0
    
    
    joueurInitial=joueur
    
    #placement du premier pion impose
    g.placerPion(grilleinitiale,joueur,coup[0],score)
    coordPionARetourner=coup[1]#recuperation des coordonnes des pions a retourné en lien avec le coup effectué
    g.retournerPion(grilleinitiale, joueur, coordPionARetourner, score)#retourner les pions 
   
    
    joueur=g.joueurAdverse(joueur)  #changement de joueur
    
    coupsPossiblesPrecedant=[coup]
    
    performanceIa=0
    while partie < nbrePartie:
        #print(partie)
        finPartie=False
        grille=grilleinitiale.copy()
        
        now=time.time()
        #simulation d'une partie
        while finPartie == False:
            
            #calcul des coups autorises
            coupsPossibles=g.calculCoupAutorise(grille, joueur)
            
            #création d'une liste avec uniquement les tuples des coordonnées des coups possibles
            coordCoupsPossibles=[]
            for liste in coupsPossibles:
                coordCoupsPossibles.append(liste[0])
            
            
            #choix d'un coup aleatoirement
            if coordCoupsPossibles != []:
                
                coordCoup=a.IA_Alea (coordCoupsPossibles)
                
                #placer et retourner les pions
                g.placerPion(grille,joueur,coordCoup,score)
                coordPionARetourner=coupsPossibles[coordCoupsPossibles.index(coordCoup)][1]#recuperation des coordonnes des pions a retourné en lien avec le coup effectué
                g.retournerPion(grille, joueur, coordPionARetourner, score)#retourner les pions 
            
        
        
            finPartie=v.finPartieMinMax(score,True,coupsPossiblesPrecedant,coupsPossibles)
            coupsPossiblesPrecedant=coupsPossibles[:]
            joueur=g.joueurAdverse(joueur)    
        #print("partie",partie, "; temps :", round(time.time()-now,3), "s ; gagnant :", finPartie)    
        if finPartie == joueurInitial:
            performanceIa+=1
        elif finPartie == g.joueurAdverse(joueurInitial):
            performanceIa-=1
        
        partie+=1
        
    #print("Performance Ia : " ,performanceIa)
    return performanceIa
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        