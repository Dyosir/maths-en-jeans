# coding: utf-8

"""
Adaptation du programme en version procédurale, mais en utilisant la POO. Seules les fonctions utilisées pour récolter des données n'ont pas été adaptées.
Des fonctions comme "debug", "brut", etc ...
"""


import os
import pickle  


os.chdir(os.getcwd())


class Immeuble(): 
	"""Classe représentant un immeuble et ses différentes propriétés : nombre d'étages, boutons de l'ascenseur.
	On y trouve aussi de nombreuses méthodes qui analysent l'immeuble. """
	def __init__(self, intervalle, liste_boutons):
		""" On crée notre objet."""
		# constantes
		with open("ressources/liste_nb_premiers", "rb") as f: 
			self.liste_nb_premiers = pickle.Unpickler(f).load()
		# variables
		self.intervalle = intervalle  # l'intervalle représente le nombre d'étages 
		self.liste_boutons = liste_boutons
		self.liste_etages_accessibles = self.calculerEtagesAccessibles()
		self.limite = self.calculerLimite()
		self.nb_etages_inaccessibles = self.calculerNbEtagesInaccessibles()
		self.nb_etages_accessibles = self.intervalle - self.nb_etages_inaccessibles

	def __repr__(self):
		""" Méthode permettant d'afficher toutes les propriétés de notre objet. """
		representation = "\
		#### PROPRIETES ####\n\
		Nombre d'étages total : {}\n\
		Boutons disponibles : {}\n\
		Nombre d'étages accessibles : {}(soit {}%)\n\
		Limite (seulement si boutons premiers entre eux) : {}\n\
		#### FIN PROPRIETES ####\
		".format(self.intervalle, ", ".join(str(i) for i in self.liste_boutons), self.nb_etages_accessibles, round((self.nb_etages_accessibles / self.intervalle) * 100, 1), self.limite)
		return representation

	def decomposer(self, nombre_a_decomposer): 
		""" Méthode permettant de décomposer en produit de facteurs premiers un nombre donné. """
		decomposition = []
		i = 0
		while nombre_a_decomposer != 1:
			if nombre_a_decomposer % self.liste_nb_premiers[i] == 0: 
				nombre_a_decomposer /= self.liste_nb_premiers[i]
				decomposition.append(self.liste_nb_premiers[i])
			else: 
				i += 1
		return decomposition


class ImmeubleDeuxBoutonsNaturels(Immeuble): 
	""" Classe représentant un immeuble possédant deux boutons naturels, en plus du bouton 0. """
	def __init__(self, intervalle, liste_boutons):
		self.bouton1 = liste_boutons[1] # boutons avant car dans le constructeur de l'immeuble on appelle des méthodes qui ont besoin des boutons
		self.bouton2 = liste_boutons[2]
		Immeuble.__init__(self, intervalle, liste_boutons) # on reprend le constructeur d'Immeuble

	def calculerEtagesAccessibles(self):
		""" Méthode permettant de calculer les étages accessibles de l'immeuble à partir deux deux boutons. """
		liste_etages_accessibles = []
		i = 0
		while i * self.bouton1 <= self.intervalle: 
			j = 0
			while i * self.bouton1 + j * self.bouton2 <= self.intervalle:
				liste_etages_accessibles.append(i * self.bouton1 + j * self.bouton2)
				j += 1
			i += 1
		liste_etages_accessibles = sorted(list(set(liste_etages_accessibles)))  # pour éviter les doublons et trier la liste 
		return liste_etages_accessibles

	def calculerLimite(self): 
		""" On calcule la 'limite' des boutons grâce à la formule f(x, y) = (x - 1)(y - 1). """
		if self.premiersEntreEux(self.bouton1, self.bouton2):
			limite = (self.bouton1 - 1) * (self.bouton2 - 1)
		else: # ils ne sont pas premiers entre eux
			limite = "PAS DE LIMITE CAR PAS PREMIERS ENTRE EUX"
		return limite 

	def calculerNbEtagesInaccessibles(self):
		""" On calcule le nombre d'étages inaccessibles grâce à la formule : (I / k) * (k - 1) + (aO - a - O + 1) / 2 ."""
		if self.premiersEntreEux(self.bouton1, self.bouton2):
			k = 1
			a = self.bouton1
			O = self.bouton2
		else:
			dec_1 = self.decomposer(self.bouton1)
			dec_2 = self.decomposer(self.bouton2)
			liste_diviseurs_a_suppr = [] # les diviseurs "communs" de k qui sont dans 1 que l'on ne peut pas supprimer avant la fin de la boucle for
			liste_diviseurs_communs = []
			for i in range(len(dec_1)):
				if dec_1[i] in dec_2: 
					liste_diviseurs_communs.append(dec_1[i])
					liste_diviseurs_a_suppr.append(i)
					del dec_2[dec_2.index(dec_1[i])] # on supprime le facteur que l'on retrouve dans k
			for i in range(len(liste_diviseurs_a_suppr)): # suppression des facteurs utilisés
				del dec_1[liste_diviseurs_a_suppr[i]]
				for j in range(len(liste_diviseurs_a_suppr)): 
					liste_diviseurs_a_suppr[j] = liste_diviseurs_a_suppr[j] - 1
			k = 1 
			for i in range(len(liste_diviseurs_communs)): 
				k *= liste_diviseurs_communs[i]
			a = 1
			for i in range(len(dec_1)):
				a *= dec_1[i]
			O = 1
			for i in range(len(dec_2)):
				O *= dec_2[i]
		nb_etages_inaccessibles = (self.intervalle * k - self.intervalle) / k + (a * O - a - O + 1) / 2 # on applique la formule 
		return nb_etages_inaccessibles

	def premiersEntreEux(self, x, y): 
		""" Méthode permettant de savoir si deux nombres donnés sont premiers entre eux. """ 
		premiers_entre_eux = True 
		dec_x = self.decomposer(x)
		dec_y = self.decomposer(y)
		for i in range(len(dec_x)):
			if dec_x[i] in dec_y: # on teste si on trouve un facteur de la décomposition commun 
				premiers_entre_eux = False 
		return premiers_entre_eux


class ImmeubleTroisBoutonsNaturels(Immeuble):
	""" Classe représentant un immeuble avec trois boutons naturels, en plus de 0. """
	def __init__(self, intervalle, liste_boutons):
		self.bouton1 = liste_boutons[1]
		self.bouton2 = liste_boutons[2]
		self.bouton3 = liste_boutons[3]
		Immeuble.__init__(self, intervalle, liste_boutons)

	def calculerEtagesAccessibles(self):
		""" Méthode permettant de calculer les étages accessibles à partir des trois boutons de l'immeuble. """
		liste_etages_accessibles = []
		i = 0
		while i * self.bouton1 <= self.intervalle:
			j = 0
			while i * self.bouton1 + j * self.bouton2 <= self.intervalle:
				k = 0
				while i * self.bouton1 + j * self.bouton2 + k * self.bouton3 <= self.intervalle:
					liste_etages_accessibles.append(i * self.bouton1 + j * self.bouton2 + k * self.bouton3)
					k += 1
				j += 1
			i += 1
		liste_etages_accessibles = list(sorted(set(liste_etages_accessibles)))
		return liste_etages_accessibles

	def calculerLimite(self):
		""" Méthode permettant de calculer la limite des boutons, s'il y en a une. """
		return "PROTOTYPE"

	def calculerNbEtagesInaccessibles(self): 
		""" Méthode permettant de calculer le nombre d'étages inaccessibles. """
		return 0

	def premiersEntreEux(self, x, y, z):
		""" Méthode permettant de savoir si trois nombres donnés sont premiers entre eux. """
		premiers_entre_eux = True
		dec_x = self.decomposer(x)
		dec_y = self.decomposer(y)
		dec_z = self.decomposer(z)
		for i in range(len(dec_x)):
			for j in range(len(dec_y)):
				if dec_x[i] in dec_y or dec_x[i] in dec_z or dec_y[j] in dec_z:
					premiers_entre_eux = False
		return premiers_entre_eux


def main():
	""" Fonction prinpale du programme. """
	while True:
		erreur = False
		commande = input("Rentrez la commande que vous souhaitez (pour sortir : exit()).\n")
		try: 
			exec(commande)
		except SyntaxError: 
			erreur = True
			detail_erreur = "SYNTAXE"
		except NameError:
			erreur = True
			detail_erreur = "NOM VARIABLE"
		except AttributeError:
			erreur = True
			detail_erreur = "ATTRIBUT INEXISTANT"
		except ValueError: 
			erreur = True
			detail_erreur = "VALEUR VARIABLE"
		except ZeroDivisionError:
			erreur = True
			detail_erreur = "DIVISION PAR ZERO"
		if(erreur):
			print("La commande n'est rentrée n'est pas correcte ! Détails : {}.".format(detail_erreur))


if __name__ == "__main__":
	main()