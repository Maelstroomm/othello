# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 20:20:30 2023

@author: Mael
"""
import Creation_grille_et_affichage as c
import gestion_des_coups as g
import utilisateur_console as u
import Victoire as v
import IA_aleatoire as a
import IA_Maximisation_V2 as x
import IA_MinMax as m
import IA_MinMaxAlphaBeta as b 
import IA_NegaMax as n
import IA_monteCarlo as o
import time
from variablesGlobales import VIDE,NOIR,BLANC,BORD,HUMAIN,IA_ALEA,IA_MAXIMISATION,IA_MINMAX,IA_MINMAXALPHABETA,IA_MONTECARLO


def jouer(typeJoueur1:int,typeJoueur2:int):
    #initialisation de la grille
    grille= c.initialiserGrille()
    #c.afficherGrille(grille)
    print(grille,typeJoueur1,typeJoueur2)
    
    dicoJoueurs={NOIR:typeJoueur1,BLANC:typeJoueur2}
    
    
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
            
            #####Disjonction de cas en fonction du type de joueur qui doit jouer
            
            #si c'est à un humain de jouer
            if dicoJoueurs[joueur]==HUMAIN:
                coordCoup=u.demandeCoordUtilisateur(joueur)
                
                while coordCoup not in coordCoupsPossibles:
                    print("Ce coup n'est pas possible. Merci d'entrer de nouvelles coordonnées.")
                    coordCoup=u.demandeCoordUtilisateur(joueur)
            
            #si c'est à l'IA aleatoire de jouer
            elif dicoJoueurs[joueur]==IA_ALEA:
                coordCoup=a.IA_Alea (coordCoupsPossibles)
            
            #si c'est à l'IA de maximisation de jouer
            elif dicoJoueurs[joueur]==IA_MAXIMISATION:
                coordCoup=x.IA_Maxi (coupsPossibles)
            
            #si c'est à l'IA MinMax de jouer
            elif dicoJoueurs[joueur]==IA_MINMAX:
                profondeurMaxi=3
                coordCoup=m.MinMax(grille,True, joueur, score,profondeurMaxi)[1]
            
            #si c'est à l'IA MinMaxAlphaBeta de jouer
            elif dicoJoueurs[joueur]==IA_MINMAXALPHABETA:
                profondeurMaxi=1
                #now=time.time()
                coordCoup=b.MinMaxAlphaBeta(grille,True, joueur, score,profondeurMaxi)[1]  
                
                print("MinMax alpha beta : ", coordCoup)#, time.time()-now)
                
                
                
                #print(time.time()-now)
                #now=time.time()
                coordCoup=m.MinMax(grille,True, joueur, score,profondeurMaxi)[1]
                #print(time.time()-now)
                
                print("MinMax: ", coordCoup)#, time.time()-now)
                
                coordCoup=n.negaMax(grille,True, joueur, score,profondeurMaxi)[1]  
                print("NegaMax: ", coordCoup)
                
            #si c'est à l'IA monte carlo de jouer
            elif dicoJoueurs[joueur]==IA_MONTECARLO:
                now=time.time()
                nbrePartie=10#100+50*(score[0]+score[1])
                nbrePartie=profondeurIA(nbrePartie, score, IA_MONTECARLO)
                coordCoup=o.monteCarlo(grille, joueur, score,nbrePartie)
                print(coordCoup)
                print("Temps jeu Ia monteCarlo :", time.time()-now)
            #####
            
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
    
                

def main():
    listeIa=[IA_ALEA, IA_MAXIMISATION, IA_MINMAX,IA_MINMAXALPHABETA,IA_MONTECARLO] #type d'IA existantes
    print("Bonjour, \nVous voulez jouer à l'Othello. \nVoici les modes de jeu disponibles : ")
    print(" 1- joueur contre joueur")
    print(" 2- joueur contre IA aléatoire")
    print(" 3- joueur contre IA de maximisation")
    print(" 4- joueur contre IA MinMax")
    print(" 5- joueur contre IA MinMax alpha beta")
    print(" 6- joueur contre Montecarlo")
    print(" 7- IA contre IA")
    #demande du mode de jeu
    modeJeu=""
    while modeJeu not in ["1","2","3","4","5","6", "7"]:
        modeJeu=input("Veuillez entrer un mode de jeu (1,2,3,4,5, 6 ou 7) :")
    modeJeu=int(modeJeu)
    
    
    if modeJeu==1:
        jouer(HUMAIN,HUMAIN)
    
    elif modeJeu == 7:
        print("Mode IA contre IA. \nVoici les IA disponibles :")
        print(" 1- IA aléatoire")
        print(" 2- IA de maximisation")
        print(" 3- IA MinMax")
        print(" 4- IA MinMax coupure alpha beta")
        print(" 5- IA probabiliste Monte Carlo")
        difficulteIA1=""
        difficulteIA2=""
        while difficulteIA1 not in ["1","2","3","4","5"] or difficulteIA2 not in ["1","2","3","4","5"]:
            difficulteIA1=input("Veuillez entrer une difficulté  pour le première IA (1,2,3,4 ou 5) :")
            difficulteIA2=input("Veuillez entrer une difficulté  pour le deuxième IA (1,2,3,4 ou 5) :")
        difficulteIA1=int(difficulteIA1)
        difficulteIA2=int(difficulteIA2)
        jouer(listeIa[difficulteIA1-1],listeIa[difficulteIA2-1])
    
    else:
        print("Mode joueur contre IA")
        commencer=""
        while commencer not in ["OUI","NON"]:
            commencer=input("Voulez vous commencer ? (entrez oui/non) :").upper()
        if commencer =="OUI":
            jouer(HUMAIN,listeIa[modeJeu-2])
        if commencer =="NON":
            jouer(listeIa[modeJeu-2],HUMAIN)
            
def profondeurIA(profondeurBase:int, score:list,ia:int)->int:
    """
    Permet d'augmenter la profondeur en fin de partie

    Parameters
    ----------
    profondeurBase : int
        DESCRIPTION.
    score : list
        DESCRIPTION.

    Returns
    -------
    int
        DESCRIPTION.

    """
    numeroCoup=score[0]+score[1]-4
    #print("numeroCoup :", numeroCoup)
    if ia== IA_MINMAXALPHABETA and numeroCoup >= 47:
        #print(64-numeroCoup)
        return 64-numeroCoup
    elif ia== IA_MINMAX and numeroCoup >= 54:
        #print(64-numeroCoup)
        return 64-numeroCoup
    elif ia ==IA_MONTECARLO and numeroCoup >= 40:
        return profondeurBase*5
    else:
        return profondeurBase


def jouerTestIA(typeJoueur1:int,typeJoueur2:int,nbre):
    partie=0
    gagnant=[]
    
    dicoJoueurs={NOIR:typeJoueur1,BLANC:typeJoueur2}
    print("Noir : ", typeJoueur1, "; Blanc :",typeJoueur2)
    
    
    while partie < nbre:
        #initialisation de la grille
        grille= c.initialiserGrille()
        #c.afficherGrille(grille)
        #print(grille)
        
        
        
        
        #premier joueur
        joueur=NOIR 
        
        #variable qui va stocker les coup possible pour le joueur d'avant
        coupsPossiblesPrecedant=[0]
        
        
        score=[2,2]
        
        VarFinPartie=False
        while VarFinPartie == False :
            coupsPossibles=g.calculCoupAutorise(grille, joueur)
            if coupsPossibles==[]:#si le joueur doit passer
                #print(joueur ," ne peut pas jouer et passe son tour")
                pass
            else:
                #création d'une liste avec uniquement les tuples des coordonnées des coups possibles
                coordCoupsPossibles=[]
                for liste in coupsPossibles:
                    coordCoupsPossibles.append(liste[0])
                
                #####Disjonction de cas en fonction du type de joueur qui doit jouer
                
                #si c'est à un humain de jouer
                if dicoJoueurs[joueur]==HUMAIN:
                    coordCoup=u.demandeCoordUtilisateur(joueur)
                    
                    while coordCoup not in coordCoupsPossibles:
                        #print("Ce coup n'est pas possible. Merci d'entrer de nouvelles coordonnées.")
                        coordCoup=u.demandeCoordUtilisateur(joueur)
                
                #si c'est à l'IA aleatoire de jouer
                elif dicoJoueurs[joueur]==IA_ALEA:
                    coordCoup=a.IA_Alea (coordCoupsPossibles)
                
                #si c'est à l'IA de maximisation de jouer
                elif dicoJoueurs[joueur]==IA_MAXIMISATION:
                    coordCoup=x.IA_Maxi (coupsPossibles)
                
                
                
                
                #si c'est à l'IA MinMax de jouer
                elif dicoJoueurs[joueur]==IA_MINMAX:
                    profondeurMaxi=3
                    profondeurMaxi=profondeurIA(profondeurMaxi,score,IA_MINMAX)
                    coordCoup=m.MinMax(grille,True, joueur, score,profondeurMaxi)[1]
                
                #si c'est à l'IA MinMaxAlphaBeta de jouer
                elif dicoJoueurs[joueur]==IA_MINMAXALPHABETA:
                    profondeurMaxi=5
                    profondeurMaxi=profondeurIA(profondeurMaxi,score,IA_MINMAXALPHABETA)
                    coordCoup=b.MinMaxAlphaBeta(grille,True, joueur, score,profondeurMaxi)[1] 
                    #coordCoup=n.negaMax(grille,True, joueur, score,profondeurMaxi)[1]  
                    #print("NegaMax: ", coordCoup)
                
                #si c'est à l'IA monte carlo de jouer
                elif dicoJoueurs[joueur]==IA_MONTECARLO:
                    nbrePartie=20#+50*(score[0]+score[1])
                    coordCoup=o.monteCarlo(grille, joueur, score,nbrePartie)
                    print(coordCoup)
                #####
                
                #mise a jour de la grille
                g.placerPion(grille,joueur,coordCoup,score) #permet de placer le pion 
                
                coordPionARetourner=coupsPossibles[coordCoupsPossibles.index(coordCoup)][1]#recuperation des coordonnes des pions a retourné en lien avec le coup effectué
                g.retournerPion(grille, joueur, coordPionARetourner, score)#retourner les pions 
                #c.afficherGrille(grille)
                #print(grille)
            
        
            
            #fin de partie ? 
            VarFinPartie=v.finPartie(score,coupsPossiblesPrecedant,coupsPossibles)
            coupsPossiblesPrecedant=coupsPossibles[:]
            #print("Score : " , score)
            joueur=g.joueurAdverse(joueur)    
    
        gagnant.append(VarFinPartie)
        
        partie+=1
    print(gagnant)
    cptNoir=0
    cptBlanc=0
    for i in range(len(gagnant)):
        if gagnant[i]==NOIR: 
            cptNoir+=1
        elif gagnant[i]==BLANC: 
            cptBlanc+=1
    print("Le joueur noir a gagner : ", cptNoir)
    print("Le joueur blanc a gagner : ", cptBlanc)
    
        
    

#main()  

now=time.time()
jouerTestIA(IA_ALEA,IA_ALEA,100)#IA_MINMAX)
print("temps : ", time.time()-now)

