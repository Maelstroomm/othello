# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 16:26:11 2023

@author: Mael
"""
#pour ouvrir un fichier
#from tkinter import fildialog
#filedialog.askopenfilename
import tkinter as tk 
from tkinter import ttk
from tkinter.filedialog import askopenfilename,asksaveasfilename
import pickle
from functools import partial
import ControleurPartie as ctrl
from variablesGlobales import VIDE,NOIR,BLANC,BORD,HUMAIN,IA_MINMAX,IA_MAXIMISATION,IA_ALEA,IA_MINMAXALPHABETA,IA_MONTECARLO
import gestion_des_coups as g
import webbrowser
import Victoire as v
import time







        
    

class Othello(tk.Tk): #la classe othello herite de la classe tk.Tk
    
    def __init__(self): #constructeur
        super().__init__()


        self._coordDernierClic=(0,0)#

        self.listecases = []
        self.listepion_ret = []

        #taille de la fentere
        self._largeurEcran=0.95*self.winfo_screenwidth();  #obtient la largeur de l'ecran
        self._hauteurEcran=0.90*self.winfo_screenheight()  #obtient la hauteur de l'ecran
        #self.geometry("%dx%d" % (self._largeurEcran,self._hauteurEcran))
        self.geometry("700x600") #largeurxhauteur   on a prefere creer une fenetre de taille fixe pour un resultat esthetique optimal
        self.iconbitmap("Othello_logo.ico")
        #proprietes de la fenetre
        self.title("Othello")
        
        #numero de la frame actuelle
        self._numeroFrame=0 
        
        #definition d'une variable canvas
        self._canvas=None
        
        
        self._canvasTaille =  800 #min(self.hauteurEcran, self.largeurEcran)
        self._tailleCase=self._canvasTaille/8
        
        self.varAfficherCasesPossibles = tk.IntVar()
        self.varAfficherNbrepion = tk.IntVar()
        
        
        #definir les differentes frames de l'appli (ici les differentes fenetres)
        self._frame1=tk.Frame(self)
        self._frame2=tk.Frame(self)
        self._frame3=tk.Frame(self)
        self._frame4=tk.Frame(self)
        #self.iconbitmap("Othello_logo.ico")
        
        #gerer les evenement du clavier
        # quitter proprement si on appuye sur echap ou si on ferme la fenetre
        self.bind("<Escape>",lambda event: self.destroy())  
        
        #creer la premiere frame
        self.createFrame1()
        
        
        #temps de reaction de l'ia
        self.lapsTempsIA=800
        
        #si le bouton jouer contre l'ordinateur n'est pas selectionner alors on est forcement dans le cas d'un match JcJ
        self.joueur1 = HUMAIN
        self.joueur2 = HUMAIN
        
        #varible de score:
        self.varScore1=tk.StringVar()
        self.varScore2=tk.StringVar()
        
        #varaible de joueur
        self.varjoueur=tk.StringVar()
        
        
        
    
    def createFrame1(self):
        #fenetre d'accueil. 
        self._numeroFrame=1
        self._frame1.grid()
        
        self.joueur1 = HUMAIN
        self.joueur2 = HUMAIN
        
        #creation grande zone de texte pour permettre le placement des boutons a peu pres au milieu de la fenetre
        text = tk.Label (self._frame1, text = ' ', width = 28, height=12)
        text.grid (row=0, column = 1)
        
        #creation du bouton de jeu JcJ qui permet de jouer a 2 sur l'odinateur a tour de rôle
        btJouer=tk.Button(self._frame1, text="Jouer à 2",bg="green", fg="white", command=self.createFrame2)
        btJouer.grid(row=1, column=2)
        
        text2 = tk.Label (self._frame1, text = ' ')
        text2.grid (row=2, column = 2)
        
        #creation du menu deroulant pour la difficulte de l'IA contre laquelle on souhaite jouer
        labelChoix = tk.Label(self._frame1, text = "Veuillez faire un choix de difficulté !")
        labelChoix.grid(row=4, column=2)
        listeDifficulte=["Facile 1", "Facile 2","Moyen", "Difficile", "Expert"]
        listeCombo = ttk.Combobox(self._frame1, values=listeDifficulte, text = "Veuillez faire un choix de difficulté !")
        listeCombo.current(0)
        listeCombo.grid(row=5, column=2)
       
        #creation du bouton pour lancer la partie contre l'IA
        btJouer2=tk.Button(self._frame1, text="Jouer contre l'ordinateur",bg="green", fg="white", command=partial(self.diff_ordi, listeCombo))
        btJouer2.grid(row=3, column=2)
        
        
        
        #choix de la couleur du joueur et placement des radioButton
        text3 = tk.Label (self._frame1, text = ' ')
        text3.grid (row=6, column = 2)
        
        text4 = tk.Label (self._frame1, text = 'Veuillez choisir la couleur que vous souhaitez jouer')
        text4.grid (row=7,column=2)
        
        liste = ['Blanc', 'Noir']
        joueur = [BLANC,NOIR]
        self.varGr = tk.StringVar()
        self.varGr.set (liste[1])
        for i in range (2):
            self._choixjoueur = tk.Radiobutton(self._frame1, variable= self.varGr, text = liste[i], value = joueur[i])
            self._choixjoueur.grid (row = 8+i, column =2)
        
        self._choixjoueur.select ()
        
        
        #creation du bouton pour faire des test sur les ia
        btTest=tk.Button(self._frame1, text="Tester les IA",bg="green", fg="white", command=self.createFrame4)
        btTest.grid(row=12, column=2, pady=50)
       
    def createFrame2(self):
        #fenetre de jeu
        self._numeroFrame=2
        self._frame1.destroy()
        self._frame1=tk.Frame(self)
        
        self._frame2.grid()  

        
        #creation de l'objet controleur qui va permettre de controler les actions de la partie
        self.choix_joueur()

        
            
        #Canvas
        self._initCanevas()#initialisation du canvas


        #creation d'une barre de menu
        menu = tk.Menu(self)
        self.config(menu=menu)
        #definition du menu fichier et de tout les boutons disponibles
        fichierMenu = tk.Menu(menu)
        menu.add_cascade(label="Fichier", menu=fichierMenu)
        fichierMenu.add_command(label="Ouvrir...", command=self.ouvrir)
        fichierMenu.add_command(label="Sauvegarder", command=self.sauvegarde)
        fichierMenu.add_separator()
        fichierMenu.add_command(label="Retour au menu", command=self.retour)
        fichierMenu.add_command(label="Quitter le jeu", command=self.destroy)
       
        
        #definition du menu parametre et de tout les boutons disponibles
        parametreMenu = tk.Menu(menu)
        menu.add_cascade(label="Paramètres", menu=parametreMenu)
        tempsIaMenu = tk.Menu(menu)
        parametreMenu.add_cascade(label="Temps reaction IA", menu=tempsIaMenu)
        tempsIaMenu.add_radiobutton(label="Immediat", command=partial(self.changerTempsIA,50))
        tempsIaMenu.add_radiobutton(label="1/2 seconde", command=partial(self.changerTempsIA,500))
        tempsIaMenu.add_radiobutton(label="1 secondes", command=partial(self.changerTempsIA,1000))
        tempsIaMenu.add_radiobutton(label="2 secondes", command=partial(self.changerTempsIA,2000))
        tempsIaMenu.add_radiobutton(label="5 secondes", command=partial(self.changerTempsIA,5000))
        tempsIaMenu.add_radiobutton(label="10 secondes", command=partial(self.changerTempsIA,10000))
        
        #definition du menu affichage et de toutes les boutons disponibles
        afficherMenu = tk.Menu(menu)
        menu.add_cascade(label="Affichage", menu=afficherMenu)
        afficherMenu.add_checkbutton(label="Cases possibles", variable=self.varAfficherCasesPossibles, onvalue= 1, offvalue = 0 , command=self.cases_possibles)
        afficherMenu.add_checkbutton(label="Nombre pions a retourner", variable=self.varAfficherNbrepion, onvalue=1, offvalue=0, command= self.pion_a_retourner)

        
        #definition du menu aide et de toutes les boutons disponibles
        aideMenu = tk.Menu(menu)
        menu.add_cascade(label="Aide", menu=aideMenu)
        aideMenu.add_command(label="A propos...", command=partial(self.createFrame3))
        aideMenu.add_command(label="Règles du jeu", command=partial(self.page_web))
        
        
        
        #affichage du score:
        score1 = tk.Label(self._frame2, textvariable = self.varScore1)
        score2 = tk.Label(self._frame2, textvariable = self.varScore2)
        score1.grid ( row = 3, column = 20)
        score2.grid ( row = 4, column = 20)
        self.afficherScore()
        
        #affichage du joueur
        joueur = tk.Label (self._frame2, textvariable = self.varjoueur)
        joueur.grid (row = 1, column = 20)
        self.affichage_joueur()
    
    
    def createFrame3(self):
        
        fenetreCredit=tk.Tk ()
        fenetreCredit.title ("Crédits")
        text = tk.Label (fenetreCredit, text =  "Merci d'avoir joué à notre version du jeu Othello développée dans le cadre d'un projet scolaire \n Credits : Maël Bornard et Aloïs Morin")
        text.grid(row = 0 , column = 0)
        
        fenetreCredit.iconbitmap("Othello_logo.ico")
    
    def createFrame4 (self):
        self._numeroFrame=4
        self._frame1.destroy()
        self._frame1=tk.Frame(self)
        
        self._frame4.grid()  
        
        #titre
        text = tk.Label (self._frame4, text ="Tester la performance des IA",borderwidth =10)
        text.grid (row=0, column = 1, columnspan=5)
        
        #type d'ia dispo
        listeIA=["IA aléatoire", "IA de maximisation","IA MinMax", "IA MinMax coupure alpha beta","IA probabiliste Monte Carlo"]
        listeVariableIA=[IA_ALEA,IA_MAXIMISATION,IA_MINMAX,IA_MINMAXALPHABETA,IA_MONTECARLO]
        #creation du 1er menu deroulant pour chosir le type de la premiere IA
        labelChoix1 = tk.Label(self._frame4, text = "Type de la première IA :")
        labelChoix1.grid(row=4, column=2)
        listeCombo1 = ttk.Combobox(self._frame4, values=listeIA, width=25)
        listeCombo1.current(0)
        listeCombo1.grid(row=5, column=2,padx=10, pady=4)
        
        #creation du 2 eme menu deroulant pour chosir le type de la deuxieme IA
        labelChoix2 = tk.Label(self._frame4, text = "Type de la deuxième IA :")
        labelChoix2.grid(row=4, column=3)
        listeCombo2 = ttk.Combobox(self._frame4, values=listeIA, width=25)
        listeCombo2.current(0)
        listeCombo2.grid(row=5, column=3,padx=10, pady=4)
        
        
        
        #titre
        text2 = tk.Label (self._frame4, text ="Nombre de partie(s) à simuler")
        text2.grid (row=4, column = 4)
        
        #creation d'un champ de saisie pour rentrer le nombre de partie a simuler
        saisie=tk.StringVar() 
        champSaisie=tk.Entry(self._frame4, textvariable =saisie, width=7)
        champSaisie.insert(0,"10")
        champSaisie.grid(row=5, column=4)
        
        #creation du bouton jouer
        btJouerIA=tk.Button(self._frame4, text="Lancer",bg="green", fg="white", command=partial(self.lancerSimulationIa,saisie,listeCombo1,listeCombo2,listeIA,listeVariableIA))
        btJouerIA.grid(row=6, column=2, columnspan=3,padx=20,pady=50)
        
        #creation du bouton retour
        btRetour=tk.Button(self._frame4, text="Retour au menu",bg="green", fg="white", command=self.retour)
        btRetour.grid(row=12, column=12,pady=200)
        
        text="Ne paniquez pas si la fenêtre ne repond pas, \n les calculs ont lieu et prennent du temps,\n Merci de ne pas fermer la fenêtre"
        texte_attente=tk.Label(self._frame4, text=text,justify ='left')
        texte_attente.grid(row=8, column=2, columnspan=3)
        
    def lancerSimulationIa (self,saisie,combo1,combo2,listeIA:list,listeVariableIA:list):
        nbrePartie=saisie.get()
        try:
            nbrePartie=int(nbrePartie)
            continuer=True
        except:
            print("Merci d'entrer un nombre entier")
            continuer=False
        if continuer:
            #recuperation des types d'ia 
            type1=combo1.get()
            type2=combo2.get()
            self.joueur1=listeVariableIA[listeIA.index(type1)]
            self.joueur2=listeVariableIA[listeIA.index(type2)]
            
            
            
            #lancer la simulation
            now =time.time()
            print("Simulation : ",nbrePartie,"parties ; joueur noir :",type1,"; joueur blanc :",type2)
            resultats=self.simulerParieIa(nbrePartie)
            print("-----------------------------------------------")
            print("Simulation terminée en", round(time.time()-now,3), "s.")
            print(nbrePartie,"partie jouées")
            print("Resultats :")
            print(type1 ,"(Noir) a gagné", resultats[0], "fois.")
            print(type2 ,"(Blanc) a gagné", resultats[1], "fois.")
            print("Il y a eu",resultats[2], "exaequo.")
            texte="Simulation terminée en "+str(round(time.time()-now,3))+ "s.\n"+str(nbrePartie)+" partie jouées.\nResultats :\n"+ type1 +" (Noir) a gagné "+str(resultats[0])+" fois.\n"+ type2 +" (Blanc) a gagné "+str(resultats[1])+" fois.\nIl y a eu "+str(resultats[2])+ " exaequo."
            texteResultat=tk.Label(self._frame4, text=texte,justify ='left')
            texteResultat.grid(row=7, column=2, columnspan=3)
            
    def simulerParieIa(self,nbrePartie:int)->list:
        partie=0
        listeResultat=[0,0,0]#nombre de partie gagnees par l'ia 1, l'ia 2 et le nombre d'exaequo
        while partie < nbrePartie:
            print("Partie : ",partie)
            #creation d'un nouveau controleur
            self._controleur=ctrl.ControlePartie(self, self.joueur1, self.joueur2,False)
            #lancement de la partie
            self._controleur.onClic(None,None)
            #recupperation des resultats
            gagnant=self._controleur.varFinPartie
            if gagnant == NOIR:
                listeResultat[0]+=1
            elif gagnant == BLANC:
                listeResultat[1]+=1
            else:
                listeResultat[2]+=1
            partie+=1
        return listeResultat
    
    
    
    #definition de l'option retour a la fenêtre d'accueil 
    def retour(self):
        if self._numeroFrame==2:
            self._frame2.destroy()#detruire la frame2
            self._frame2=tk.Frame(self)#la redeclarer 
            self.createFrame1()
        elif self._numeroFrame==4:
            self._frame4.destroy()#detruire la frame4
            self._frame4=tk.Frame(self)#la redeclarer 
            self.createFrame1()
    
    
    
    #definition de la difficulte de l'odinateur dans le cas d'un match contre lui
    def diff_ordi (self,combobox):

        self.joueur1 = HUMAIN
        difficulte=combobox.get() #on recupere la valeur de la combobox et on attribue une IA pour chaque difficulté
        if difficulte == "Facile 1":
            self.joueur2 = IA_MAXIMISATION
        elif difficulte == "Facile 2":
            self.joueur2 = IA_ALEA
        elif difficulte == "Moyen":
            self.joueur2 = IA_MONTECARLO
        elif difficulte == "Difficile":
            self.joueur2 = IA_MINMAX
        elif difficulte == "Expert" :
            self.joueur2 = IA_MINMAXALPHABETA
            
        if difficulte in ("Facile 1", "Facile 2", "Moyen","Difficile","Expert"):
            self.createFrame2()
      
    def page_web(self):
        
        """
        Permet d'ouvrir la page internet définisant les règles de l'othello
        """
        webbrowser.open('https://www.ffothello.org/othello/regles-du-jeu/')
     
    def afficherScore(self): 
        """
        Permet de mettre a jour les widget score pour afficher les scores des deux joueurs
        """
        noir = str (self._controleur.score[1])
        blanc = str (self._controleur.score[0])
        self.varScore1.set("Score joueur noir : " + noir )
        self.varScore2.set("Score joueur blanc : " + blanc )
     
        
     
   
    
    def affichage_joueur (self):
        """
        Affichage de la couleur du joueur qui doit jouer sur l'interface graphique
        """
        joueur = self._controleur.joueur
        if joueur == BLANC :
            text = "Blanc"
        elif joueur == NOIR :
            text = "Noir"
        
        self.varjoueur.set("Tour du joueur : " + text)
        
        
    def choix_joueur(self):
        """
        Permet de choisir la couleur que l'on souhaite jouer lors d'un match contre l'IA
        """

        joueur=int(self.varGr.get())
        if joueur == NOIR:
            self._controleur=ctrl.ControlePartie(self, self.joueur1, self.joueur2)
        if joueur == BLANC:
            self._controleur=ctrl.ControlePartie(self, self.joueur2, self.joueur1)
    
    
    def pion_a_retourner (self):
        """
        Fonction qui affiche sur le plateau le nombre de pions que l'on peut retourner en jouant à l'emplacement du chiffre
        """

        
        if self.varAfficherNbrepion.get() == 1:
            listepions = []
            liste = []
            listeCasesPossibles = g.calculCoupAutorise (self._controleur.grille, self._controleur.joueur)
        
            for i in range (len (listeCasesPossibles)):
                listepions.append (str(len(listeCasesPossibles[i][1])))
                liste.append (listeCasesPossibles[i][0])
            
            for j in range (len(liste)):
                a = (self._tailleCase*(liste[j][1]-1) + (self._tailleCase/2))
                b = (self._tailleCase*(liste[j][0]-1) + (self._tailleCase/2))
            
            
                self.listepion_ret.append (self._canvas.create_text(a,b, anchor= 'center' ,text = listepions[j]))
            
        else :
            self.suppr_pions()
            
    
    def cases_possibles(self):
        """
        Fonction qui permet d'afficher les cases jouables dans une autre couleur
        Compatible avec le nombre de pions que l'on peut retourner

        """
        
        if self.varAfficherCasesPossibles.get() == 1:
            
            liste = []
            listeCasesPossibles = g.calculCoupAutorise (self._controleur.grille, self._controleur.joueur)
            
            for i in range (len (listeCasesPossibles)):
                liste.append (listeCasesPossibles[i][0])
                   
            for j in range (len(liste)):
                a = (self._tailleCase*(liste[j][1]-1))
                b = (self._tailleCase*(liste[j][0]-1))
                c = a + self._tailleCase
                d = b +self._tailleCase
                    
                self.listecases.append (self._canvas.create_rectangle(a,b,c,d, fill = "#E81F00"))
        else:
            self.suppr_cases_possibles()
    
    
    def suppr_pions (self):
        """
        Permet de "détruire" le nombre de pions a retourner du coup précédent pour les remettre a jour dans l'interface

        """
        for i in range (len(self.listepion_ret)):
            self._canvas.delete(self.listepion_ret[i])
        self.listepion_ret = []
        
        
    def suppr_cases_possibles(self):
        """
        Permet de "détruire" les cases possibles affichées du coup précédent pour les remettre a jour dans l'interface

        """
        for j in range (len(self.listecases)):
            self._canvas.delete(self.listecases[j])
        self.listecases=[]
    
    
    
    def changerTempsIA(self,temps:int):
        """
        permet a l'utilisateur de modifier le temps que met l'IA pour jouer son coup
        """
        self.lapsTempsIA=temps
        
    
    def frame_victoire(self):
        """
        Permet d'ouvrir une fenetre donnant le vainqueur ainsi que le score obtenu à la fin par chacun des deux joueurs
        """
        
        gagnant = self._controleur.varFinPartie
        if gagnant == BLANC :
            text = "Le gagnant est le joueur Blanc avec un score de " + str(self._controleur.score[0]) + " à " + str(self._controleur.score[1])
        elif gagnant == NOIR :
            text = "Le gagnant est le joueur Noir avec un score de " + str(self._controleur.score[1]) + " à " + str(self._controleur.score[0])
            
        elif gagnant == "exaequo":
            text = "Egalité, aucun des des joueurs n'est vainqueur"
            

        
        if self._controleur.varFinPartie != False :  
            fenetreVictoire=tk.Tk ()
            fenetreVictoire.geometry("300x70")
            fenetreVictoire.title ("Gagnant")
            text = tk.Label (fenetreVictoire, text = text ) 
            text.grid()
            fenetreVictoire.iconbitmap("Othello_logo.ico")
    
    
    def _initCanevas(self):
        """
        Création du canvas dans l'interface graphique
        """       
           
        self._canvas = tk.Canvas(self._frame2, background="forestgreen", width=self._canvasTaille, height=self._canvasTaille)
        
        #demarrage de la detection d'un clic de souris pour la placement d'un pion (clic gauche)
        self._canvas.bind('<Button-1>', self._clic)
        
        #affichage de la grille
        for i in range (8):
            self._canvas.create_line((0,self._tailleCase*i),(self._canvasTaille,self._tailleCase*i))
        for i in range (8):
            self._canvas.create_line((self._tailleCase*i,0),(self._tailleCase*i),self._canvasTaille)
        
        
        self._controleur.initialisergrilleIHM()#initilaliser la grillle (le tableau np)
        
        self._canvas.grid(row=0,column=0,rowspan=8,columnspan = 4) #afficher le canvas creer plus tot
        
    
    def afficherGrilleIHM (self, grille):
        """
        affiche la grille dans l'interface graphique
        """
        #parcours tous le tableau (sauf les bords)
        for i in range(1,len(grille)-1):
            for j in range(1,len(grille)-1):
                if grille[i][j] != VIDE:#si la case n'est pas vide
                    self.dessinerPion((i,j), grille[i][j])#affichage du pion
            
    
    
    def dessinerPion(self, coord :tuple,joueur):
        """
        permet d'afficher un pion dans le canvas a un emplacement donne et adapte la couleur au joueur

        Parameters
        ----------
        coord : tuple : coordonnee (ligne, colonne) dans la grille(tableau) du pion
        joueur : TYPE

        Raises
        ------
        Exception
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if joueur == NOIR:
            couleur="black"
        elif joueur == BLANC:
            couleur="white"
        else:
            raise Exception("Dans dessinerPion, joueur non conforme ")
        
        #conversion des coord ligne colonne en coord 'algeprique' 
        #calcul des coordonnees de points en haut a gauche(x0,y0) et en bas a droite (x1,y1)de la case se trouvant a ligne colonne
        ligne, colonne=coord[0]-1, coord[1]-1
        
        x0=colonne*self._tailleCase
        y0=ligne*self._tailleCase
        x1=(colonne+1)*self._tailleCase
        y1=(ligne+1)*self._tailleCase
        marge=0.9*self._tailleCase
        
        #affichage du pion : rond 
        self._canvas.create_oval((x0+marge,y0+marge),(x1-marge,y1-marge), fill=couleur)
        
        
        
        
    def _clic(self, event):
        """
        fonction qui est appellee lors d'un clic de la souris sur le canvas

        """
        #recuuperer les coordonnees du clic
        x=event.x
        y=event.y

        #conversion des coodonees du clic en coordonnees ligne colonne.
        ligne=int(y//self._tailleCase+1)
        colonne=int(x//self._tailleCase+1)
        #print("ligne :", ligne,"; colonne :", colonne)
            
        self._coordDernierClic=(ligne,colonne)
        
        #appeller le controleur pour gerer la logique de la partie
        self._controleur.onClic(self._coordDernierClic, self.lapsTempsIA)
        
        
        
    
    def ouvrir(self):
        """
        Permet de charger une partie enregistree
        L'ouverture s'effectue a partir  d'un fichier binaire a l'extention .pickle

        """
        #boite de dialogue qui recupere le chemin d'acces
        chemin = askopenfilename(initialdir="/Parties Enregistrees",defaultextension='.pickle',filetypes=[('fichier binaire','*.pickle')],initialfile="Une sauvegarde")
        print(chemin)
        
        
        # chargement des donnees a partir du fichier binaire
        with open(chemin, "rb") as f:
            data = pickle.load(f)
        
        
        
        #extraction des donnees:
            
        self.joueur1=data["joueur1"]
        self.joueur2=data["joueur2"]
        self._controleur.joueur=data["joueur"]
        self._controleur.dicoJoueurs=data["dicoJoueurs"]
        self._controleur.coupsPossiblesPrecedant=data["coupsPossiblesPrecedant"]
        self._controleur.score=data["score"]
        self._controleur.varFinPartie=data["finPartie"]
        self._controleur.grille=data["grille"]
        valueAfficherCasesPossibles=data["valueAfficherCasesPossibles"]
        valueAfficherNbrepion=data["valueAfficherNbrepion"]
        self.lapsTempsIA=data["lapsTempsIA"]
        
        self.affichageNouvellePartie(valueAfficherCasesPossibles,valueAfficherNbrepion)
        
        
    def sauvegarde(self):
        """
        Permet de sauvgarder une partie en cours.
        La sauvgarde s'effectue dans un fichier binaire a l'extention .pickle
        Elements enregistres : 
            grille
            types des joueurs
            joueur actuel
            score
            options d'affichage et tps de reaction de l'ia
            ...
            
        """
        
        #boite de dialogue qui recupere le chemin d'acces
        chemin = asksaveasfilename(initialdir="/Parties Enregistrees",defaultextension='.pickle',filetypes=[('fichier binaire','*.pickle')],initialfile="Sauvegarde_othello")
        print(chemin)
        
        
        
        # preparer les donner a enregistrer dans un dictionaire :
        data = {
            "joueur1" : self.joueur1,
            "joueur2" : self.joueur2,
            "joueur" : self._controleur.joueur,
            "dicoJoueurs" : self._controleur.dicoJoueurs,
            "coupsPossiblesPrecedant" : self._controleur.coupsPossiblesPrecedant,
            "score" : self._controleur.score,
            "finPartie" : self._controleur.varFinPartie,
            "grille" : self._controleur.grille,
            "valueAfficherCasesPossibles" :self.varAfficherCasesPossibles.get(),
            "valueAfficherNbrepion":self.varAfficherNbrepion.get(),
            "lapsTempsIA": self.lapsTempsIA
            }
        
        # enregistrement des donnees dans un fichier binaire
        with open(chemin, "wb") as fichier:
            pickle.dump(data, fichier)
            
    
    def affichageNouvellePartie(self,valueAfficherCasesPossibles:int,valueAfficherNbrepion:int):
        """
        Est appelee apres l'ouverture d'une partie enregistree
        Permet d'afficher la la grille sur le canvas, de mettre a jours les scores et les differentes options

        """
        #canvas
        self._canvas.destroy()
        self._initCanevas()
        
        #score et tour de jeu
        self.affichage_joueur()
        self.afficherScore()
        
        #cases possibles et pions a retourner
        self.varAfficherCasesPossibles.set(valueAfficherCasesPossibles)
        self.cases_possibles()
        self.varAfficherNbrepion.set(valueAfficherNbrepion)
        self.pion_a_retourner()
        
                
    
        
app=Othello()

app.mainloop()
