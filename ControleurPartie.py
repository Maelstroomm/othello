# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 14:59:55 2023

@author: Mael
"""
from variablesGlobales import VIDE,NOIR,BLANC,BORD,HUMAIN,IA_ALEA,IA_MAXIMISATION,IA_MINMAX,IA_MINMAXALPHABETA,IA_MONTECARLO
import gestion_des_coups as g
import Creation_grille_et_affichage as c
import IA_MinMax as m
import Victoire as v
import IA_aleatoire as a
import IA_Maximisation_V2 as x
import IA_NegaMax as n
import IA_monteCarlo as o
import time



class ControlePartie(): #objet qui va permettre de gerer toute la logique du jeu
    
    def __init__(self,othello,typeJoueur1,typeJoueur2, affichageIHM:bool=True): #constructeur qui prend en argument l'interface graphique associee
        #interface graphique    
        self.othello=othello        
        
        #premier joueur
        self.joueur=NOIR 
        
        self.dicoJoueurs={NOIR:typeJoueur1,BLANC:typeJoueur2}
        #variable qui va stocker les coup possible pour le joueur d'avant
        self.coupsPossiblesPrecedant=[0]
        self.afficherIHM=affichageIHM
        
        self.score=[2,2]
        
        self.varFinPartie=False
        self.grille= c.initialiserGrille()
        
    
    def initialisergrilleIHM(self):
        self.othello.afficherGrilleIHM(self.grille)
    
    def profondeurIA(self,profondeurBase:int,ia:int,coupsPossibles:list=[])->int:
        """
        Permet d'augmenter/diminuer la profondeur 
        en fonction de l'avancement de la partie et du nombre de possibilites de coups 
        
        Parameters
        ----------
        profondeurBase : int
            DESCRIPTION.
        ia: type d'ia
        coupsPossibles : list : liste des coups possibles
        Returns
        -------
        int
            DESCRIPTION.

        """
        numeroCoup=self.score[0]+self.score[1]-4
        
        
        if ia == IA_MINMAXALPHABETA:
            profondeur=profondeurBase-4
            if numeroCoup >=46:
                profondeur=64-numeroCoup
            elif numeroCoup >=39:
                profondeur+=2
            elif numeroCoup >=33:
                profondeur+=1
            
            if len(coupsPossibles)>=12:
                profondeur-+1
            elif len(coupsPossibles)<=8:
                profondeur+=1
            elif len(coupsPossibles)<=5:
                profondeur+=2
            
            #print("Profondeur : ",profondeur)
            return profondeur
        
        elif ia == IA_MINMAX:
            profondeur=profondeurBase
            
            if numeroCoup >=51:
                profondeur=64-numeroCoup
            elif numeroCoup >=47:
                profondeur+=2
            elif numeroCoup >=43:
                profondeur+=1
            
            
            if len(coupsPossibles)>=13:
                profondeur-=2
            elif len(coupsPossibles)>=9:
                profondeur-=1
            elif len(coupsPossibles)<=3:
                profondeur+=1
            
            #print("Profondeur : ",profondeur)
            return profondeur
        elif ia == IA_MONTECARLO:
            print(numeroCoup)
            nbrePartie=profondeurBase*60
            nbrePartie=int(nbrePartie/(len(coupsPossibles)*(60-numeroCoup)))
            print(nbrePartie)
            if numeroCoup >=50:
                nbrePartie*=2
            elif numeroCoup >=40:
                nbrePartie=int(nbrePartie*1.5)
            #print("Nombre partie par possibilités : ",nbrePartie)
            return nbrePartie
        else:
            return profondeurBase
    
    
    def onClic(self,coordCoup:tuple, lapsTemps:int):
        if  not   self.varFinPartie:       
            coupsPossibles=g.calculCoupAutorise(self.grille, self.joueur)
            
            if coupsPossibles==[]:#si le joueur doit passer
                self.varFinPartie=v.finPartie(self.score,self.coupsPossiblesPrecedant,coupsPossibles)#fin de partie?
                self.coupsPossiblesPrecedant=coupsPossibles[:]
                self.joueur=g.joueurAdverse(self.joueur)
                if self.afficherIHM:
                    #affciher le joueur
                    self.othello.affichage_joueur()
                    
                    #afficher les cases possibles:
                    self.othello.suppr_cases_possibles()
                    self.othello.cases_possibles()
                    self.othello.frame_victoire()
                    print(self.joueur ," ne peut pas jouer et passe son tour")
                    print("Score : " , self.score)
                else:
                    self.onClic(None,None)
            else:
                #création d'une liste avec uniquement les tuples des coordonnées des coups possibles
                coordCoupsPossibles=[]
                for liste in coupsPossibles:
                    coordCoupsPossibles.append(liste[0])
                
                
                #####Disjonction de cas en fonction du type de joueur qui doit jouer
                
                #si c'est à l'humain de jouer les coordonnes du coup a jouer sont des arguments de la fonction
                
                #si c'est à l'IA aleatoire de jouer
                if self.dicoJoueurs[self.joueur]==IA_ALEA:
                    coordCoup=a.IA_Alea (coordCoupsPossibles)
                
                #si c'est à l'IA de maximisation de jouer
                elif self.dicoJoueurs[self.joueur]==IA_MAXIMISATION:
                    coordCoup=x.IA_Maxi (coupsPossibles)
                
                #si c'est à l'IA minmax de jouer   
                elif self.dicoJoueurs[self.joueur]==IA_MINMAX:
                    now=time.time()
                    profondeurMaxi=4
                    profondeurMaxi=self.profondeurIA(profondeurMaxi,IA_MINMAX,coordCoupsPossibles)
                    coordCoup=m.MinMax(self.grille,True, self.joueur, self.score,profondeurMaxi)[1]
                    #print("temps : ", time.time()-now)
                    
                
                #si c'est à l'IA min max avec coupure alpha beta de jouer   
                elif self.dicoJoueurs[self.joueur]==IA_MINMAXALPHABETA:
                    now=time.time()
                    
                    profondeur=8
                    profondeurMaxi=self.profondeurIA(profondeur,IA_MINMAXALPHABETA, coordCoupsPossibles)
                    
                    result=n.negaMax(self.grille,True, self.joueur, self.score,profondeurMaxi)
                    coordCoup=result[1]
                    #print("temps : ", time.time()-now)
                
                #si c'est à l'IA probabiliste Monte Carlo de jouer   
                elif self.dicoJoueurs[self.joueur]==IA_MONTECARLO:
                    now=time.time()
                    
                    nombrePartieTotal =100  #300
                    nombrePartie=self.profondeurIA(nombrePartieTotal,IA_MONTECARLO, coordCoupsPossibles)
                    coordCoup=o.monteCarlo(self.grille, self.joueur,self.score,nombrePartie)
                    #print(coordCoup)
                    #print("temps : ", time.time()-now)
                    
                #####
                
                if coordCoup in coordCoupsPossibles:
                    #mise a jour de la grille
                    g.placerPion(self.grille,self.joueur,coordCoup,self.score) #permet de placer le pion 
                    
      
                    
                    
                    
                    coordPionARetourner=coupsPossibles[coordCoupsPossibles.index(coordCoup)][1]#recuperation des coordonnes des pions a retourné en lien avec le coup effectué
                    g.retournerPion(self.grille, self.joueur, coordPionARetourner, self.score)#retourner les pions 
                    
                    
                    self.varFinPartie=v.finPartie(self.score,self.coupsPossiblesPrecedant,coupsPossibles)#fin de partie?
                    self.coupsPossiblesPrecedant=coupsPossibles[:]
                    
                    
                    self.joueur=g.joueurAdverse(self.joueur)#changer de joueur
                    
                    if self.afficherIHM:
                        print(self.grille)
                        print("Score : " , self.score)
                        #afficher la grille dans l'interface graphique
                        self.othello.afficherGrilleIHM(self.grille)
    
                        #pour faire jouer l'ia
                        if self.dicoJoueurs[self.joueur] != HUMAIN:
                            self.othello._frame1.after(lapsTemps, lambda: self.onClic(None,lapsTemps))#permet de faire jouer l'ia tout en permetttant l'affichage du coup du joueur
                        #afficher le score    
                        self.othello.afficherScore()
                        
                        #affciher le joueur
                        self.othello.affichage_joueur()
                        
                        #afficher les cases possibles:
                        self.othello.suppr_cases_possibles()
                        self.othello.cases_possibles()
                        
                        self.othello.suppr_pions()
                        self.othello.pion_a_retourner()
                        self.othello.frame_victoire()
                    else:
                        self.onClic(None,None)
                else :
                    if self.afficherIHM:
                        print("Ce coup n'est pas possible. Merci d'entrer de nouvelles coordonnées.")
        else:
            if self.afficherIHM:
                print("Fin de Partie")



        