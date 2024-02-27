# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 08:45:16 2023

@author: Mael
"""
import Creation_grille_et_affichage as c
import gestion_des_coups as g
import Victoire as v
import utilisateur_console as u
import evaluationsMinMax as e
import numpy as np
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




def MinMax(grille:np.array, evalMax: bool, joueur,score :list, profondeurMax:int, profondeur:int=0, indicesFils:list=[], coupsPossiblesPrecedant:list=[]):
    """
    Fonction recursive qui revoie le gain et les coordonnees du coup que doit jouer l'IA pour essayer de gagner

    Parameters
    ----------
    grille : list
        grille du jeu
    evalMax : bool
        True si c'est a l'IA de jouer : on maximise les gains
        False si c'est a l'humain de jouer: on minimise les gains
    joueur 
    score : list : score (s)
    profondeurMax : int :  nombre d'appel recursif maximum : correspond au nombre max de coups a anticiper
    profondeur : int,  optional
        DESCRIPTION. The default is 0. nombre d'appel recursif (=nombre de coups a anticipe) deja effectue 
    indicesFils : list, optional
        DESCRIPTION. The default is [].

    Returns
    -------
    TYPE
        DESCRIPTION.
    TYPE
        DESCRIPTION.

    """
    #Cas d'arret
    if profondeur>=profondeurMax :
        #print("evaluation : ",e.evaluation2(grille, score,joueur))
        if joueur == NOIR :
            #print("evaluation : ",grille,e.evaluation2(grille, score,joueur))
            return ( e.evaluation2(grille, score,joueur),None)
        elif joueur == BLANC :
            #print("evaluation : ",grille,-e.evaluation2(grille, score,joueur))
            return (- e.evaluation2(grille, score,joueur),None)

    
    else: 
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
            
            gainsDesFils=[]
            #print(plateauxFils,scoresFils)
            #on rappelle MinMax() si tous les plateaux fils en changeant evalMax (car on change de joueur)                
            for i in range(len(plateauxFils)):
                gainsDesFils.append(MinMax(plateauxFils[i], not evalMax, joueur, scoresFils[i], profondeurMax,profondeur+1,coupsPossibles)[0])

            if evalMax :
                maxi=max(gainsDesFils)  
                return maxi, indicesFils[gainsDesFils.index(maxi)]  #on renvoie le gain max de tous les coups fils ainsi que les coordonees qui lui correspondes
            else:
                mini=min(gainsDesFils)
                return mini, indicesFils[gainsDesFils.index(mini)] #on renvoie le gain min de tous les coups fils ainsi que les coordonees qui lui correspondes
            


def jouer(typeJoueur1,typeJoueur2):
    #initialisation de la grille
    grille= c.initialiserGrille()
    c.afficherGrille(grille)
    
    
    dicoJoueurs={NOIR:typeJoueur1,BLANC:typeJoueur2}
    #associationJoueur1=(NOIR, typeJoueur1)
    #associationJoueur2=(BLANC, typeJoueur2)

    #premier joueur
    joueur=NOIR 
    
    #variable qui va stocker les coup possible pour le joueur d'avant
    coupsPossiblesPrecedant=[0]
    
    
    score=[2,2]
    
    VarFinPartie=False
    while VarFinPartie == False :
        coupsPossibles=g.calculCoupAutorise(grille, joueur)
        if coupsPossibles==[]:#si le joueur doit passer
            print(joueur ," ne peut pas jouer et passe son tour")    
        else:
            #création d'une liste avec uniquement les tuples des coordonnées des coups possibles
            coordCoupsPossibles=[]
            
            for liste in coupsPossibles:
                coordCoupsPossibles.append(liste[0])

            if dicoJoueurs[joueur]==HUMAIN:
                coordCoup=u.demandeCoordUtilisateur(joueur)
                
                while coordCoup not in coordCoupsPossibles:
                    print("Ce coup n'est pas possible. Merci d'entrer de nouvelles coordonnées.")
                    coordCoup=u.demandeCoordUtilisateur(joueur)
            elif dicoJoueurs[joueur]==IA_MINMAX:
                profondeurMaxi=4
                coordCoup=MinMax(grille,True, joueur, score,profondeurMaxi)[1]
            print(coordCoup)
            
            
            #mise a jour de la grille
            g.placerPion(grille,joueur,coordCoup,score) #permet de placer le pion 
            
            coordPionARetourner=coupsPossibles[coordCoupsPossibles.index(coordCoup)][1]#recuperation des coordonnes des pions a retourné en lien avec le coup effectué
            g.retournerPion(grille, joueur, coordPionARetourner, score)#retourner les pions 
            #c.afficherGrille(grille)
            print(grille)
            
       
            
        #fin de partie ? 
        VarFinPartie=v.finPartie(score,coupsPossiblesPrecedant,coupsPossibles)
        coupsPossiblesPrecedant=coupsPossibles[:]
        print("Score : " , score)
        joueur=g.joueurAdverse(joueur)
                


#jouer(IA_MINMAX,IA_MINMAX)  