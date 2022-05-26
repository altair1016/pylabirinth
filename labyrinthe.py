#!/usr/bin/env python
# -*- coding: Utf-8 -*
'''
@author: Marco Iannella, Mattia Primavera
@copyright: Copyrights for code authored by Marco Iannella, Mattia Primavera
@version: 1.0.0
'''
import tkinter
import sys
import os
import time
#import tkinter.filedialog

class Labyrinthe:
	""" Cette classe, modélise un labyrinthe reél avec les fonctions qu 'il lui apartient, l'interface et le movement du joueur"""
	
	def __init__(self):
		"""Initialisation des variables des variables en Python"""
		self.labyrinthe = []
		self.fenetre = tkinter.Tk()
		self.fenetre.title("Labyrinthe")	
		self.bouton = tkinter.Button(self.fenetre, text="Quitter", command=self.fenetre.destroy)
		self.regle = tkinter.Canvas(self.fenetre, height=100, width=3000, bg="black")
		self.regle.create_text(250, 50, text="Aider ErFantasmaGiallo à sortir de son faux monde PacMan\nH=pour alle en haut\nB=pour aller en bas\nG=pour aller a gauche\nD=pour aller a droite", fill="yellow")
		self.bouton.configure(width=1000)
		self.canvas = tkinter.Canvas(self.fenetre, height=3000, width=3000, bg="black")
		self.entree = tuple()
		self.gagne = 0 #tant que self.gagne = 0 c'est possible de faire des mouvements
		self.img = tkinter.PhotoImage(file="fantasminoRosso.gif")
		self.mouvements = 0
		self.tempsActuel = 0 
		self.nomFichier="labyrinthe.lab"
	def chargeLab (self, nomFichier):
		"""Fonction qui prends en argument le nom d'un fichier et charge le labyrinthe contenu dans celui ci *.lab"""
		compteur = 1
		listeLignesLab = list()
		fichier = open(nomFichier, "r")
		for ligne in fichier.readlines():
			chaineConverti = ""
			for car in ligne:
				if car == "0":
					chaineConverti += "   "
				if car == "E" and compteur%2 != 0:
					chaineConverti += " E "
				if car == "1" and compteur%2 != 0:
					chaineConverti += "---"
				if car == "1" and compteur%2 == 0:
					chaineConverti += "|  "
				if car == "E" and compteur%2 == 0:
					chaineConverti += "E  "
			listeLignesLab.append(chaineConverti)
			compteur +=1
		for i, ligne in enumerate(listeLignesLab):
			if(i % 2 != 0):
				listeLignesLab[i] = ligne[0:len(listeLignesLab[i])-2]
		fichier.close()
		for i in listeLignesLab:
			chaine = i
			listeCar = list()
			for car in chaine:
				listeCar.append(car)
			self.labyrinthe.append(listeCar)
		self.entree = self.rechercheEntree()

	def afficheLab(self):
		"""Fonction qui affiche le labyrinthe"""
		for element1 in self.labyrinthe:
			for element2 in element1:
				print(element2, end='')
			print("\n", end='')

	def rechercheEntree(self):
		"""Fonction qui cherche l'entree du labyrinthe et return 0 si il la trouve, autrement return 1"""
		entree = "E"
		for i in enumerate(self.labyrinthe):
			for j in enumerate(i[1]):
				if j[1] == entree and i[0] == 0:
					#retourne 1 si l'entree se trouve dans le haut du lab
					return(i[0], j[0], 1)
				if i[0]%2!=0 and i[1][0] == entree:
					#retourne 2 si l'entree se trouve a gauche du lab
					return(i[0], j[0], 2)
				if  j[1] == entree and i[0] == len(self.labyrinthe)-1:
					#retourne 3 si l'entree se trouve dans le bas du lab
					return(i[0], j[0], 3)
				if i[0]%2 !=0 and j[0] == len(i[1]) -1 and j[1]==entree:
					#retourne 4 si l'entree se trouve a la droite du lab
					return(i[0], j[0], 4)
		return 0

	def rechercheJoueur(self):
		"""Fonction qui cherche le joueur du labyrinthe et return 0 si il la trouve, autrement return 1"""
		joueur = "J"
		for i in enumerate(self.labyrinthe):
			for j in enumerate(i[1]):
				if j[1] == joueur :
					return(i[0], j[0], 1)
		return 0


	def nouvellePartie(self):
		"""Fonction qui cherche l'entree dans la liste et il y place le joueur au premier access du programme"""
		entree = "E"
		for i in enumerate(self.labyrinthe):
			for j in enumerate(i[1]):
				if j[1] == entree:
					self.labyrinthe[i[0]][j[0]] = "J"

	def moveDown(self, event):
		""" Fonction qui permet le mouvement vers le bas du joueur dans le lab"""
		position = self.rechercheJoueur()
		print (position, "position")
		print (self.mouvements)
		if "J" in self.labyrinthe[0] and self.entree[2]==1 and self.gagne == 0  :
			#si J est dans la premiere ligne entree ....(reste expliqué plus haut)
			self.labyrinthe[position[0]+1][position[1]] = "J"
			self.labyrinthe[self.entree[0]][self.entree[1]] ="E"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()

		elif  position[1] in range (1, len(self.labyrinthe[position[0]])-2) and position[0]+1 == len(self.labyrinthe)-1 and self.labyrinthe[position[0]+1][position[1]] == " " and self.gagne == 0:
			#si la ligne du J est celle avant la sortie (caracterisé par " ") qui se trouve a la derniere ligne 
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]+1][position[1]] = "J"
			self.afficheLab()
			self.mouvements += 1
			self.restartCanvas()
			self.tempsActuel = int(time.time() - self.tempsActuel )
			self.gagne = 1
			self.finPartie()
		elif position[0]+2 <= len(self.labyrinthe)-2 and position[1] != len(self.labyrinthe[position[0]])-1 and self.labyrinthe[position[0]+1][position[1]] is not "-" and self.labyrinthe[position[0]+2][position[1]] is not "|" and self.gagne == 0 :
			#si la position de J et petit ou egale a la longeur -2 et la case adjacent de la ligne succesive n'a pas de Mur
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]+2][position[1]] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
	
	def moveUp(self,event):
		""" Fonction qui permet le mouvement vers le haut du joueur dans le lab"""
		position = self.rechercheJoueur()
		print (position, "position")
		print (self.mouvements)
		if position[0] == self.entree[0] and self.entree[2] == 3 and self.gagne == 0  :
			#si l'entre donc J sont sur la derniere ligne du lab 
			self.labyrinthe[position[0]-1][position[1]] = "J"
			self.labyrinthe[self.entree[0]][self.entree[1]] ="E"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
		elif position[0] -2 > 0 and self.labyrinthe[position[0]-2][position[1]] is not "|" and self.gagne == 0 and position[1] in range(1, len(self.labyrinthe[position[0]-1])) :
			#verifie la validite de la position et de symboles autour d'elle
			if  self.labyrinthe[position[0]-1][position[1]] is not "-" and position[1] in range (1, len(self.labyrinthe[position[0]])-2): 
				#si la position est dans le range ca veut dire que on est dans le lab et on a rien a voir avec les murs sur le cote. Ca c'est pour ne pas generer les OUTOFB quand l'entree se trouve sur la droi
				self.labyrinthe[position[0]][position[1]] = " "
				self.labyrinthe[position[0]-2][position[1]] = "J"
				self.mouvements += 1
				self.afficheLab()
				self.restartCanvas()
		elif position[1] in range (1, len(self.labyrinthe[position[0]])-2) and position[0]-1 == 0 and self.labyrinthe[position[0]-1][position[1]] == " ":
			#cas gagnant
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]-1][position[1]] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
			self.gagne = 1
			self.finPartie()


	def moveLeft(self,event):
		""" Fonction qui permet le mouvement vers la gauche du joueur dans le lab"""
		position = self.rechercheJoueur()
		print (position,"position")
		print (self.mouvements)
		if position[1] == len(self.labyrinthe[position[0]])-1 and self.entree[2] == 4 and self.gagne == 0  :
			#si l'entre donc J se trouve a la gauche complete du tab
			self.labyrinthe[position[0]][position[1]] = "E"
			self.labyrinthe[position[0]][position[1]-2] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
		elif position[1]-1 in range (1, len(self.labyrinthe[position[0]])) and self.labyrinthe[position[0]][position[1]-1] is not "|" and self.gagne == 0 and position[0] is not len(self.labyrinthe)-1 and position[0] is not 0:
			#si la position de J est compri entre 1 et la fin de la ligne et la case adjacent a gauche n'est pas un mur
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]][position[1]-3] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
		elif position[1] == 1 and self.labyrinthe[position[0]][position[1]-1] == " " and self.gagne ==0 :
			#si la position est eguale a 1 et la case adjacent est eguale a " " ca veut dire que c'est la sortie
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]][position[1]-1] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
			self.tempsActuel = int(time.time() - self.tempsActuel )
			self.gagne = 1
			self.finPartie()
	def moveRight(self,event):
		""" Fonction qui permet le mouvement vers la droite du joueur dans le lab"""
		position = self.rechercheJoueur()
		print (position,"position")
		print (self.mouvements)
		if position[1] == 0  and self.entree[2] == 2 and self.gagne == 0:
			#si l'entre donc le J se trouve a la complete droite du tab
			self.labyrinthe[position[0]][position[1]] = "E"
			self.labyrinthe[position[0]][position[1]+1] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
		elif position[1]+3 in range (1, len(self.labyrinthe[position[0]])) and self.labyrinthe[position[0]][position[1]+2] is not "|" and self.gagne == 0 and position[0] is not len(self.labyrinthe)-1 and position[0]is not 0:
			#si la position actuelle + 3 est compris entre 1 et la longeur de la ligne et deux cases apres il n'y a pas de mur
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]][position[1]+3] = "J"
			self.mouvements += 1
			self.afficheLab()

			self.restartCanvas()
		elif position[1] == len(self.labyrinthe[position[0]])-3 and self.labyrinthe[position[0]][position[1]+2] == " ":
			#cas gagnant
			self.labyrinthe[position[0]][position[1]] = " "
			self.labyrinthe[position[0]][position[1]+2] = "J"
			self.mouvements += 1
			self.afficheLab()
			self.restartCanvas()
			self.tempsActuel = int(time.time() - self.tempsActuel)
			self.gagne = 1
			self.finPartie()
					
	def demarrerFenetre(self):
		"""Fonction qui ouvre une fenetre initialise dans le constructeur"""
		self.bouton.pack()
		self.regle.pack()
		self.canvas.pack()	
		self.dessineLab()
		self.tempsActuel= time.time()
		self.fenetre.bind("<b>", self.moveDown)
		self.fenetre.bind("<h>", self.moveUp)
		self.fenetre.bind("<g>", self.moveLeft)
		self.fenetre.bind("<d>", self.moveRight)
		self.fenetre.mainloop()

	def finPartie(self):

		if self.gagne == 1:
			self.fenetreMessage = tkinter.Tk()
			self.fenetreMessage.title("Fin Partie")
			canvas2= tkinter.Canvas(self.fenetreMessage, width=300,height=30)
			message = tkinter.Message(self.fenetreMessage, text="FELICITATIONS, VOUS AVEZ GAGNÉ!!!\n" + "-Vous avez rejoint la fin en: "+str(self.tempsActuel / 60)[:4]+"min" + "\n-Vous avez effectué "+str(self.mouvements)+" mouvement/s", width=250,background="yellow", relief="raised")
			bouton1 = tkinter.Button(self.fenetreMessage, text="Recommencer", command = self.resetPartie)
			bouton2 = tkinter.Button(self.fenetreMessage, text="Quitter", command = sys.exit)
			bouton1.configure(width=15)
			bouton2.configure(width=15)
			canvas2.pack()
			message.pack()
			bouton1.pack()
			bouton2.pack()
			self.fenetreMessage.mainloop()
		

	def dessineLab(self):
		"""Fonction qui dessine le labyrinthe utilisant le module tkinter"""
		#Lignes 77 a 88 dessinent les murs horizonteaux
		point_depart=[0,0]
		point_arrive=[30,0]
		for element1 in self.labyrinthe:
			point_depart[0] = 0
			point_arrive[0] = 30
			point_depart[1] += 30
			point_arrive[1] += 30
			for element2 in element1:
				point_depart[0] += 30
				point_arrive[0] += 30
				if element2 == "-":
					self.canvas.create_line(point_depart[0],point_depart[1],point_arrive[0],point_arrive[1], width=6, fill="blue", dash=(3,3), splinesteps=3)
					self.canvas.create_line(point_depart[0]+5,point_depart[1]+5,point_arrive[0]+5,point_arrive[1]+5, width=6, fill="white", dash=(3,3), splinesteps=3)
		#Lignes 91 a 105 dessinent les murs verticaux
		point_depart=[0,-30]
		point_arrive=[0,30]
		for element1 in self.labyrinthe:
			point_depart[0] = 0
			point_arrive[0] = 0
			point_depart[1] += 30
			point_arrive[1] += 30
			for element2 in element1:
				point_depart[0] += 30
				point_arrive[0] += 30
				if element2 == "|":
					self.canvas.create_line(point_depart[0],point_depart[1],point_arrive[0],point_arrive[1], width=6, fill="blue", dash=(3,3), splinesteps=3)
					self.canvas.create_line(point_depart[0]+5,point_depart[1]+5,point_arrive[0]+5,point_arrive[1]+5, width=6, fill="white", dash=(3,3), splinesteps=3)
		self.dessineJoueur()
	def dessineJoueur(self):
		"""Fonction dessinant le joueur"""
		point_depart=[0,0]
		point_arrive=[30,20]
		for element1 in self.labyrinthe:
			point_depart[0] = 0
			point_arrive[0] = 30
			point_depart[1] += 30
			point_arrive[1] += 30
			for element2 in element1:
				point_depart[0] += 30
				point_arrive[0] += 30
				if element2 == "J":
					self.canvas.create_image(point_depart[0],point_depart[1], image=self.img)
	
	def restartCanvas(self):
		""" Fonction qui fait une mise a jour du canvas a chaque changement"""
		self.canvas.destroy()
		self.bouton.pack()
		self.canvas = tkinter.Canvas(self.fenetre, height=1400, width=1400, bg="black")
		self.dessineLab()
		self.dessineJoueur()
		self.canvas.pack()

	def modalitePartie(self):
		"""Fonction qui commence une partie"""
		self.chargeLab(self.nomFichier)
		self.afficheLab()
		self.nouvellePartie()
		self.afficheLab()
		self.demarrerFenetre()

	def resetPartie(self):
		"""Fonction qui efface la vieille partie et qui en recrée une autre du moment qu'on decide de recommencer le match"""
		self.fenetre.destroy()
		self.fenetreMessage.destroy()
		lab2=Labyrinthe()
		lab2.modalitePartie()

	#def choixFichier(self):
	#	"""Fonction qui permet de choisir un fichier lab par l'interface"""
	#	fichierMap = tkinter.filedialog.askopenfilename(title="Choisir un fichier")
	#	return fichierMap
	# ON n'a pas eu assez de temp pour travailler sour Ca...

#FIN CLASSE LABYRINTHE 

