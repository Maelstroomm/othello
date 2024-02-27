# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:05:39 2023

@author: Mael
"""
import numpy as np
from variablesGlobales import VIDE,NOIR,BLANC,BORD


def joueurAdverse(joueur:int)->int:
    """
    fonction qui renvoie le joueur adverse à celui passsé en argument

    Parameters
    ----------
    joueur : int
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    int
        DESCRIPTION.

    """
    if joueur == BLANC:
        return NOIR
    elif joueur == NOIR:
        return BLANC
    else:
        raise Exception("ERREUR ! fonction joueurAdvese() ne peut prendre en argument que BLANC (1) ou NOIR (2) ")




def  renvoiVosinAdverse(grille : np.array, joueur)->list:
    """
    Cette fonction  parcours toute la grille à la recherche des cases 
    qui remplissent ces 2 critères :
        - case VIDE
        - case qui à au moins un pion de la couleur opposée dans son voisinage
    Renvoie les cases qui satisfont ces 2 critères et renvoie aussi pour chaqune de ces case les coordonnées des pion adverses dans le voisinage
    
    Parameters
    ----------
    grille : tableau
        plateau de jeu
    joueur : TYPE
        joueur qui est en train de jouer : BLANC ou NOIR

    Returns
    -------
    casesPossibles : list
       liste de listes composées:  - d'un tuple de coordonnées (ligne,colonne) des cases vides qui ont au moins un pion de la couleur opposé dans leur voisinage (carré de 3*3 autour de la case).
                                   - d'une liste  de tuple avec les coordonnées des case adverses dans le voisinage
    """
    directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    casesPossibles=[]
    for i in range(1,np.shape(grille)[0]-1):        #parcourrs des lignes
        for j in range(1, np.shape(grille)[1]-1):   #parcourrs des colonnes
            if grille[i][j] == VIDE :               #case VIDE
                adversaireVoisin=[]

                for direction in directions:
                    if grille[i+direction[0]][j+direction[1]]==joueurAdverse(joueur):
                        adversaireVoisin.append((i+direction[0],j+direction[1]))
                if adversaireVoisin != []:
                    casesPossibles.append([(i,j),adversaireVoisin])
    return casesPossibles
                        

    
    
    
def pionARetourner(grille : np.array ,joueur, coordCase : tuple,listeVosins:list)->list:
    """
    fonction qui renvoie le

    Parameters
    ----------
    grille : np.array
        plateau de jeu.
    joueur : TYPE
        joueur en cours.
    coordCase : tuple
        coordonnees de la case initiale ou l'on veut savoir si jouer ici permet de retourner au moins un pion .
    listeVosins : list
        liste de tuple des coordonnees de tous les pions voisin adjacents.

    Returns
    -------
    list
        coordonnees des coups jouableset des pion a retourner. 
        #de la forme [[(ligne,colonne),[(ligne,colonne),...,(ligne,colonne)]],..., [(ligne,colonne),[(ligne,colonne),...,(ligne,colonne)]]]
    retourn [] si on ne peut retourner aucun pion

    """
    retournePion=[]
    #pour chaque pion adverse dans le voisinage de la case : 
    for coordVoisin in listeVosins:
        retournePionPotentiel=[]
        
        
        #calcul du "vecteur d'éplacement" permetant de se déplacer de la case initiale vers le pion adverse
        directionLigne=coordVoisin[0]-coordCase[0]
        directionColonne=coordVoisin[1]-coordCase[1]
        

        #coordonnées de la cese que l'on veut étudier
        ligne=coordCase[0]+directionLigne
        colonne=coordCase[1]+directionColonne
        
        continuer=True
        while grille[ligne][colonne] != BORD and continuer==True:       #tant que l'on a pas atteint le BORD
            if grille[ligne][colonne] == joueur:    #si le pion etudiee est celui du joueur
                #on valide les coordonnees des pion a retourner en les ajoutant à la liste des pions a retourner
                for i in range (len(retournePionPotentiel)):
                    retournePion.append(retournePionPotentiel[i])
                continuer=False
            elif grille[ligne][colonne] == joueurAdverse(joueur):   # #si le pion etudiee est celui du joueur adverse
                retournePionPotentiel.append((ligne,colonne))       #on ajoute ses coordonnées dans la liste 
                #deplacement dans le sens du vecteur deplacemnt vers la prochaine case
                ligne+=directionLigne               
                colonne+=directionColonne
            else:                                   #si on rencontre un case VIDE
                continuer= False                        #cela veut dire que l'on ne peut pas retourner de pion dans cette direction.
      
    return retournePion


def calculCoupAutorise(grille : np.array, joueur) -> list:
    """
    Fonction qui renvoie les coordonnées des cases où le joueur peut jouer 
    ainsi que les coordonnées des pions a retourner si il joue sur une de ces cases.

    Parameters
    ----------
    grille : np.array
        plateau de jeu
    joueur : TYPE
        joueur en cours

    Returns
    -------
    listeCasesPossibles : list
        Liste de liste qui contient autant d'élément que de coup possible
        Chaque liste contient deux éléments : 
            - un tuple qui contient les coordonnées d'une case d'un coup possible (ligne, colonne)
            - une liste de tuple : chaque tuple contient les coordonnées d'un pion a retourner si le joueur décide de joueur le coup associer

    """
    #retournes toutes les cases qui sont potentiellement joueable ainsi que les coordonnées des pions voisin adverse
    resultRenvoiVoisinAdverse=renvoiVosinAdverse(grille, joueur) #de la forme [[(ligne,colonne),[(ligne,colonne),...,(ligne,colonne)]],..., [(ligne,colonne),[(ligne,colonne),...,(ligne,colonne)]]]

    listeCasesPossibles=[]

    #parcours de toutes les coups potentiellement jouables
    for case in resultRenvoiVoisinAdverse:
        coordCase=case[0] #coordonnées de la case qui est potentiellement jouable
        listeVosins=case[1] #liste des tuples de coordonnées de tous les poins adverse dans le voisinage de la case
        
        #verification pour savoir si le coup permet de retourner au moins un pion
        resultPionARetourner=pionARetourner(grille,joueur, coordCase,listeVosins)
        if resultPionARetourner != [] :
            listeCasesPossibles.append([coordCase,resultPionARetourner])
        
    
    return listeCasesPossibles



def ajouterPointJoueur(joueur, valeurAAjouter:int, score:list):
    """
    Permet de mettre a jour les scores

    Parameters
    ----------
    joueur : TYPE
    valeurAAjouter : int : nombre de point a rajouter(si positif)/enlever(si négatif) au joueur
    score : list :liste des score [scoreBLANC, scoreNOIR]
    """
    if joueur==BLANC:
        score[0]+=valeurAAjouter
    elif joueur==NOIR:
        score[1]+=valeurAAjouter


def placerPion(grille: np.array, joueur,coordPion:tuple, score:list):
    """
    permet de placer un pion sur une case VIDE

    Parameters
    ----------
    grille : np.array
    joueur : TYPE
    coordPion : tuple : coordonnees de la case ou le pion doit être placé
    score : list : : liste des score [scoreBLANC, scoreNOIR]
    """
    grille[coordPion[0]][coordPion[1]]=joueur   #placement du pion
    ajouterPointJoueur(joueur, 1, score)        #mise a jour des score : +1point pour ce joueur
 

def retournerPion(grille: np.array, joueur,coordPion:list, score:list):
    """
    Fonction qui permet de retourner les un nombre de pion donné et d'actualiser les scores
    Parameters
    ----------
    grille : np.array
    joueur : TYPE
    coordPion : list : liste de tuple contenant les coordonnes des pions a retourner
    score : list : liste des score [scoreBLANC, scoreNOIR]
    """
    for pion in coordPion:  
        #pour chaque pion a retourner
        if grille[pion[0]][pion[1]] == BLANC:           #si le pion present est BLANC
            ajouterPointJoueur(BLANC, -1, score)     #-1 pour le BLANC
            ajouterPointJoueur(NOIR, 1, score)       #+1 pour le NOIR
        else:                                           #sinon, si le poin present est NOIR
            ajouterPointJoueur(BLANC, 1, score)
            ajouterPointJoueur(NOIR, -1, score)
        
        grille[pion[0]][pion[1]]=joueur                 #changement de couleur du pion : on le retourne
    